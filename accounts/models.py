# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from datetime import timedelta
from django.utils import timezone

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    membership_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    membership_start_date = models.DateField(blank=True, null=True)
    membership_end_date = models.DateField(blank=True, null=True)
    membership_active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def is_membership_valid(self):
        """Check if membership is currently valid"""
        if not self.membership_active:
            return False
        today = timezone.now().date()
        return self.membership_start_date <= today <= self.membership_end_date
    
    def extend_membership(self, duration_days):
        """Extend membership by specified days"""
        if self.membership_end_date:
            self.membership_end_date = self.membership_end_date + timedelta(days=duration_days)
        else:
            self.membership_start_date = timezone.now().date()
            self.membership_end_date = self.membership_start_date + timedelta(days=duration_days)
        self.membership_active = True
        self.save()