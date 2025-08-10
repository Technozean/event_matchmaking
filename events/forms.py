from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import Host, Event, OnboardingQuestion, Participant, PublicQuestion


class HostRegistrationForm(UserCreationForm):
    """Form for host registration"""
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=128, required=True)
    phone = forms.CharField(max_length=20, required=False)
    organization = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'name', 'phone', 'organization')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'name',
            Row(
                Column('phone', css_class='form-group col-md-6 mb-0'),
                Column('organization', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),

        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create host profile
            Host.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                email=self.cleaned_data['email'],
                phone=self.cleaned_data.get('phone', ''),
                organization=self.cleaned_data.get('organization', '')
            )
        return user


class HostProfileForm(forms.ModelForm):
    """Form for editing host profile"""
    class Meta:
        model = Host
        fields = ['name', 'email', 'phone', 'organization']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'email',
            Row(
                Column('phone', css_class='form-group col-md-6 mb-0'),
                Column('organization', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),

        )


class EventCreationForm(forms.ModelForm):
    """Form for creating events"""
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'date', 'end_date', 'location', 
            'max_participants', 'registration_deadline', 'template',
            'allow_waitlist', 'enable_qa', 'enable_matchmaking'
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'registration_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'description',
            Row(
                Column('date', css_class='form-group col-md-6 mb-0'),
                Column('end_date', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('location', css_class='form-group col-md-6 mb-0'),
                Column('max_participants', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('registration_deadline', css_class='form-group col-md-6 mb-0'),
                Column('template', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('allow_waitlist', css_class='form-group col-md-4 mb-0'),
                Column('enable_qa', css_class='form-group col-md-4 mb-0'),
                Column('enable_matchmaking', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),

        )


class OnboardingQuestionForm(forms.ModelForm):
    """Form for creating/editing onboarding questions"""
    class Meta:
        model = OnboardingQuestion
        fields = [
            'question_text', 'question_type', 'is_mandatory', 'order',
            'choices', 'maps_to_field'
        ]
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 2}),
            'choices': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Comma-separated choices for MCQ/Checkboxes'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'question_text',
            Row(
                Column('question_type', css_class='form-group col-md-6 mb-0'),
                Column('maps_to_field', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'choices',
            Row(
                Column('is_mandatory', css_class='form-group col-md-6 mb-0'),
                Column('order', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),

        )


class DynamicParticipantForm(forms.ModelForm):
    """Dynamic form for participant registration based on event questions"""
    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'email', 'phone']

    def __init__(self, event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = event
        
        # Add mandatory default fields
        self.helper = FormHelper()
        
        # Add dynamic fields based on event questions
        layout_fields = ['first_name', 'last_name', 'email', 'phone']
        
        # Get questions for this event (either custom questions or template questions)
        questions = event.onboarding_questions.all()
        if not questions and event.template:
            questions = event.template.template_questions.all()
        
        for question in questions:
            field_name = f'question_{question.id}'
            
            if question.question_type == 'multiple_choice':
                choices = [(choice.strip(), choice.strip()) for choice in question.get_choices_list()]
                self.fields[field_name] = forms.ChoiceField(
                    label=question.question_text,
                    choices=[('', 'Select...')] + choices,
                    required=question.is_mandatory
                )
            elif question.question_type == 'checkboxes':
                choices = [(choice.strip(), choice.strip()) for choice in question.get_choices_list()]
                self.fields[field_name] = forms.MultipleChoiceField(
                    label=question.question_text,
                    choices=choices,
                    widget=forms.CheckboxSelectMultiple,
                    required=question.is_mandatory
                )
            elif question.question_type == 'long_text':
                self.fields[field_name] = forms.CharField(
                    label=question.question_text,
                    widget=forms.Textarea(attrs={'rows': 4}),
                    required=question.is_mandatory
                )
            elif question.question_type == 'rating_scale':
                self.fields[field_name] = forms.ChoiceField(
                    label=question.question_text,
                    choices=[(i, i) for i in range(1, 6)],
                    widget=forms.RadioSelect,
                    required=question.is_mandatory
                )
            elif question.question_type == 'number':
                self.fields[field_name] = forms.IntegerField(
                    label=question.question_text,
                    required=question.is_mandatory
                )
            else:  # short_text, email
                widget = forms.EmailInput if question.question_type == 'email' else forms.TextInput
                self.fields[field_name] = forms.CharField(
                    label=question.question_text,
                    widget=widget,
                    required=question.is_mandatory
                )
            
            layout_fields.append(field_name)
        
        self.helper.layout = Layout(*layout_fields)

    def save(self, commit=True):
        participant = super().save(commit=False)
        participant.event = self.event
        
        if commit:
            participant.save()
            
            # Save question responses and denormalize key fields
            questions = self.event.onboarding_questions.all()
            if not questions and self.event.template:
                questions = self.event.template.template_questions.all()
            
            denormalized_data = {}
            
            for question in questions:
                field_name = f'question_{question.id}'
                if field_name in self.cleaned_data:
                    answer = self.cleaned_data[field_name]
                    
                    # Handle multiple choice fields
                    if isinstance(answer, list):
                        answer = ', '.join(answer)
                    
                    # Create question response
                    from .models import QuestionResponse
                    QuestionResponse.objects.create(
                        participant=participant,
                        question=question,
                        answer=str(answer)
                    )
                    
                    # Store for denormalization
                    if question.maps_to_field:
                        denormalized_data[question.maps_to_field] = answer
            
            # Update participant with denormalized data
            for field, value in denormalized_data.items():
                if hasattr(participant, field):
                    setattr(participant, field, value)
            
            participant.save()
        
        return participant


class PublicQuestionForm(forms.ModelForm):
    """Form for submitting public questions during events"""
    class Meta:
        model = PublicQuestion
        fields = ['question_text']
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ask your question here...'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'question_text'
        )
