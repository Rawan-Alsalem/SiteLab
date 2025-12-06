from django.urls import path
from . import views

app_name = 'portfolios'

urlpatterns = [
    path('portfolio-add/', views.portfolio_add, name='portfolio_add'),
    path('portfolio-edit/', views.portfolio_edit, name='portfolio_edit'),
    path('publish-success/', views.portfolio_published, name='publish_success'),    path('preview/', views.preview_view, name='preview_view'), 
    path('published/<str:username>/', views.published_view, name='published_view'),
    path('portfolio_template1/', views.template1_view, name='template1_view'),
    path('portfolio_template2/', views.template2_view, name='template2_view'),
    path('portfolio_template3/', views.template3_view, name='template3_view'),
    path('portfolio_template4/', views.template4_view, name='template4_view'),
]