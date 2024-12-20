from django.urls import path
from django.urls import include
from . import views

app_name = 'frontend'

urlpatterns = [
    # General Pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Car Listings
    path('car-listings/list', views.car_listings, name='car_listings'),
    path('car-listings/list/<int:pk>/', views.car_listing_detail, name='car_listing_detail'),
    
    # Authentication
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('password-reset/<uidb64>/<token>', views.password_reset, name='password_reset'),
    path('email/verify/<uidb64>/<token>/', views.email_verify, name='email_verify'),
    
    # User Profile
    path('profile/', views.profile, name='profile'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('profile/add-listing/', views.add_listing, name='add_listing'),
    path('profile/my-listings/', views.profile_listings, name='profile_listings'),
    path('profile/favourites/', views.profile_favourites, name='favourites'),
    path('profile/compare/', views.compare, name='compare'),
    path('profile/dashboard/', views.dashboard, name='dashboard'),
    path('profile/messages/', views.profile_messages, name='messages'),
]


# URLs

# General
# 1. BASE-URL/ - home page (index.html)
# 2. BASE-URL/about/ - about page (about.html)
# 3. BASE-URL/contact/ - contact page (contact.html)

# Car listings
# 2. BASE-URL/car-listings/list - car listings page (listing-list.html/listing-grid.html)
# 3. BASE-URL/car-listings/list/<int:pk> - car listing detail page (listing-single.html)

# Authentication
# 4. BASE-URL/login/ - login page (login.html)
# 5. BASE-URL/register/ - register page (register.html)
# 6. BASE-URL/password-reset/ - password reset page (password-reset.html)
# 7. BASE-URL/forgot-password/ - forgot password page (forgot-password.html)

# User profile
# 8. BASE-URL/profile/ - user profile page (profile.html)
# 9. BASE-URL/profile/settings/ - user profile settings page (profile-settings.html)
# 10. BASE-URL/profile/add-listing/ - add listing page (add-listing.html)
# 11. BASE-URL/profile/my-listings/ - user listings page (profile-listings.html)
# 12. BASE-URL/profile/favourites/ - user favourites page (profile-favourite.html)
# 13. BASE-URL/profile/compare/ - compare listings page (compare.html)
# 14. BASE-URL/profile/dashboard/ - user dashboard page (dashboard.html)
# 15. BASE-URL/profile/messages/ - user messages page (profile-message.html)
