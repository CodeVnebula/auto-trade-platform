from django.urls import path
from django.urls import include
from . import views

app_name = 'car_listing'

urlpatterns = [
    path('cars/', include(
            [
                path('config-data/', views.ConfigData.as_view(), name='config_data'),
                path('manufacturers/<int:make_id>/models', views.CarMakeModelsList.as_view(), name='manufacturer_models'),
            ]
        )
    ),
]