from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.db import models
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
    
    # ตรวจสอบว่ามี caregiver profile หรือไม่
    if not hasattr(request.user, 'caregiver_profile'):
        messages.error(request, "คุณต้องมีโปรไฟล์ผู้ดูแลเพื่อส่งข้อเสนอ")
        return redirect('job_post_detail', pk=job_post_id)
    
    # ป้องกันไม่ให้ owner ส่งข้อเสนอให้งานของตัวเอง
    if request.user == job_post.owner:
        messages.error(request, "คุณไม่สามารถส่งข้อเสนอให้งานของตัวเองได้")
        return redirect('job_post_detail', pk=job_post_id)
    
    # ตรวจสอบว่าเคยส่งข้อเสนอไปแล้วหรือยัง
    existing_proposal = Proposal.objects.filter(
        job_post=job_post, 
        caregiver=request.user
    ).first()
    
    if existing_proposal:
        messages.warning(request, "คุณได้ส่งข้อเสนอสำหรับงานนี้ไปแล้ว")
        return redirect('job_post_detail', pk=job_post_id)
    
    if request.method == 'POST':
        form = ProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.job_post = job_post
            proposal.caregiver = request.user
            proposal.save()
            messages.success(request, "ส่งข้อเสนอเรียบร้อยแล้ว")
            return redirect('job_post_detail', pk=job_post_id)
        else:
            # ถ้า form ไม่ valid ให้แสดง error กลับไปที่หน้า detail พร้อม form
            proposals = job_post.proposals.select_related('caregiver').all()
            return render(request, 'job_post_detail.html', {
                'job_post': job_post,
                'proposals': proposals,
                'proposal_form': form,  # ส่ง form ที่มี error กลับไป
            })
    
    # ถ้าเป็น GET request ให้ redirect กลับไปหน้า detail
    return redirect('job_post_detail', pk=job_post_id)

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

    if request.method == 'POST':
        # Use valid booking status, e.g. 'C'
        booking = Booking.objects.create(
            owner=job_post.owner,
            caregiver=proposal.caregiver,
            pet=job_post.pet,
            start=job_post.start,
            end=job_post.end,
            status='C',  # confirmed
            proposal=proposal
        )
        proposal.status = 'accepted'
        proposal.save()
        job_post.status = 'assigned'
        job_post.save()
        # Reject others
        Proposal.objects.filter(job_post=job_post).exclude(id=proposal_id).update(status='rejected')
        messages.success(request, "Proposal accepted and booking created.")
        return redirect('booking_list')
    else:
        messages.error(request, "Invalid request method.")
        return redirect('job_post_detail', pk=job_post_id)

@login_required
def myposts(request):
    job_posts = JobPost.objects.filter(owner=request.user).select_related('pet')
    return render(request, 'myposts.html', {'job_posts': job_posts})

@login_required
def booking_list(request):
    owner_bookings = Booking.objects.filter(owner=request.user).select_related('caregiver', 'pet', 'proposal')
    caregiver_bookings = Booking.objects.filter(caregiver=request.user).select_related('owner', 'pet', 'proposal')

    return render(request, 'booking_list.html', {
        'owner_bookings': owner_bookings,
        'caregiver_bookings': caregiver_bookings,
    })

@login_required
def booking_complete(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)

    if request.user != booking.owner and request.user != booking.caregiver:
        messages.error(request, "You cannot complete this booking.")
        return redirect('booking_list')

    if booking.status != 'C':
        messages.error(request, "This booking is not confirmed.")
        return redirect('booking_list')

    booking.status = 'D'
    booking.save()
    messages.success(request, "Booking marked as completed.")
    return redirect('booking_list')

@login_required
def my_booking_history(request):
    # Get bookings where user is either owner or caregiver
    bookings = Booking.objects.filter(
        models.Q(owner=request.user) | models.Q(caregiver=request.user)
    ).select_related('proposal__job_post', 'caregiver', 'owner', 'pet').order_by('-start')
    
    return render(request, 'booking_history.html', {'bookings': bookings})

@login_required
def write_review(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, owner=request.user, status='D')
    # status 'D' means done/completed
    if hasattr(booking, 'review'):
        messages.error(request, "You have already reviewed this booking.")
        return redirect('booking_history')

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
    user = request.user
    pets = user.pets.all() 

    caregiver_profile = None
    if hasattr(user, 'caregiver_profile'):
        caregiver_profile = user.caregiver_profile

    context = {
        'user': user,
        'pets': pets,
        'caregiver_profile': caregiver_profile,
    }
    return render(request, 'myprofile.html', context)

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
    
