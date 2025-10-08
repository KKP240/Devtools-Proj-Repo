# pet_service/serializers.py
from rest_framework import serializers
from .models import Pet

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'owner_id', 'name', 'species', 'age', 'notes', 'photo']
        read_only_fields = ['owner_id'] # ป้องกันไม่ให้มีการส่ง owner_id มาแก้ไขโดยตรง