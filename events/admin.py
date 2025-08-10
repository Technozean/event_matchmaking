from django.contrib import admin
from .models import (
    Host, Event, EventTemplate, OnboardingQuestion, Participant, 
    QuestionResponse, PublicQuestion, QuestionVote, ParticipantMatch,
    EventInsight, ChatQuery
)


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'organization', 'created_at']
    list_filter = ['created_at', 'organization']
    search_fields = ['name', 'email', 'organization']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(EventTemplate)
class EventTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'is_active', 'created_at']
    list_filter = ['template_type', 'is_active']
    search_fields = ['name', 'description']


class OnboardingQuestionInline(admin.TabularInline):
    model = OnboardingQuestion
    extra = 0
    fields = ['question_text', 'question_type', 'is_mandatory', 'order', 'maps_to_field']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'host', 'date', 'status', 'participant_count', 'created_at']
    list_filter = ['status', 'date', 'enable_qa', 'enable_matchmaking']
    search_fields = ['title', 'description', 'host__name']
    readonly_fields = ['created_at', 'updated_at', 'participant_count', 'waitlist_count']
    inlines = [OnboardingQuestionInline]
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('host', 'title', 'description', 'location')
        }),
        ('Schedule', {
            'fields': ('date', 'end_date', 'registration_deadline')
        }),
        ('Registration', {
            'fields': ('max_participants', 'template', 'qr_code')
        }),
        ('Settings', {
            'fields': ('status', 'allow_waitlist', 'enable_qa', 'enable_matchmaking')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'participant_count', 'waitlist_count'),
            'classes': ('collapse',)
        })
    )


@admin.register(OnboardingQuestion)
class OnboardingQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'event', 'question_type', 'is_mandatory', 'order']
    list_filter = ['question_type', 'is_mandatory', 'event']
    search_fields = ['question_text', 'event__title']
    list_editable = ['order', 'is_mandatory']


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'event', 'status', 'role', 'industry', 'registered_at']
    list_filter = ['status', 'event', 'industry', 'experience_years']
    search_fields = ['first_name', 'last_name', 'email', 'role', 'skills']
    readonly_fields = ['registered_at', 'updated_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Event Details', {
            'fields': ('event', 'status', 'priority_score')
        }),
        ('Profile Information', {
            'fields': ('role', 'company', 'industry', 'experience_years', 'skills', 'interests', 'bio')
        }),
        ('Timestamps', {
            'fields': ('registered_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = ['participant', 'question', 'answer', 'created_at']
    list_filter = ['question__question_type', 'created_at']
    search_fields = ['participant__first_name', 'participant__last_name', 'answer']


@admin.register(PublicQuestion)
class PublicQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'event', 'votes', 'is_answered', 'created_at']
    list_filter = ['is_answered', 'event', 'created_at']
    search_fields = ['question_text', 'answer']
    readonly_fields = ['votes', 'created_at']


@admin.register(QuestionVote)
class QuestionVoteAdmin(admin.ModelAdmin):
    list_display = ['participant', 'question', 'created_at']
    list_filter = ['created_at']


@admin.register(ParticipantMatch)
class ParticipantMatchAdmin(admin.ModelAdmin):
    list_display = ['participant1', 'participant2', 'match_score', 'is_mutual', 'created_at']
    list_filter = ['is_mutual', 'event', 'created_at']
    search_fields = ['participant1__first_name', 'participant2__first_name', 'match_reasons']
    readonly_fields = ['created_at']


@admin.register(EventInsight)
class EventInsightAdmin(admin.ModelAdmin):
    list_display = ['event', 'insight_type', 'title', 'generated_at']
    list_filter = ['insight_type', 'generated_at']
    search_fields = ['title', 'content']
    readonly_fields = ['generated_at']


@admin.register(ChatQuery)
class ChatQueryAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'query', 'query_type', 'created_at']
    list_filter = ['query_type', 'created_at']
    search_fields = ['query', 'response', 'user__username']
    readonly_fields = ['created_at']
