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


def category_list(request):
    categories = Category.objects.filter(is_active=True)
    data = []

    for category in categories:
        data.append({
            "id": category.id,
            "category_name": category.category_name,
            "slug": category.slug,
            "alt_text" : category.alt_text,
            "meta_title": category.meta_title,
            "meta_description": category.meta_description,
            "meta_image": request.build_absolute_uri(category.meta_image.url) if category.meta_image else None,  # ✅ added
            "og_title": category.og_title,
            "og_decriptions": category.og_description,
            "twitter_title": category.og_title,
            "twitter_decriptions": category.og_description,
            "meta_keywords": category.meta_keywords,
            "canonical_url": category.canonical_url,
            "robots_tag": category.robots_tag,
            "publisher" : category.publisher,
            "image": request.build_absolute_uri(category.image.url) if category.image else None,
            "short_description" : category.short_description,
            "descriptions" : category.description,
            "schema_markup" : category.schema_markup,
            "is_active": category.is_active
        })

    return JsonResponse(data, safe=False)


@require_GET
def product_list_api(request):
    category_name = request.GET.get('category')
    slug = request.GET.get('slug')  # updated to match URL param
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
            "alt_text" : product.alt_text,
            "category": product.category.category_name,
            "descriptions": product.description,
            "meta_title": product.meta_title,
            "meta_description": product.meta_description,
            "meta_image": request.build_absolute_uri(product.meta_image.url) if product.meta_image else None,  # ✅ added
            "og_title": product.og_title,
            "og_decriptions": product.og_description,
            "twitter_title": product.og_title,
            "twitter_decriptions": product.og_description,
            "meta_keywords": product.meta_keywords,
            "canonical_url": product.canonical_url,
            "robots_tag": product.robots_tag,
            "publisher" : product.publisher,
            "attributes": attributes,
            "gallery_images": gallery,
        })

    return JsonResponse(data, safe=False)

