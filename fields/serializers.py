from rest_framework import serializers
from .models import Field

class FieldUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['current_stage', 'notes'] # Core requirements for updates [cite: 28, 29]