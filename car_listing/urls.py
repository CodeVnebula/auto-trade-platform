from django.urls import path
from django.urls import include
from . import views

app_name = 'car_listing'

urlpatterns = [
    path('car-listings/', include(
            [   
                path('list/<int:pk>/delete/', views.CarListingDeleteView.as_view(), name='delete_car_listing'),
                path('list/', views.CarListingListView.as_view(), name='list_car_listings'),
                path('list/<int:pk>', views.CarListingDetailView.as_view(), name='list_car_listings'),
                path('config-data/', views.ConfigData.as_view(), name='config_data'),
                path('manufacturers/models/<int:make_id>', views.CarMakeModelsList.as_view(), name='manufacturer_models'),
                path('create/', views.CarListingCreateView.as_view(), name='create_car_listing'),
                path('upload-photos/<int:listing_id>', views.UploadCarListingPhotosView.as_view(), name='upload_photos'),
                path('upload/', views.Template.as_view(), name='upload_photos_template'),
                path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car-detail'),
            ]
        )
    ),
]