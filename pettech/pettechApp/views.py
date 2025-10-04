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
    search_query = request.GET.get('search', '')
    if search_query:
        job_posts = JobPost.objects.filter(status='open', title__icontains=search_query).select_related('owner', 'pet')[:12]
        return render(request, 'index.html', {'job_posts': job_posts, 'search_query': search_query})
 
    job_posts = JobPost.objects.filter(status='open').select_related('owner', 'pet')[:12]
    return render(request, 'index.html', {'job_posts': job_posts})

def caregiver_detail(request, pk):
    caregiver = get_object_or_404(CaregiverProfile, pk=pk)
    reviews = Review.objects.filter(booking__caregiver=caregiver.user).select_related('booking')
    return render(request, 'caregiver_detail.html', {
        'caregiver': caregiver,
        'reviews': reviews,
    })

@login_required
def job_post_create(request):
    if request.method == 'POST':
        job_form = JobPostForm(request.POST, user=request.user)
        pet_form = PetForm(request.POST, request.FILES)

        if job_form.is_valid() and pet_form.is_valid():
            pet = pet_form.save(commit=False)
            pet.owner = request.user
            pet.save()

            job_post = job_form.save(commit=False)
            job_post.owner = request.user
            job_post.pet = pet
            job_post.save()

            messages.success(request, "เพิ่มสัตว์เลี้ยงและสร้างงานเรียบร้อยแล้ว")
            return redirect('/')
        else:
            print("=== FORM ERRORS ===")
    else:
        job_form = JobPostForm(user=request.user)
        pet_form = PetForm()

    return render(request, 'job_post_create.html', {
        'job_form': job_form,
        'pet_form': pet_form
    })



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
    return render(request, 'job_post_detail.html', {'form': form, 'job_post': job_post})

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
def myposts(request):
    job_posts = JobPost.objects.filter(owner=request.user).select_related('pet')
    return render(request, 'myposts.html', {'job_posts': job_posts})

@login_required
def booking_detail(request):
    bookings = Booking.objects.filter(owner=request.user).select_related('caregiver', 'pet')
    return render(request, 'booking_detail.html', {'bookings': bookings})

@login_required
def my_booking_history(request):
    bookings = Booking.objects.filter(owner=request.user).select_related('caregiver', 'pet')
    return render(request, 'booking_history.html', {'bookings': bookings})

@login_required
def write_review(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, owner=request.user, status='D')
    if hasattr(booking, 'review'):
        messages.error(request, "You have already reviewed this booking.")
        return redirect('booking_history')
    if request.method == 'GET':
        form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.save()
            messages.success(request, "Review submitted successfully.")
            return redirect('booking_history')
    else:
        form = ReviewForm()

    return render(request, 'write_review.html', {'form': form, 'booking': booking})

@login_required
def myprofile(request):
    return render(request, 'myprofile.html')

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