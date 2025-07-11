from django.shortcuts import render, HttpResponse
from .models import *
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, generics
from django.views.decorators.csrf import csrf_exempt
# from .serializers import ProductReviewSerializer
# from  core.serializers import ProductSerializer, ProductReviewSerializer

from rest_framework.views import APIView
# from .serializers import ReviewSerializer, ContactMessageSerializer, ContactDetailSerializer, LegalPageSerializer, HomePageContentSerializer, PageMetaSerializer
from django.utils.timezone import now

from django.views.decorators.http import require_GET
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from bs4 import BeautifulSoup
from django.http import JsonResponse

# Create your views here.

# Start code This code fetch complte image url
def make_image_urls_absolute(html_content, request):
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, "html.parser")
    for img in soup.find_all("img"):
        src = img.get("src")
        if src and src.startswith("/"):
            img["src"] = request.build_absolute_uri(src)
    return str(soup)
# End code

def home(request):
    return render(request, 'home.html')

def social_media_links(request):
    links = SocialMediaLink.objects.all()
    link_data = []

    for link in links:
        link_data.append({
            "id": link.id,
            "platform": link.platform,
            "iconclass" : link.icon_class,
            "url": link.url if hasattr(link, 'url') else None  # Add this field in your model if needed
            
        })

    response = {
        "current_time": now().strftime("%Y-%m-%d %H:%M:%S"),
        "social_media_links": link_data
    }

    return JsonResponse(response)

# Category API
def category_list(request):
    categories = Category.objects.filter(is_active=True)
    data = []

    for category in categories:
        description_html = make_image_urls_absolute(category.description, request)

        data.append({
            "id": category.id,
            "category_name": category.category_name,
            "slug": category.slug,
            "alt_text": category.alt_text,
            "meta_title": category.meta_title,
            "meta_description": category.meta_description,
            "meta_image": request.build_absolute_uri(category.meta_image.url) if category.meta_image else None,
            "og_title": category.og_title,
            "og_decriptions": category.og_description,
            "twitter_title": category.og_title,
            "twitter_decriptions": category.og_description,
            "meta_keywords": category.meta_keywords,
            "canonical_url": category.canonical_url,
            "robots_tag": category.robots_tag,
            "publisher": category.publisher,
            "image": request.build_absolute_uri(category.image.url) if category.image else None,
            "short_description": category.short_description,
            "descriptions": description_html,  # ✅ updated with absolute image URLs
            "schema_markup": category.schema_markup,
            "is_active": category.is_active
        })

    return JsonResponse(data, safe=False)
# End Category API

# Product API

# def make_image_urls_absolute(html_content, request):
#     if not html_content:
#         return ""
#     soup = BeautifulSoup(html_content, "html.parser")
#     for img in soup.find_all("img"):
#         src = img.get("src")
#         if src and src.startswith("/"):
#             img["src"] = request.build_absolute_uri(src)
#     return str(soup)


@require_GET
def product_list_api(request):
    category_name = request.GET.get('category')
    slug = request.GET.get('slug')
    limit = request.GET.get('limit')

    products = Product.objects.all()

    if slug:
        products = products.filter(slug=slug)

    if category_name:
        products = products.filter(category__category_name__iexact=category_name)

    if limit:
        try:
            limit = int(limit)
            products = products[:limit]
        except ValueError:
            pass  # Ignore invalid limit values

    data = []
    for product in products:
        image_url = request.build_absolute_uri(product.image.url) if product.image else None
        description = make_image_urls_absolute(product.description, request)

        attributes = [
            {"title": attr.title, "value": attr.value}
            for attr in product.attributes.all()
        ]

        gallery = [
            {
                "image": request.build_absolute_uri(img.image.url),
                "alt_text": img.alt_text
            }
            for img in product.gallery_images.all()
        ]

        data.append({
            "id": product.id,
            "name": product.name,
            "slug": product.slug,
            "image": image_url,
            "alt_text": product.alt_text,
            "category": product.category.category_name,
            "descriptions": description,
            "meta_title": product.meta_title,
            "meta_description": product.meta_description,
            "meta_image": request.build_absolute_uri(product.meta_image.url) if product.meta_image else None,
            "og_title": product.og_title,
            "og_decriptions": product.og_description,
            "twitter_title": product.og_title,
            "twitter_decriptions": product.og_description,
            "meta_keywords": product.meta_keywords,
            "canonical_url": product.canonical_url,
            "robots_tag": product.robots_tag,
            "publisher": product.publisher,
            "attributes": attributes,
            "gallery_images": gallery,
            "schema_markup" : product.schema_markup,
        })

    return JsonResponse(data, safe=False)



def testimonial_list(request):
    testimonials = Testimonial.objects.all()
    testimonial_data = []

    for t in testimonials:
        image_url = request.build_absolute_uri(t.profile_image.url) if t.profile_image else None
        testimonial_data.append({
            "id": t.id,
            "name": t.name,
            "verified": t.verified,
            "profile_image": image_url,
            "rating": t.rating,
            "title": t.title,
            "testimonial": t.testimonial
        })

    response = {
        "current_time": now().strftime("%Y-%m-%d %H:%M:%S"),
        "testimonials": testimonial_data
    }

    return JsonResponse(response)


def banner_api(request):
    banners = Banner.objects.all()
    data = []

    for banner in banners:
        image_url = request.build_absolute_uri(banner.image.url) if banner.image else None

        data.append({
            "id": banner.id,
            "title": banner.title,
            "subtitle": banner.subtitle,
            "image": image_url,
            "alt_text" : banner.alt_text,
            "enquiry_button_text": banner.enquiry_button_text,
        })

    return JsonResponse(data, safe=False)


def blog_list(request):
    blogs = Blog.objects.all()
    blog_data = []

    for blog in blogs:
        image_url = request.build_absolute_uri(blog.image.url) if blog.image else None

         # Process content to convert <img src="/media/..."> to full URLs
        soup = BeautifulSoup(blog.content, 'html.parser')
        for img in soup.find_all('img'):
            src = img.get('src')
            if src and src.startswith('/'):
                img['src'] = request.build_absolute_uri(src)

        blog_data.append({
            "id": blog.id,
            "title": blog.title,
            "slug": blog.slug,
            "description": blog.description,
            "content": str(soup),
            "image": image_url,
            "alt_text" : blog.alt_text,
            "meta_title": blog.meta_title,
            "meta_description": blog.meta_description,
            "meta_image": request.build_absolute_uri(blog.meta_image.url) if blog.meta_image else None,  # ✅ added
            "og_title": blog.og_title,
            "og_decriptions": blog.og_description,
            "twitter_title": blog.og_title,
            "twitter_decriptions": blog.og_description,
            "meta_keywords": blog.meta_keywords,
            "canonical_url": blog.canonical_url,
            "robots_tag": blog.robots_tag,
            "publisher" : blog.publisher,
            "schema_markup" : blog.schema_markup,
            "date_posted": blog.date_posted.strftime("%Y-%m-%d %H:%M:%S") if blog.date_posted else None
        })

    response = {
        "current_time": now().strftime("%Y-%m-%d %H:%M:%S"),
        "blogs": blog_data
    }

    return JsonResponse(response)