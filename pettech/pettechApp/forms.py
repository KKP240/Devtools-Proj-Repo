from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Pet, CaregiverProfile, Booking, Review

User = get_user_model()

WEEKDAY_CHOICES = [
    ('Mon','Mon'), ('Tue','Tue'), ('Wed','Wed'),
    ('Thu','Thu'), ('Fri','Fri'), ('Sat','Sat'), ('Sun','Sun')
]

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_caregiver = forms.BooleanField(required=False, initial=False, label="สมัครเป็นพี่เลี้ยง")

    class Meta:
        model = User
        fields = ("username", "email", "is_caregiver", "password1", "password2")

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ["name", "species", "age", "notes", "photo"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

class CaregiverProfileForm(forms.ModelForm):
    # available_days in model is JSONField(list) — we expose as MultipleChoice here
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
        # store list (JSONField will accept)
        return list(days)

class BookingForm(forms.ModelForm):
    start = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Booking
        fields = ["pet", "start", "end"]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 3}),
        }
