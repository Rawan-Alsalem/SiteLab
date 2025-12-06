from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('our-services/', views.our_services, name='our_services'),
    path('reviews/', views.all_reviews, name='all_reviews'),
]
