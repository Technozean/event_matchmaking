from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Q
from .models import (
    Host, Event, EventTemplate, OnboardingQuestion, Participant, 
    PublicQuestion, QuestionVote, ParticipantMatch, EventInsight
)
from .forms import (
    HostRegistrationForm, HostProfileForm, EventCreationForm, 
    OnboardingQuestionForm, DynamicParticipantForm, PublicQuestionForm
)


def home(request):
    """Home page"""
    recent_events = Event.objects.filter(
        status='published',
        date__gte=timezone.now()
    ).order_by('date')[:6]
    
    context = {
        'recent_events': recent_events
    }
    return render(request, 'events/home.html', context)


def host_register(request):
    """Host registration view"""
    if request.method == 'POST':
        form = HostRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Event Matchmaking.')
            return redirect('host_dashboard')
    else:
        form = HostRegistrationForm()
    
    return render(request, 'events/auth/register.html', {'form': form})


@login_required
def host_dashboard(request):
    """Host dashboard showing their events and analytics"""
    try:
        host = request.user.host_profile
    except Host.DoesNotExist:
        messages.error(request, 'Please complete your host profile.')
        return redirect('host_profile')
    
    events = host.events.all().order_by('-created_at')
    
    # Get basic stats
    total_events = events.count()
    total_participants = sum(event.participant_count for event in events)
    upcoming_events = events.filter(date__gte=timezone.now(), status='published').count()
    
    context = {
        'host': host,
        'events': events[:10],  # Latest 10 events
        'stats': {
            'total_events': total_events,
            'total_participants': total_participants,
            'upcoming_events': upcoming_events,
        }
    }
    return render(request, 'events/host/dashboard.html', context)


@login_required
def host_profile(request):
    """Host profile management"""
    try:
        host = request.user.host_profile
    except Host.DoesNotExist:
        # Create host profile if doesn't exist
        host = Host.objects.create(
            user=request.user,
            name=request.user.get_full_name() or request.user.username,
            email=request.user.email
        )
    
    if request.method == 'POST':
        form = HostProfileForm(request.POST, instance=host)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('host_dashboard')
    else:
        form = HostProfileForm(instance=host)
    
    return render(request, 'events/host/profile.html', {'form': form, 'host': host})


@login_required
def create_event(request):
    """Create a new event"""
    try:
        host = request.user.host_profile
    except Host.DoesNotExist:
        messages.error(request, 'Please complete your host profile first.')
        return redirect('host_profile')
    
    if request.method == 'POST':
        form = EventCreationForm(request.POST)
        if form.is_valid():
            try:
                event = form.save(commit=False)
                event.host = host
                event.save()
            except Exception as e:
                messages.error(request, f'Error creating event: {str(e)}')
                return render(request, 'events/host/create_event.html', {'form': form})
            
            # Copy questions from template if selected
            if event.template:
                template_questions = event.template.template_questions.all()
                for template_q in template_questions:
                    OnboardingQuestion.objects.create(
                        event=event,
                        question_text=template_q.question_text,
                        question_type=template_q.question_type,
                        is_mandatory=template_q.is_mandatory,
                        order=template_q.order,
                        choices=template_q.choices,
                        maps_to_field=template_q.maps_to_field
                    )
            
            messages.success(request, 'Event created successfully!')
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventCreationForm()
    
    return render(request, 'events/host/create_event.html', {'form': form})


@login_required
def event_detail(request, event_id):
    """Event detail view for hosts"""
    event = get_object_or_404(Event, id=event_id, host__user=request.user)
    
    # Handle publish action
    if request.method == 'POST' and request.POST.get('action') == 'publish':
        if event.status == 'draft':
            event.status = 'published'
            event.save()
            messages.success(request, f'"{event.title}" has been published! Participants can now register.')
        else:
            messages.warning(request, 'This event is already published.')
        return redirect('event_detail', event_id=event.id)
    
    participants = event.participants.all().order_by('-registered_at')
    questions = event.onboarding_questions.all().order_by('order')
    public_questions = event.public_questions.all()[:10]
    
    context = {
        'event': event,
        'participants': participants,
        'questions': questions,
        'public_questions': public_questions,
    }
    return render(request, 'events/host/event_detail.html', context)


@login_required
def edit_event(request, event_id):
    """Edit an existing event"""
    event = get_object_or_404(Event, id=event_id, host__user=request.user)
    
    if request.method == 'POST':
        form = EventCreationForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventCreationForm(instance=event)
    
    return render(request, 'events/host/edit_event.html', {'form': form, 'event': event})


