# users/serializers.py
from rest_framework import serializers
from .models import CustomUser, CaregiverProfile

class CaregiverProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaregiverProfile
        fields = ['bio', 'hourly_rate', 'area', 'available_days']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        # ใช้ create_user เพื่อให้มีการ hash password โดยอัตโนมัติ
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    # แสดงข้อมูล profile ที่เชื่อมกันอยู่แบบ Nested
    caregiver_profile = CaregiverProfileSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'caregiver_profile']

    def update(self, instance, validated_data):
        # Logic สำหรับการ update profile ที่เป็น nested data
        profile_data = validated_data.pop('caregiver_profile', {})
        profile = instance.caregiver_profile

        # Update fields ของ User instance
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        # Update fields ของ CaregiverProfile instance
        # ถ้ายังไม่มี profile ให้สร้างใหม่
        if not hasattr(instance, 'caregiver_profile'):
            profile = CaregiverProfile.objects.create(user=instance, **profile_data)
        else:
            profile.bio = profile_data.get('bio', profile.bio)
            profile.hourly_rate = profile_data.get('hourly_rate', profile.hourly_rate)
            profile.area = profile_data.get('area', profile.area)
            profile.available_days = profile_data.get('available_days', profile.available_days)
            profile.save()
            
        return instance