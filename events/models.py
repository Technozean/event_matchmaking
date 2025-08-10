from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Host(models.Model):
    """Host model for event creators"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='host_profile')
    name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class EventTemplate(models.Model):
    """Pre-built questionnaire templates for different event types"""
    TEMPLATE_TYPES = [
        ('tech_meetup', 'Tech Meetup'),
        ('startup_networking', 'Startup Networking'),
        ('hr_talent', 'HR & Talent'),
        ('education', 'Education'),
        ('custom', 'Custom'),
    ]
    
    name = models.CharField(max_length=255)
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPES)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"


class Event(models.Model):
    """Main Event model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    max_participants = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    template = models.ForeignKey(EventTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    
    # Settings
    allow_waitlist = models.BooleanField(default=True)
    enable_qa = models.BooleanField(default=True)
    enable_matchmaking = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Generate QR code when event is saved"""
        # Save first to get the primary key
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Generate QR code only after we have a primary key
        if is_new or not self.qr_code:
            self.generate_qr_code()
    
    def generate_qr_code(self):
        """Generate QR code for event registration"""
        try:
            import qrcode
            from PIL import Image
            from io import BytesIO
            from django.core.files import File
            
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            # Use a more flexible URL (can be configured later)
            qr.add_data(f"http://localhost:8000/register/{self.pk}/")
            qr.make(fit=True)
            
            # Create QR code image
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to RGB if necessary
            if qr_img.mode != 'RGB':
                qr_img = qr_img.convert('RGB')
            
            # Create white background with padding
            width, height = qr_img.size
            new_img = Image.new('RGB', (width + 40, height + 40), 'white')
            new_img.paste(qr_img, (20, 20))
            
            # Save to BytesIO
            stream = BytesIO()
            new_img.save(stream, format='PNG')
            stream.seek(0)
            
            # Save to model field
            file_name = f'qr_event_{self.pk}.png'
            self.qr_code.save(file_name, File(stream), save=False)
            stream.close()
            
            # Save again to update the qr_code field
            super(Event, self).save(update_fields=['qr_code'])
            
        except Exception as e:
            # Log the error but don't fail the save operation
            print(f"Error generating QR code for event {self.pk}: {e}")
            pass

    @property
    def participant_count(self):
        return self.participants.filter(status='registered').count()

    @property
    def waitlist_count(self):
        return self.participants.filter(status='waitlisted').count()


class OnboardingQuestion(models.Model):
    """Questions for participant registration"""
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('short_text', 'Short Text'),
        ('long_text', 'Long Text'),
        ('rating_scale', 'Rating Scale'),
        ('checkboxes', 'Checkboxes'),
        ('email', 'Email'),
        ('number', 'Number'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='onboarding_questions', null=True, blank=True)
    template = models.ForeignKey(EventTemplate, on_delete=models.CASCADE, null=True, blank=True, related_name='template_questions')
    question_text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    is_mandatory = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    # For multiple choice and checkboxes
    choices = models.TextField(blank=True, help_text="Comma-separated choices for MCQ/Checkboxes")
    
    # For denormalized fields (skills, role, industry, etc.)
    maps_to_field = models.CharField(max_length=50, blank=True, help_text="Field name for denormalization")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.question_text[:50]}..."

    def get_choices_list(self):
        """Return choices as a list"""
        if self.choices:
            return [choice.strip() for choice in self.choices.split(',')]
        return []


class Participant(models.Model):
    """Participant registration data"""
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('waitlisted', 'Waitlisted'),
        ('cancelled', 'Cancelled'),
        ('attended', 'Attended'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    
    # Denormalized fields for easy filtering and AI analysis
    skills = models.CharField(max_length=500, blank=True)  # comma-separated
    role = models.CharField(max_length=128, blank=True)
    industry = models.CharField(max_length=128, blank=True)
    experience_years = models.IntegerField(null=True, blank=True)
    interests = models.CharField(max_length=500, blank=True)  # comma-separated
    company = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    
    # Priority scoring for waitlist management
    priority_score = models.FloatField(default=0.0)
    
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['event', 'email']
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.event.title}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_skills_list(self):
        """Return skills as a list"""
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []

    def get_interests_list(self):
        """Return interests as a list"""
        if self.interests:
            return [interest.strip() for interest in self.interests.split(',')]
        return []


class QuestionResponse(models.Model):
    """Individual responses to onboarding questions"""
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(OnboardingQuestion, on_delete=models.CASCADE)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['participant', 'question']

    def __str__(self):
        return f"{self.participant.full_name} - {self.question.question_text[:30]}..."


class PublicQuestion(models.Model):
    """Q&A questions during events"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='public_questions')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, null=True, blank=True)
    question_text = models.TextField()
    votes = models.IntegerField(default=0)
    is_answered = models.BooleanField(default=False)
    answer = models.TextField(blank=True)
    answered_by = models.ForeignKey(Host, on_delete=models.SET_NULL, null=True, blank=True)
    answered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-votes', '-created_at']

    def __str__(self):
        return f"{self.question_text[:50]}... ({self.votes} votes)"


class QuestionVote(models.Model):
    """Track votes on public questions"""
    question = models.ForeignKey(PublicQuestion, on_delete=models.CASCADE, related_name='question_votes')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['question', 'participant']

    def __str__(self):
        return f"{self.participant.full_name} voted on: {self.question.question_text[:30]}..."


class ParticipantMatch(models.Model):
    """AI-generated participant matches"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='matches')
    participant1 = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='matches_as_p1')
    participant2 = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='matches_as_p2')
    match_score = models.FloatField()
    match_reasons = models.TextField()  # AI-generated explanation
    is_mutual = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['participant1', 'participant2']
        ordering = ['-match_score']

    def __str__(self):
        return f"Match: {self.participant1.full_name} <-> {self.participant2.full_name} ({self.match_score:.2f})"


class EventInsight(models.Model):
    """AI-generated insights about events"""
    INSIGHT_TYPES = [
        ('skill_distribution', 'Skill Distribution'),
        ('industry_spread', 'Industry Spread'),
        ('experience_levels', 'Experience Levels'),
        ('interests_analysis', 'Interests Analysis'),
        ('networking_potential', 'Networking Potential'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='insights')
    insight_type = models.CharField(max_length=50, choices=INSIGHT_TYPES)
    title = models.CharField(max_length=255)
    content = models.TextField()
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.event.title} - {self.title}"


class ChatQuery(models.Model):
    """Track AI chat queries about event data"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='chat_queries')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Could be host or participant
    query = models.TextField()
    response = models.TextField()
    query_type = models.CharField(max_length=50, default='general')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.query[:50]}..."
