from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.views import View

from .models import CaregiverProfile, Pet, Booking, Review, JobPost, Proposal
from .forms import (
    RegisterForm, LoginForm, PetForm, CaregiverProfileForm,
    BookingForm, ReviewForm, JobPostForm, ProposalForm
)

def home(request):
    caregivers = CaregiverProfile.objects.select_related('user').all()[:12]
    job_posts = JobPost.objects.filter(status='open').select_related('owner', 'pet')[:12]
    return render(request, 'index.html', {'caregivers': caregivers, 'job_posts': job_posts})

def caregiver_list(request):
    q = request.GET.get('q', '')
    qs = CaregiverProfile.objects.select_related('user').all()
    if q:
        qs = qs.filter(user__username__icontains=q)
    return render(request, 'caregiver_list.html', {'caregivers': qs, 'query': q})

def caregiver_detail(request, pk):
    caregiver = get_object_or_404(CaregiverProfile, pk=pk)
    reviews = Review.objects.filter(booking__caregiver=caregiver.user).select_related('booking')
    return render(request, 'caregiver_detail.html', {
        'caregiver': caregiver,
        'reviews': reviews,
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
def job_post_create(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job_post = form.save(commit=False)
            job_post.owner = request.user
            job_post.save()
            messages.success(request, "Job post created.")
            return redirect('job_post_list')
    else:
        form = JobPostForm(user=request.user)  # Pass user to filter pets
    return render(request, 'job_post_create.html', {'form': form})

def job_post_list(request):
    q = request.GET.get('q', '')
    qs = JobPost.objects.filter(status='open').select_related('owner', 'pet')
    if q:
        qs = qs.filter(title__icontains=q)
    return render(request, 'job_post_list.html', {'job_posts': qs, 'query': q})

def job_post_detail(request, pk):
    job_post = get_object_or_404(JobPost, pk=pk)
    proposals = job_post.proposals.select_related('caregiver').all()
    proposal_form = ProposalForm() if job_post.status == 'open' else None
    return render(request, 'job_post_detail.html', {
        'job_post': job_post,
        'proposals': proposals,
        'proposal_form': proposal_form,
    })

@login_required
def proposal_submit(request, job_post_id):
    job_post = get_object_or_404(JobPost, pk=job_post_id, status='open')
    if not hasattr(request.user, 'caregiver_profile'):
        messages.error(request, "You need a caregiver profile to submit a proposal.")
        return redirect('job_post_detail', pk=job_post_id)
    if request.method == 'POST':
        form = ProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.job_post = job_post
            proposal.caregiver = request.user
            proposal.save()
            messages.success(request, "Proposal submitted.")
            return redirect('job_post_detail', pk=job_post_id)
    else:
        form = ProposalForm()
    return render(request, 'proposal_submit.html', {'form': form, 'job_post': job_post})

@login_required
def proposal_accept(request, job_post_id, proposal_id):
    job_post = get_object_or_404(JobPost, pk=job_post_id)
    proposal = get_object_or_404(Proposal, pk=proposal_id, job_post=job_post)
    if request.user != job_post.owner:
        messages.error(request, "Only the job post owner can accept proposals.")
        return redirect('job_post_detail', pk=job_post_id)
    if job_post.status != 'open':
        messages.error(request, "This job post is no longer open.")
        return redirect('job_post_detail', pk=job_post_id)
    booking = Booking.objects.create(
        owner=job_post.owner,
        caregiver=proposal.caregiver,
        pet=job_post.pet,
        start=job_post.start,
        end=job_post.end,
        status='P',
        proposal=proposal
    )
    proposal.status = 'accepted'
    proposal.save()
    job_post.status = 'assigned'
    job_post.save()
    Proposal.objects.filter(job_post=job_post).exclude(id=proposal_id).update(status='rejected')
    messages.success(request, "Proposal accepted and booking created.")
    return redirect('my_bookings')

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(owner=request.user).select_related('caregiver', 'pet')
    return render(request, 'my_bookings.html', {'bookings': bookings})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html', {"form": form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')