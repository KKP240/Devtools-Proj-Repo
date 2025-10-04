from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Pet, CaregiverProfile, Booking, Review, JobPost, Proposal, User

WEEKDAY_CHOICES = [
    ('Mon', 'Mon'), ('Tue', 'Tue'), ('Wed', 'Wed'),
    ('Thu', 'Thu'), ('Fri', 'Fri'), ('Sat', 'Sat'), ('Sun', 'Sun')
]

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        pw = cleaned_data.get('password')
        confirm_pw = cleaned_data.get('confirm_password')
        if pw != confirm_pw:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ["name", "species", "age", "notes", "photo"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
            "photo": forms.URLInput(attrs={
                'placeholder': 'https://example.com/photo.jpg (ไม่บังคับ)'
            }),
        }

class CaregiverProfileForm(forms.ModelForm):
    available_days = forms.MultipleChoiceField(
        choices=WEEKDAY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = CaregiverProfile
        fields = ["bio", "hourly_rate", "area", "available_days"]

    def clean_available_days(self):
        days = self.cleaned_data.get("available_days", [])
        return list(days)

class BookingForm(forms.ModelForm):
    start = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Booking
        fields = ["pet", "start", "end"]

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')
        if start and end and start >= end:
            raise forms.ValidationError("End time must be after start time.")
        return cleaned_data

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 3}),
        }

# แก้ไข: ลบ field 'pet' ออก เพราะจะสร้างพร้อมกันกับ PetForm
class JobPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = JobPost
        fields = ["title", "description", "start", "end", "location", "budget"]
        widgets = {
            "start": forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            "end": forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            "description": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "budget": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')
        if start and end and start >= end:
            raise forms.ValidationError("End time must be after start time.")
        return cleaned_data

class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ["message", "proposed_rate"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_proposed_rate(self):
        rate = self.cleaned_data.get('proposed_rate')
        if rate <= 0:
            raise forms.ValidationError("Proposed rate must be positive.")
        return rate