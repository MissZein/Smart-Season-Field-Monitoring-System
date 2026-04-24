from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
from datetime import timedelta

class Field(models.Model):
    # Field Stages [cite: 33, 34]
    STAGE_CHOICES = [
        ('PLANTED', 'Planted'),
        ('GROWING', 'Growing'),
        ('READY', 'Ready'),
        ('HARVESTED', 'Harvested'),
    ]

    # Core Attributes 
    name = models.CharField(max_length=100)
    crop_type = models.CharField(max_length=100) 
    planting_date = models.DateField() 
    current_stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='PLANTED')
    
    # Access & Management [cite: 10, 18]
    # Add null=True and blank=True
    assigned_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    notes = models.TextField(blank=True, null=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def field_status(self):
    # Calculate days since planting
        days_in_ground = (date.today() - self.planting_date).days
    
    # 1. COMPLETED: Check for Harvested stage
    # Using .upper() makes the check case-insensitive just in case
        if self.current_stage.upper() in ['HARVESTED', 'HA']:
            return 'Completed' 
    
    # 2. AT RISK: 
    # Let's trigger this if it's been 'PLANTED' for > 14 days without moving to 'GROWING'
    # OR if it's been 'GROWING' for > 60 days (more realistic than 100)
        if self.current_stage.upper() in ['PLANTED', 'PL'] and days_in_ground > 14:
            return 'At Risk'
    
        if self.current_stage.upper() in ['GROWING', 'GR'] and days_in_ground > 60:
            return 'At Risk' 
        
    # 3. ACTIVE: Default for everything else
        return 'Active'