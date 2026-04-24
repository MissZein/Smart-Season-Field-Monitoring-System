from django.db import models
from django.contrib.auth.models import User
from datetime import date

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
        """
        Computed status logic [cite: 40, 41]
        - Completed: If stage is Harvested [cite: 44]
        - At Risk: Based on custom logic (e.g., if 'Growing' takes too long) [cite: 43, 45]
        - Active: Default state for growing fields [cite: 42]
        """
        if self.current_stage == 'HARVESTED':
            return 'Completed' 
        
        # 'At Risk' logic: If the crop has been in the 'Growing' stage for over 100 days
        days_in_ground = (date.today() - self.planting_date).days
        if self.current_stage == 'GROWING' and days_in_ground > 100:
            return 'At Risk' 
            
        return 'Active' 