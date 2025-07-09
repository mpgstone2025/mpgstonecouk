# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/categories/', views.category_list, name='category-list'),
    path('api/social-media/', views.social_media_links, name='social_media_links'),
    path('api/products/', views.product_list_api, name='product_list_api')
    
]
