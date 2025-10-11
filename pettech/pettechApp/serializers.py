from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Pet, CaregiverProfile, JobPost, Proposal, Booking, Review


class UserPublicSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id", "username", "first_name", "last_name"]


class PetSerializer(serializers.ModelSerializer):
	class Meta:
		model = Pet
		fields = ["id", "owner", "name", "species", "age", "notes", "photo"]
		read_only_fields = ["owner", "id"]


class CaregiverProfileSerializer(serializers.ModelSerializer):
	user = UserPublicSerializer(read_only=True)

	class Meta:
		model = CaregiverProfile
		fields = ["id", "user", "bio", "hourly_rate", "area", "available_days"]


class JobPostSerializer(serializers.ModelSerializer):
	owner = UserPublicSerializer(read_only=True)
	pet = PetSerializer()

	class Meta:
		model = JobPost
		fields = [
			"id",
			"owner",
			"pet",
			"title",
			"description",
			"start",
			"end",
			"location",
			"budget",
			"status",
			"created_at",
		]
		read_only_fields = ["id", "status", "created_at", "owner"]

	def create(self, validated_data):
		pet_data = validated_data.pop("pet")
		request = self.context.get("request")
		user = request.user if request else None
		pet = Pet.objects.create(owner=user, **pet_data)
		job_post = JobPost.objects.create(owner=user, pet=pet, **validated_data)
		return job_post

	def update(self, instance, validated_data):
		pet_data = validated_data.pop("pet", None)
		for attr, value in validated_data.items():
			setattr(instance, attr, value)
		if pet_data:
			pet = instance.pet
			for attr, value in pet_data.items():
				setattr(pet, attr, value)
			pet.save()
		instance.save()
		return instance


class ProposalSerializer(serializers.ModelSerializer):
	caregiver = UserPublicSerializer(read_only=True)
	job_post = JobPostSerializer(read_only=True)
	caregiver_profile_id = serializers.SerializerMethodField()
	job_post_id = serializers.PrimaryKeyRelatedField(
		source='job_post', queryset=JobPost.objects.all(), write_only=True, required=False
	)

	class Meta:
		model = Proposal
		fields = [
			"id",
			"job_post",
			"job_post_id",
			"caregiver",
			"caregiver_profile_id",
			"message",
			"proposed_rate",
			"status",
			"created_at",
		]
		read_only_fields = ["id", "caregiver", "status", "created_at", "job_post"]

	def get_caregiver_profile_id(self, obj):
		cg = getattr(obj.caregiver, 'caregiver_profile', None)
		return cg.id if cg else None


class BookingSerializer(serializers.ModelSerializer):
	owner = UserPublicSerializer(read_only=True)
	caregiver = UserPublicSerializer(read_only=True)
	pet = PetSerializer(read_only=True)
	proposal = ProposalSerializer(read_only=True)
	has_review = serializers.SerializerMethodField()
	caregiver_profile_id = serializers.SerializerMethodField()

	class Meta:
		model = Booking
		fields = [
			"id",
			"owner",
			"caregiver",
			"pet",
			"start",
			"end",
			"status",
			"created_at",
			"proposal",
			"has_review",
			"caregiver_profile_id",
		]
		read_only_fields = ["id", "owner", "caregiver", "pet", "created_at", "proposal"]

	def get_has_review(self, obj):
		try:
			return hasattr(obj, 'review') and obj.review is not None
		except Exception:
			return False

	def get_caregiver_profile_id(self, obj):
		cg = getattr(obj.caregiver, 'caregiver_profile', None)
		return cg.id if cg else None


class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Review
		fields = ["id", "booking", "rating", "comment", "created_at"]
		read_only_fields = ["id", "created_at"]
