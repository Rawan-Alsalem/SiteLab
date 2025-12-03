from django.urls import path
from . import views

app_name="contact"

urlpatterns = [
    path('', views.contact_view, name='contact_view'),
    path('admin/messages/', views.contact_messages_view, name='contact_messages_view'),
]