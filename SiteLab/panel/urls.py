from django.urls import path
from . import views

app_name = 'panel'

urlpatterns = [
    path('', views.panel_view, name='panel_view'),
    path('add/review/', views.add_review, name="add_review"),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('request/delete/<int:request_id>/', views.delete_custom_request, name='delete_custom_request'),
    path('portfolio/delete/', views.delete_portfolio, name='delete_portfolio'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('custom/delete/<int:request_id>/', views.delete_custom_request, name='delete_custom_request'),


]
