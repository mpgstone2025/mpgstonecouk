# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),    
    path('ckeditor/custom-browse/', views.ckeditor_latest_first, name='ckeditor_custom_browse'),
    path("delete-file/", views.delete_file, name="delete_file"),
    path('api/banners/', views.banner_api, name='banner_api'),
    path('api/about-us/', views.get_about_us, name='about-us'),
    path('api/categories/', views.category_list, name='category-list'),
    path('api/social-media/', views.social_media_links, name='social_media_links'),
    path('api/products/', views.product_list_api, name='product_list_api'),
    path('api/testimonials/', views.testimonial_list, name='testimonial_list'),
    path('api/blogs/', views.blog_list, name="blog_list"),
    path('api/comments/', views.blog_comments, name="blog_comment"),
    path('api/catalogues/', views.product_catalogue_list, name='product_catalogue_list'),

]
