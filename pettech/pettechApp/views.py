from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import CaregiverProfile, Pet, Booking, Review
from .forms import (
    RegisterForm, LoginForm, PetForm, CaregiverProfileForm,
    BookingForm, ReviewForm
)



def home(request):
    # show featured caregivers on home
    caregivers = CaregiverProfile.objects.select_related('user').all()[:12]
    return render(request, 'index.html', {'caregivers': caregivers})

def caregiver_list(request):
    q = request.GET.get('q', '')
    qs = CaregiverProfile.objects.select_related('user').all()
    if q:
        qs = qs.filter(user__username__icontains=q)  # simple filter, adapt as needed
    return render(request, 'caregiver_list.html', {'caregivers': qs, 'query': q})

def caregiver_detail(request, pk):
    caregiver = get_object_or_404(CaregiverProfile, pk=pk)
    reviews = caregiver.user.reviews.all() if hasattr(caregiver.user, 'reviews') else []
    booking_form = BookingForm()
    review_form = ReviewForm()
    return render(request, 'caregiver_detail.html', {
        'caregiver': caregiver,
        'reviews': reviews,
        'booking_form': booking_form,
        'review_form': review_form,
    })

@login_required
def pet_add(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            messages.success(request, "Pet added.")
            return redirect('home')
    else:
        form = PetForm()
    return render(request, 'pet_add.html', {'form': form})

@login_required
def booking_create(request, caregiver_id):
    caregiver = get_object_or_404(CaregiverProfile, pk=caregiver_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.owner = request.user
            booking.caregiver = caregiver.user
            booking.save()
            messages.success(request, "Booking requested.")
            return redirect('my_bookings')
    else:
        form = BookingForm()
    return render(request, 'booking_form.html', {'form': form, 'caregiver': caregiver})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(owner=request.user).select_related('caregiver','pet')
    return render(request, 'my_bookings.html', {'bookings': bookings})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # if user indicated is_caregiver, create empty caregiver profile
            if form.cleaned_data.get('is_caregiver'):
                CaregiverProfile.objects.get_or_create(user=user)
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in.")
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out.")
    return redirect('home')

def pet_list(request):
    pet = Pet.objects.select_related('owner').all()[:12]
    return render(request, 'pet.html', {'pet': pet})
