from django.contrib import admin
from .models import UserProfile, ChallengeRecord


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'points', 'level', 'created_at']
    list_filter = ['level']
    search_fields = ['user__username']


@admin.register(ChallengeRecord)
class ChallengeRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'challenge_name', 'difficulty', 'status', 'score', 'completed_at']
    list_filter = ['difficulty', 'status']
    search_fields = ['user__username', 'challenge_name']