@login_required
def manage_questions(request, event_id):
    """Manage onboarding questions for an event"""
    event = get_object_or_404(Event, id=event_id, host__user=request.user)
    questions = event.onboarding_questions.all().order_by('order')
    
    if request.method == 'POST':
        form = OnboardingQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.event = event
            question.save()
            messages.success(request, 'Question added successfully!')
            return redirect('manage_questions', event_id=event.id)
    else:
        form = OnboardingQuestionForm()
    
    context = {
        'event': event,
        'questions': questions,
        'form': form
    }
    return render(request, 'events/host/manage_questions.html', context)


def event_registration(request, event_id):
    """Public event registration page"""
    event = get_object_or_404(Event, id=event_id, status='published')
    
    # Check if registration is still open
    if event.registration_deadline and timezone.now() > event.registration_deadline:
        messages.error(request, 'Registration for this event has closed.')
        return render(request, 'events/registration_closed.html', {'event': event})
    
    # Check if event is full
    is_full = event.max_participants and event.participant_count >= event.max_participants
    
    if request.method == 'POST':
        form = DynamicParticipantForm(event, request.POST)
        if form.is_valid():
            # Check if email already registered
            existing = Participant.objects.filter(
                event=event, 
                email=form.cleaned_data['email']
            ).first()
            
            if existing:
                messages.error(request, 'This email is already registered for this event.')
            else:
                participant = form.save(commit=False)
                
                # Determine status based on availability
                if is_full and event.allow_waitlist:
                    participant.status = 'waitlisted'
                    status_message = 'You have been added to the waitlist.'
                elif is_full:
                    messages.error(request, 'This event is full and waitlist is not available.')
                    return render(request, 'events/register.html', {'form': form, 'event': event})
                else:
                    participant.status = 'registered'
                    status_message = 'Registration successful!'
                
                participant.save()
                form.save_m2m()  # Save many-to-many relationships
                
                messages.success(request, status_message)
                return render(request, 'events/registration_success.html', {
                    'participant': participant,
                    'event': event
                })
    else:
        form = DynamicParticipantForm(event)
    
    context = {
        'event': event,
        'form': form,
        'is_full': is_full
    }
    return render(request, 'events/register.html', context)


def event_qa(request, event_id):
    """Public Q&A page for events"""
    event = get_object_or_404(Event, id=event_id, enable_qa=True)
    questions = event.public_questions.all()
    
    # Check if user is a registered participant
    participant = None
    if request.POST.get('email'):
        participant = Participant.objects.filter(
            event=event,
            email=request.POST.get('email')
        ).first()
    
    if request.method == 'POST' and 'submit_question' in request.POST:
        form = PublicQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.event = event
            question.participant = participant
            question.save()
            messages.success(request, 'Question submitted successfully!')
            return redirect('event_qa', event_id=event.id)
    else:
        form = PublicQuestionForm()
    
    context = {
        'event': event,
        'questions': questions,
        'form': form,
        'participant': participant
    }
    return render(request, 'events/qa.html', context)


@require_POST
def vote_question(request, question_id):
    """Vote on a public question"""
    question = get_object_or_404(PublicQuestion, id=question_id)
    
    # Get participant email from request
    email = request.POST.get('email')
    if not email:
        return JsonResponse({'error': 'Email required'}, status=400)
    
    participant = get_object_or_404(
        Participant, 
        event=question.event, 
        email=email
    )
    
    # Check if already voted
    vote, created = QuestionVote.objects.get_or_create(
        question=question,
        participant=participant
    )
    
    if created:
        question.votes += 1
        question.save()
        return JsonResponse({'votes': question.votes, 'voted': True})
    else:
        # Remove vote
        vote.delete()
        question.votes -= 1
        question.save()
        return JsonResponse({'votes': question.votes, 'voted': False})


def event_list(request):
    """Public list of available events"""
    events = Event.objects.filter(
        status='published',
        date__gte=timezone.now()
    ).order_by('date')
    
    # Filter by search query
    search = request.GET.get('search')
    if search:
        events = events.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(location__icontains=search)
        )
    
    context = {
        'events': events,
        'search': search
    }
    return render(request, 'events/event_list.html', context)


def event_public_detail(request, event_id):
    """Public event detail page"""
    event = get_object_or_404(Event, id=event_id, status='published')
    
    context = {
        'event': event
    }
    return render(request, 'events/event_public_detail.html', context)
