# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/categories/', views.category_list, name='category-list'),
    path('api/social-media/', views.social_media_links, name='social_media_links'),
    path('api/products/', views.product_list_api, name='product_list_api'),
    path('api/testimonials/', views.testimonial_list, name='testimonial_list'),
    path('api/banners/', views.banner_api, name='banner_api'),
    path('api/blogs/', views.blog_list, name="blog_list")
]
