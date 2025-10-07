from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('compare', views.CompareListingsView, basename='compare')
router.register('favourites', views.FavouriteListingsView, basename='favourites')
router.register('', views.ProfileView, basename='profile')
router.register('mylistings', views.UserListingsViewSet, basename='user_listings')
router.register('', views.ProfileSettingsViewSet, basename='profile_settings')
router.register('', views.UploadUserProfilePictureView, basename='upload_profile_picture')



urlpatterns = router.urls


app_name = 'userprofile'

""" 
1. endpoint for adding a car to the compare list
2. endpoint for removing a car from the compare list
3. endpoint for viewing the compare list
4. endpoint for clearing the compare list

5. endpoint for user listings
6. endpoint for user profile
7. endpoint for updating user profile
8. endpoint for changing user password
9. endpoint for uploading user image
10. endpoint for removing user image
11. endpoint adding listing to user favorites
12. endpoint for removing listing from user favorites
13. endpoint for viewing user favorites
14. endpoint for getting profile settings
15. endpoint for updating profile settings
16. endpoint for deleting user account

"""