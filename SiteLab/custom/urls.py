from django.urls import path
from . import views

app_name = "custom"

urlpatterns = [
    path("new/request/", views.create_request_view, name="create_request_view"),
    path("my/requests/", views.my_requests_view, name="my_requests_view"),
    path("detail/<int:pk>/", views.request_detail_view, name="request_detail_view"),
    path("pay/<int:pk>/", views.process_payment_view, name="process_payment_view"),
    path("edit/<int:pk>/", views.edit_request_view, name="edit_request_view"),
    path('admin/requests/', views.admin_requests_view, name='admin_requests_view'),
    path('admin/requests/update/<int:pk>/', views.update_status_view, name='update_status_view'),
    path('admin/requests/delete/<int:pk>/', views.delete_request_view, name='delete_request_view'),
]