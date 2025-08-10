from django.core.management.base import BaseCommand
from events.models import EventTemplate, OnboardingQuestion


class Command(BaseCommand):
    help = 'Create pre-built questionnaire templates for different event types'

    def handle(self, *args, **options):
        self.stdout.write('Creating event templates...')
        
        # Tech Meetup Template
        tech_template, created = EventTemplate.objects.get_or_create(
            template_type='tech_meetup',
            defaults={
                'name': 'Tech Meetup Template',
                'description': 'Template for technology meetups and conferences',
                'is_active': True
            }
        )
        
        if created:
            tech_questions = [
                {
                    'question_text': 'What is your current role?',
                    'question_type': 'multiple_choice',
                    'choices': 'Software Engineer,Senior Engineer,Tech Lead,Engineering Manager,Product Manager,Designer,Data Scientist,DevOps Engineer,QA Engineer,Other',
                    'is_mandatory': True,
                    'order': 1,
                    'maps_to_field': 'role'
                },
                {
                    'question_text': 'Which programming languages do you work with? (Select all that apply)',
                    'question_type': 'checkboxes',
                    'choices': 'Python,JavaScript,Java,C++,Go,Rust,TypeScript,Swift,Kotlin,Ruby,PHP,C#',
                    'is_mandatory': True,
                    'order': 2,
                    'maps_to_field': 'skills'
                },
                {
                    'question_text': 'How many years of experience do you have in tech?',
                    'question_type': 'multiple_choice',
                    'choices': '0-1 years,1-3 years,3-5 years,5-8 years,8+ years',
                    'is_mandatory': True,
                    'order': 3,
                    'maps_to_field': 'experience_years'
                },
                {
                    'question_text': 'What technologies/frameworks are you interested in learning more about?',
                    'question_type': 'checkboxes',
                    'choices': 'React,Vue.js,Angular,Node.js,Django,Flask,Spring,Docker,Kubernetes,AWS,Azure,GCP,Machine Learning,AI,Blockchain,IoT',
                    'is_mandatory': False,
                    'order': 4,
                    'maps_to_field': 'interests'
                },
                {
                    'question_text': 'What company do you work for?',
                    'question_type': 'short_text',
                    'is_mandatory': False,
                    'order': 5,
                    'maps_to_field': 'company'
                },
                {
                    'question_text': 'What are you hoping to get out of this event?',
                    'question_type': 'long_text',
                    'is_mandatory': False,
                    'order': 6
                }
            ]
            
            for q_data in tech_questions:
                OnboardingQuestion.objects.create(template=tech_template, **q_data)
            
            self.stdout.write(f'Created Tech Meetup template with {len(tech_questions)} questions')

        # Startup Networking Template
        startup_template, created = EventTemplate.objects.get_or_create(
            template_type='startup_networking',
            defaults={
                'name': 'Startup Networking Template',
                'description': 'Template for startup networking events and pitch sessions',
                'is_active': True
            }
        )
        
        if created:
            startup_questions = [
                {
                    'question_text': 'What is your role in the startup ecosystem?',
                    'question_type': 'multiple_choice',
                    'choices': 'Founder/Co-founder,Employee at Startup,Investor/VC,Advisor/Mentor,Service Provider,Aspiring Entrepreneur,Student,Other',
                    'is_mandatory': True,
                    'order': 1,
                    'maps_to_field': 'role'
                },
                {
                    'question_text': 'What industry/sector are you involved in?',
                    'question_type': 'multiple_choice',
                    'choices': 'FinTech,HealthTech,EdTech,E-commerce,SaaS,AI/ML,Blockchain,IoT,Gaming,Food & Beverage,Transportation,Real Estate,Other',
                    'is_mandatory': True,
                    'order': 2,
                    'maps_to_field': 'industry'
                },
                {
                    'question_text': 'What stage is your startup/company at?',
                    'question_type': 'multiple_choice',
                    'choices': 'Idea Stage,MVP Development,Pre-Seed,Seed,Series A,Series B+,Established Company,Not Applicable',
                    'is_mandatory': False,
                    'order': 3
                },
                {
                    'question_text': 'What are your areas of expertise/skills?',
                    'question_type': 'checkboxes',
                    'choices': 'Product Development,Engineering,Marketing,Sales,Finance,Operations,Legal,HR,Business Development,Strategy,Design,Data Analysis',
                    'is_mandatory': True,
                    'order': 4,
                    'maps_to_field': 'skills'
                },
                {
                    'question_text': 'What type of connections are you looking to make?',
                    'question_type': 'checkboxes',
                    'choices': 'Co-founders,Investors,Mentors,Customers,Partners,Employees,Service Providers,Peers',
                    'is_mandatory': True,
                    'order': 5,
                    'maps_to_field': 'interests'
                },
                {
                    'question_text': 'Tell us about your startup/project in one sentence',
                    'question_type': 'long_text',
                    'is_mandatory': False,
                    'order': 6,
                    'maps_to_field': 'bio'
                }
            ]
            
            for q_data in startup_questions:
                OnboardingQuestion.objects.create(template=startup_template, **q_data)
            
            self.stdout.write(f'Created Startup Networking template with {len(startup_questions)} questions')

        # HR & Talent Template
        hr_template, created = EventTemplate.objects.get_or_create(
            template_type='hr_talent',
            defaults={
                'name': 'HR & Talent Template',
                'description': 'Template for HR networking and talent acquisition events',
                'is_active': True
            }
        )
        
        if created:
            hr_questions = [
                {
                    'question_text': 'What is your role in HR/Talent?',
                    'question_type': 'multiple_choice',
                    'choices': 'HR Director/VP,Talent Acquisition Manager,Recruiter,HR Business Partner,Compensation & Benefits,Learning & Development,HR Generalist,Consultant,Job Seeker,Other',
                    'is_mandatory': True,
                    'order': 1,
                    'maps_to_field': 'role'
                },
                {
                    'question_text': 'What industry do you primarily work in?',
                    'question_type': 'multiple_choice',
                    'choices': 'Technology,Finance,Healthcare,Manufacturing,Retail,Consulting,Education,Government,Non-profit,Startups,Other',
                    'is_mandatory': True,
                    'order': 2,
                    'maps_to_field': 'industry'
                },
                {
                    'question_text': 'How many years of experience do you have in HR?',
                    'question_type': 'multiple_choice',
                    'choices': '0-2 years,2-5 years,5-10 years,10-15 years,15+ years',
                    'is_mandatory': True,
                    'order': 3,
                    'maps_to_field': 'experience_years'
                },
                {
                    'question_text': 'What HR areas are you most interested in?',
                    'question_type': 'checkboxes',
                    'choices': 'Talent Acquisition,Employee Relations,Compensation & Benefits,Learning & Development,Performance Management,HR Technology,Diversity & Inclusion,Culture & Engagement,HR Analytics',
                    'is_mandatory': True,
                    'order': 4,
                    'maps_to_field': 'interests'
                },
                {
                    'question_text': 'What HR tools/platforms do you use?',
                    'question_type': 'checkboxes',
                    'choices': 'Workday,BambooHR,ADP,SuccessFactors,LinkedIn Recruiter,Greenhouse,Lever,Slack,Microsoft Teams,Other',
                    'is_mandatory': False,
                    'order': 5,
                    'maps_to_field': 'skills'
                },
                {
                    'question_text': 'What are your current HR challenges or goals?',
                    'question_type': 'long_text',
                    'is_mandatory': False,
                    'order': 6
                }
            ]
            
            for q_data in hr_questions:
                OnboardingQuestion.objects.create(template=hr_template, **q_data)
            
            self.stdout.write(f'Created HR & Talent template with {len(hr_questions)} questions')

        # Education Template
        education_template, created = EventTemplate.objects.get_or_create(
            template_type='education',
            defaults={
                'name': 'Education Template',
                'description': 'Template for educational events, workshops, and academic conferences',
                'is_active': True
            }
        )
        
        if created:
            education_questions = [
                {
                    'question_text': 'What is your role in education?',
                    'question_type': 'multiple_choice',
                    'choices': 'Teacher/Instructor,Professor,Administrator,Student,Researcher,Curriculum Developer,Educational Technology,Parent/Guardian,Policy Maker,Other',
                    'is_mandatory': True,
                    'order': 1,
                    'maps_to_field': 'role'
                },
                {
                    'question_text': 'What educational level do you primarily work with?',
                    'question_type': 'multiple_choice',
                    'choices': 'Early Childhood,Elementary,Middle School,High School,Higher Education,Adult Education,Corporate Training,Professional Development,Not Applicable',
                    'is_mandatory': True,
                    'order': 2,
                    'maps_to_field': 'industry'
                },
                {
                    'question_text': 'What subject areas are you involved with?',
                    'question_type': 'checkboxes',
                    'choices': 'STEM,Mathematics,Science,Technology,Engineering,Language Arts,Social Studies,Arts,Physical Education,Special Education,ESL,Career & Technical Education',
                    'is_mandatory': True,
                    'order': 3,
                    'maps_to_field': 'skills'
                },
                {
                    'question_text': 'What educational topics interest you most?',
                    'question_type': 'checkboxes',
                    'choices': 'Educational Technology,Online Learning,Curriculum Development,Assessment,Student Engagement,Differentiated Instruction,Classroom Management,Professional Development,Research & Data,Policy & Administration',
                    'is_mandatory': True,
                    'order': 4,
                    'maps_to_field': 'interests'
                },
                {
                    'question_text': 'How many years of experience do you have in education?',
                    'question_type': 'multiple_choice',
                    'choices': '0-2 years,2-5 years,5-10 years,10-20 years,20+ years,Not Applicable',
                    'is_mandatory': False,
                    'order': 5,
                    'maps_to_field': 'experience_years'
                },
                {
                    'question_text': 'What are you hoping to learn or share at this event?',
                    'question_type': 'long_text',
                    'is_mandatory': False,
                    'order': 6
                }
            ]
            
            for q_data in education_questions:
                OnboardingQuestion.objects.create(template=education_template, **q_data)
            
            self.stdout.write(f'Created Education template with {len(education_questions)} questions')

        self.stdout.write(self.style.SUCCESS('Successfully created all event templates!'))