@login_required
def caregiver_register(request):

    if request.method == 'POST':
        print("DEBUG caregiver_register: POST by", request.user)  # debug
        print("DEBUG POST data:", dict(request.POST))
        form = CaregiverProfileForm(request.POST)
        if form.is_valid():
            caregiver_profile = form.save(commit=False)
            caregiver_profile.user = request.user
            caregiver_profile.save()
            messages.success(request, "Caregiver profile created successfully.")
            return redirect('myprofile')
        else:
            print("DEBUG caregiver_register errors:", form.errors)  # debug
            messages.error(request, "มีข้อผิดพลาด: ดูคอนโซลเซิร์ฟเวอร์สำหรับรายละเอียด")
    else:
        form = CaregiverProfileForm()

    return render(request, 'caregiver_register.html', {'form': form})


@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        updated = False
        
        # Update username and email
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        # Validate username uniqueness
        if username and username != user.username:
            from django.contrib.auth.models import User
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            else:
                user.username = username
                updated = True
        
        # Validate email
        if email and email != user.email:
            user.email = email
            updated = True
        
        # Save user changes if any
        if updated:
            try:
                user.save()
                messages.success(request, "Profile updated successfully")
            except Exception as e:
                messages.error(request, f"Error updating profile: {str(e)}")
        
        # Handle pet form
        pet_form = PetForm(request.POST, request.FILES)
        if pet_form.is_valid():
            # Add new pet if form has data
            if pet_form.cleaned_data.get('name'):
                pet = pet_form.save(commit=False)
                pet.owner = user
                pet.save()
                messages.success(request, "Pet added successfully")
        else:
            if pet_form.errors:
                for field, errors in pet_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        
        # Redirect after POST (always redirect after successful POST)
        return redirect('myprofile')
    else:
        pet_form = PetForm()

    return render(request, 'edit_profile.html', {
        'pet_form': pet_form,
    })

@login_required
def job_post_edit(request, pk):
    job_post = get_object_or_404(JobPost, pk=pk, owner=request.user)
    pet = job_post.pet

    if request.method == 'POST':
        job_form = JobPostForm(request.POST, instance=job_post, user=request.user)
        pet_form = PetForm(request.POST, request.FILES, instance=pet)

        if job_form.is_valid() and pet_form.is_valid():
            pet_form.save()
            job_form.save()
            messages.success(request, "อัปเดตโพสต์งานเรียบร้อยแล้ว")
            return redirect('myposts')
        else:
            print("DEBUG job_post_edit errors:", job_form.errors, pet_form.errors)
            messages.error(request, "มีข้อผิดพลาด: ดูคอนโซลเซิร์ฟเวอร์สำหรับรายละเอียด")
    else:
        job_form = JobPostForm(instance=job_post, user=request.user)
        pet_form = PetForm(instance=pet)

    return render(request, 'job_post_edit.html', {
        'job_form': job_form,
        'pet_form': pet_form,
        'job_post': job_post,
    })

@login_required
def job_post_delete(request, pk):
    job_post = get_object_or_404(JobPost, pk=pk, owner=request.user)

    if request.method == 'POST':
        job_post.delete()
        messages.success(request, "ลบโพสต์งานเรียบร้อยแล้ว")
        return redirect('myposts')

    return render(request, 'job_post_delete_confirm.html', {'job_post': job_post})

@login_required
def my_proposals(request):
    proposals = Proposal.objects.filter(caregiver=request.user).select_related('job_post')
    return render(request, 'my_proposals.html', {'proposals': proposals})

@login_required
def caregiver_edit(request, pk):
    caregiver_profile = get_object_or_404(CaregiverProfile, pk=pk, user=request.user)

    if request.method == 'POST':
        form = CaregiverProfileForm(request.POST, instance=caregiver_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Caregiver profile updated successfully.")
            return redirect('myprofile')
        else:
            print("DEBUG caregiver_edit errors:", form.errors)  # debug
            messages.error(request, "มีข้อผิดพลาด: ดูคอนโซลเซิร์ฟเวอร์สำหรับรายละเอียด")
    else:
        form = CaregiverProfileForm(instance=caregiver_profile)

    return render(request, 'caregiver_edit.html', {'form': form})