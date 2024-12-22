from django.shortcuts import redirect, render
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required


# General Pages Views
def home(request):
    return render(request, 'pages/index.html')

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    return render(request, 'pages/contact.html')


# Car Listings Views
def car_listings(request):
    return render(request, 'pages/listings/listing-list.html')

def car_listing_detail(request, pk):
    return render(request, 'pages/listings/listing-single.html')


# Authentication Views
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

def login(request): 
    context = {
        'breadcrumb_title': 'Login',
        'breadcrumb_active': 'Login'
    }
    return render(request, 'pages/auth/login.html', context=context)

def register(request):
    context = {
        'breadcrumb_title': 'Register',
        'breadcrumb_active': 'Register'
    }
    return render(request, 'pages/auth/register.html', context=context)

def forgot_password(request):
    context = {
        'breadcrumb_title': 'Forgot Password',
        'breadcrumb_active': 'Forgot Password'
    }
    return render(request, 'pages/auth/forgot-password.html', context=context)

def password_reset(request, uidb64, token):
    context = {
        'breadcrumb_title': 'Password Reset',
        'breadcrumb_active': 'Password Reset'
    }
    return render(request, 'pages/auth/password-reset.html', context=context)

def email_verify(request, uidb64, token):
    context = {
        'breadcrumb_title': 'Email Verification',
        'breadcrumb_active': 'Email Verification'
    }
    url = f'http://127.0.0.1:8000/api/auth/email-verify/{uidb64}/{token}/'
    response = requests.get(url)
    
    if response.status_code == 200:
        return render(request, 'pages/auth/confirmation-successful.html', context=context)
    else:
        return render(request, 'pages/auth/confirmation-failed.html', context=context)


# User Profile Views
def add_listing(request):
    return render(request, 'pages/profile/add-listing.html')

def compare(request):
    return render(request, 'pages/profile/compare.html')

def dashboard(request):
    return render(request, 'pages/profile/dashboard.html')

def profile_listings(request):
    return render(request, 'pages/profile/profile-listing.html')

def profile_settings(request):
    return render(request, 'pages/profile/profile-settings.html')

def profile_favourites(request):
    return render(request, 'pages/profile/profile-favourite.html')

def profile_messages(request):
    return render(request, 'pages/profile/profile-message.html')

def profile(request):
    return render(request, 'pages/profile/profile.html')

