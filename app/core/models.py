from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """学员扩展信息"""

    LEVEL_CHOICES = [
        ('beginner', '入门'),
        ('intermediate', '进阶'),
        ('advanced', '高级'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    points = models.IntegerField(default=0, verbose_name='积分')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    avatar = models.URLField(blank=True, verbose_name='头像URL')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profile'
        verbose_name = '学员信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username} - {self.points}分"


class ChallengeRecord(models.Model):
    """漏洞挑战记录"""

    DIFFICULTY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('pending', '未完成'),
        ('completed', '已完成'),
        ('failed', '失败'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenge_records')
    challenge_id = models.CharField(max_length=50, verbose_name='挑战ID')
    challenge_name = models.CharField(max_length=100, verbose_name='挑战名称')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    score = models.IntegerField(default=0, verbose_name='获得积分')
    writeup = models.TextField(blank=True, verbose_name='WriteUp')
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'challenge_record'
        verbose_name = '挑战记录'
        verbose_name_plural = verbose_name
        unique_together = ['user', 'challenge_id', 'difficulty']

    def __str__(self):
        return f"{self.user.username} - {self.challenge_name}[{self.difficulty}]"
