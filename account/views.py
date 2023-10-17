import random

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from random import randint
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        if not User.objects.filter(email=request.POST['emailid']).exists():
            user = User()
            user.first_name = request.POST['firstname']
            user.last_name = request.POST['lastname']
            user.email = request.POST['emailid']
            user.username = request.POST['emailid']
            user.password = make_password(request.POST['password'])
            user.save()
            profile = Profile()
            profile.user = user
            profile.phone_number = request.POST['phonenumber']
            profile.address = request.POST['address']
            profile.save()
            messages.success(request, "Customer is registered successfully")
            return render(request, 'register.html')
        else:
            messages.error(request, "Customer is already registered")
            return render(request, 'register.html')
    else:
        return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['emailid'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, "Incorrect Email Id or Password")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

@login_required(login_url='login')
def profile_view(request):
        return render(request,'profile.html')

@login_required(login_url='login')
def edit_profile_view(request):
        if request.method == 'POST':
            user = User.objects.get(id=request.user.id)
            user.first_name = request.POST['firstname']
            user.last_name = request.POST['lastname']
            user.email = request.POST['emailid']
            user.username = request.POST['emailid']
            user.save()
            profile = Profile.objects.get(user_id=request.user.id)
            profile.phone_number = request.POST['phonenumber']
            profile.address = request.POST['address']
            if 'profilepic' in request.FILES:
                profile.image = request.FILES['profilepic']
            profile.save()
            return redirect('profile')
        else:
            return render(request, 'editprofile.html')

@login_required(login_url='login')
def change_password_view(request):
    if request.method == 'POST':
        if request.user.check_password(request.POST['oldpassword']):
            if request.POST['newpassword'] == request.POST['confirmpassword']:
                request.user.set_password(request.POST['newpassword'])
                request.user.save()
                update_session_auth_hash(request, request.user)
                return render(request, 'changepassword.html',
                {'success_message': 'Password is changed successfully'})
            else:
                return render(request, 'changepassword.html',
                {'error_message': 'New and confirm passwords mismatched'})
        else:
            return render(request, 'changepassword.html',
            {'error_message': 'Incorrect old password'})
    else:
        return render(request, 'changepassword.html')

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('logout')

def reset_password_view(request):
    if request.method == 'POST':
        if User.objects.filter(email=request.POST['emailid']).exists():
            user = User.objects.get(email=request.POST['emailid'])
            otp = str(randint(100000, 999999))
            profile = Profile.objects.get(user_id=user.id)
            profile.password_reset_code = otp
            profile.save()
            subject = 'One Time Password(OTP) to reset your password'
            message = "Your OTP to reset your password: " + otp
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['emailid']]
            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            except Exception:
                messages.error(request, 'Something went wrong. Please try again')
                return render(request, 'resetpassword.html')
            else:
                messages.success(request, 'OTP is mailed successfully to your registered email id')
            return render(request, 'resetpassword.html')
        else:
            messages.error(request, "Please enter registered email id")
            return render(request, 'resetpassword.html')
    else:
        return render(request, 'resetpassword.html')