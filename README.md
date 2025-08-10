# 🎯 Event Matchmaking Platform

A comprehensive Django-based event management and networking platform that enables hosts to create engaging events with AI-powered participant matchmaking, interactive Q&A sessions, and intelligent attendee insights.

![Platform Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Django](https://img.shields.io/badge/Django-5.2.5-blue)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.4-blue)

## 🌟 Features

### 🎪 **Event Management**
- **Smart Event Creation** with customizable questionnaire templates
- **QR Code Generation** for easy participant registration
- **Dynamic Registration Forms** that adapt to event requirements
- **Waitlist Management** with automatic priority handling
- **Event Status Management** (Draft → Published → Ongoing → Completed)

### 🤝 **Networking & Engagement**
- **AI-Powered Matchmaking** - Connect participants with similar interests and backgrounds
- **Interactive Q&A Boards** with real-time voting and moderation
- **Participant Profiles** with skills, experience, and interest tracking
- **Smart Attendee Filtering** and prioritization

### 📊 **Analytics & Insights**
- **Host Dashboard** with event statistics and participant analytics
- **Event Insights** powered by AI analysis of attendee data
- **Registration Tracking** with real-time updates
- **Networking Analytics** to measure connection success

### 🎨 **User Experience**
- **Responsive Design** optimized for all devices
- **Modern UI** built with Tailwind CSS
- **Intuitive Navigation** with role-based interfaces
- **Professional Templates** for different event types

## 🛠 Tech Stack

### **Backend**
- **Django 5.2.5** - Web framework
- **Python 3.13** - Programming language
- **SQLite/MySQL** - Database (configurable)
- **Django Crispy Forms** - Enhanced form rendering

### **Frontend**
- **Tailwind CSS 3.4** - Utility-first CSS framework
- **Vanilla JavaScript** - Interactive components
- **Responsive Design** - Mobile-first approach

### **AI & Integrations**
- **OpenAI API** - AI-powered features (matchmaking, insights)
- **QR Code Generation** - Event registration links
- **PIL (Pillow)** - Image processing

### **Development Tools**
- **Django Extensions** - Enhanced development commands
- **Python Decouple** - Environment variable management
- **Django Admin** - Comprehensive admin interface

## 🚀 Quick Start

### **Prerequisites**
- Python 3.11 or higher
- Node.js 16 or higher (for Tailwind CSS)
- Git

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/event_matchmaking.git
cd event_matchmaking
```

### **2. Set Up Python Environment**
```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# On macOS/Linux:
source env/bin/activate
# On Windows:
env\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### **3. Set Up Frontend Assets**
```bash
# Install Node.js dependencies
npm install

# Build Tailwind CSS
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css

# For development (watch mode)
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch
```

### **4. Database Setup**
```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Create sample data
python manage.py create_templates
```

### **5. Start Development Server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to see your Event Matchmaking Platform!

## 📋 Detailed Setup Guide

### **Environment Configuration**

Create a `.env` file in the project root:
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (optional - defaults to SQLite)
DATABASE_URL=mysql://user:password@localhost:3306/event_matchmaking

# OpenAI Configuration (for AI features)
OPENAI_API_KEY=your-openai-api-key

# Email Configuration (optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### **Database Options**

#### **SQLite (Default - Development)**
No additional setup required. Database file created automatically.

#### **MySQL (Production)**
```bash
# Install MySQL connector
pip install mysqlclient

# Update settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'event_matchmaking',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### **Pre-built Templates**

The platform includes questionnaire templates for different event types:

```bash
# Create all default templates
python manage.py create_templates
```

**Available Templates:**
- 🖥️ **Tech Meetup** - Programming languages, frameworks, experience levels
- 🚀 **Startup Networking** - Roles, industries, funding stages, expertise
- 👥 **HR & Talent** - HR functions, tools, years of experience, challenges
- 🎓 **Education** - Educational roles, subjects, grade levels, interests

## 🎮 Usage Guide

### **For Event Hosts**

#### **1. Create Account**
- Register at `/register/host/`
- Complete your host profile
- Access your dashboard at `/dashboard/`

#### **2. Create Events**
```bash
Dashboard → Create Event → Choose Template → Customize Questions → Publish
```

#### **3. Manage Events**
- **Edit Details**: Update event information anytime
- **Manage Questions**: Add/remove/reorder registration questions
- **Monitor Registrations**: Track participant count and waitlist
- **Q&A Moderation**: Answer questions and manage discussions

#### **4. Publish Events**
- Events start as **drafts** (only visible to you)
- Click **"Publish Event"** to make them public
- Published events appear on `/events/` and accept registrations

### **For Participants**

#### **1. Browse Events**
- Visit `/events/` to see all upcoming events
- Search by keywords, location, or event type
- View detailed event information

#### **2. Register for Events**
- Click **"Register"** on any event
- Fill out the dynamic registration form
- Join waitlist if event is full (when enabled)

#### **3. Engage During Events**
- Submit questions on the Q&A board (`/qa/{event_id}/`)
- Vote on questions from other participants
- Connect with suggested matches (when AI features are enabled)

## 🔧 Development Commands

### **Django Management**
```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver

# Django shell
python manage.py shell
```

### **Custom Management Commands**
```bash
# Create questionnaire templates
python manage.py create_templates

# Regenerate QR codes for events
python manage.py regenerate_qr_codes

# Regenerate all QR codes
python manage.py regenerate_qr_codes --all

# Regenerate QR code for specific event
python manage.py regenerate_qr_codes --event-id 1
```

### **Frontend Development**
```bash
# Watch Tailwind CSS changes
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch

# Build for production
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify

# Update Browserslist database
npx update-browserslist-db@latest
```

## 📁 Project Structure

```
event_matchmaking/
├── eventm/                          # Django project settings
│   ├── settings.py                  # Main configuration
│   ├── urls.py                      # Root URL patterns
│   └── wsgi.py                      # WSGI application
├── events/                          # Main Django app
│   ├── models.py                    # Database models
│   ├── views.py                     # View functions
│   ├── forms.py                     # Form definitions
│   ├── admin.py                     # Admin interface
│   ├── urls.py                      # App URL patterns
│   └── management/commands/         # Custom Django commands
├── templates/                       # HTML templates
│   ├── base.html                    # Base template
│   └── events/                      # Event-specific templates
│       ├── auth/                    # Authentication templates
│       └── host/                    # Host dashboard templates
├── static/                          # Static files
│   ├── css/                         # Stylesheets
│   └── js/                          # JavaScript files
├── media/                           # User uploads
│   └── qr_codes/                    # Generated QR codes
├── requirements.txt                 # Python dependencies
├── tailwind.config.js              # Tailwind CSS configuration
└── manage.py                        # Django management script
```

## 🚀 Deployment

### **Production Checklist**

#### **1. Environment Variables**
```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=your-production-secret-key
DATABASE_URL=your-production-database-url
OPENAI_API_KEY=your-openai-api-key
```

#### **2. Database Migration**
```bash
python manage.py migrate --settings=eventm.settings.production
python manage.py collectstatic --noinput
```

#### **3. Web Server Configuration**
- Configure your web server (Nginx, Apache) to serve static files
- Set up WSGI server (Gunicorn, uWSGI)
- Configure SSL certificates for HTTPS

#### **4. Media Files**
- Configure media file storage (AWS S3, local storage)
- Ensure QR code directory is writable
- Set up backup for uploaded files

### **Docker Deployment** (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.13
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "eventm.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 🤖 AI Features (Optional)

### **OpenAI Integration**
To enable AI-powered features, set your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-openai-api-key
```

**AI-Powered Features:**
- 🎯 **Participant Matchmaking** - Match attendees based on skills, interests, and goals
- 💬 **Event Data Chat** - Natural language queries about attendee data
- 📊 **Smart Insights** - AI-generated analytics and recommendations
- 🎨 **Content Suggestions** - Event description and question recommendations

## 🐛 Troubleshooting

### **Common Issues**

#### **QR Code Generation Errors**
```bash
# Regenerate QR codes
python manage.py regenerate_qr_codes --all

# Check media directory permissions
ls -la media/qr_codes/
```

#### **CSS Not Loading**
```bash
# Rebuild Tailwind CSS
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css

# Collect static files
python manage.py collectstatic --clear
```

#### **Database Issues**
```bash
# Reset migrations (development only)
rm events/migrations/0*.py
python manage.py makemigrations events
python manage.py migrate
```

#### **Template Not Found**
- Ensure `DIRS` in `TEMPLATES` setting includes template directory
- Check template file names and paths
- Verify app is in `INSTALLED_APPS`

## 📚 API Documentation

### **Key Models**

#### **Event Model**
```python
class Event(models.Model):
    host = ForeignKey(Host)
    title = CharField(max_length=255)
    description = TextField()
    date = DateTimeField()
    status = CharField(choices=['draft', 'published', 'ongoing', 'completed'])
    max_participants = IntegerField(null=True, blank=True)
    enable_qa = BooleanField(default=True)
    enable_matchmaking = BooleanField(default=True)
```

#### **Participant Model**
```python
class Participant(models.Model):
    event = ForeignKey(Event)
    first_name = CharField(max_length=128)
    last_name = CharField(max_length=128)
    email = EmailField()
    skills = CharField(max_length=500)  # Comma-separated
    role = CharField(max_length=128)
    industry = CharField(max_length=128)
    status = CharField(choices=['registered', 'waitlisted', 'cancelled'])
```

### **Key Views**

#### **Public Views**
- `/` - Home page
- `/events/` - Event listing
- `/events/{id}/` - Event details
- `/register/{id}/` - Event registration
- `/qa/{id}/` - Q&A board

#### **Host Views**
- `/dashboard/` - Host dashboard
- `/create-event/` - Event creation
- `/event/{id}/` - Event management
- `/event/{id}/edit/` - Event editing
- `/event/{id}/questions/` - Question management

## 🤝 Contributing

### **Development Setup**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Follow the setup guide above
4. Make your changes
5. Run tests: `python manage.py test`
6. Submit a pull request

### **Code Standards**
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Write tests for new features
- Update documentation for significant changes

### **Commit Messages**
```
feat: add participant matchmaking algorithm
fix: resolve QR code generation issue
docs: update API documentation
style: improve event card design
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### **Getting Help**
- 📖 **Documentation**: Check this README and inline code comments
- 🐛 **Issues**: Report bugs on the GitHub Issues page
- 💬 **Discussions**: Join community discussions for feature requests
- 📧 **Contact**: Reach out for enterprise support and custom development

### **Useful Resources**
- [Django Documentation](https://docs.djangoproject.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)

---

## 🎉 **Ready to Transform Your Events?**

The Event Matchmaking Platform is production-ready and waiting to power your networking events. From tech meetups to startup pitch nights, create meaningful connections with intelligent matchmaking and engaging interactive features.

**Get started in 5 minutes** with our quick setup guide above! 🚀

---

*Built with ❤️ using Django, Tailwind CSS, and AI-powered intelligence.*
