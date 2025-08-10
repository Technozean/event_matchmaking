from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_public_detail, name='event_public_detail'),
    path('register/<int:event_id>/', views.event_registration, name='event_registration'),
    path('qa/<int:event_id>/', views.event_qa, name='event_qa'),
    
    # Authentication
    path('register/host/', views.host_register, name='host_register'),
    path('login/', auth_views.LoginView.as_view(template_name='events/auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Host dashboard and management
    path('dashboard/', views.host_dashboard, name='host_dashboard'),
    path('profile/', views.host_profile, name='host_profile'),
    path('create-event/', views.create_event, name='create_event'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('event/<int:event_id>/questions/', views.manage_questions, name='manage_questions'),
    
    # AJAX endpoints
    path('vote/<int:question_id>/', views.vote_question, name='vote_question'),
]
