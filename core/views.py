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
from .serializers import *
from django.utils.timezone import now

from django.views.decorators.http import require_GET
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from bs4 import BeautifulSoup
from django.http import JsonResponse

# Create your views here.



# Show  image browser
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.utils._os import safe_join
from pathlib import Path
import mimetypes
import os

@staff_member_required
def ckeditor_latest_first(request):
    """
    Custom CKEditor browse view that sorts files by last modified (latest first).
    """
    media_root = settings.MEDIA_ROOT
    ck_path = settings.CKEDITOR_UPLOAD_PATH
    full_path = safe_join(media_root, ck_path)

    files = []
    path = Path(full_path)

    for file in path.glob("**/*"):
        if file.is_file():
            mime_type, _ = mimetypes.guess_type(file.name)
            if mime_type and mime_type.startswith("image/"):
                files.append({
                    'url': settings.MEDIA_URL + ck_path + '/' + file.relative_to(full_path).as_posix(),
                    'name': file.name,
                    'mtime': file.stat().st_mtime,
                })

    # Sort by most recent modification time
    files.sort(key=lambda x: x['mtime'], reverse=True)

    # Paginate (16 items per page like CKEditor default)
    paginator = Paginator(files, 16)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'ckeditor/browse_custom_admin.html', {
        'files': page_obj,
        'page_range': paginator.page_range,
        'page_obj': page_obj,
        'func_num': request.GET.get("CKEditorFuncNum"),
    })


@csrf_exempt
def delete_file(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            file_name = data.get("file_name")  # Expecting relative path like 'uploads/image.jpg'
            if not file_name:
                return JsonResponse({"error": "No file name provided"}, status=400)

            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            print("Trying to delete:", file_path)  # ✅ Debug log

            if os.path.isfile(file_path):
                os.remove(file_path)
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"error": "File not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request."}, status=400)


# def handle_uploaded_file(f):
#     upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
#     os.makedirs(upload_dir, exist_ok=True)
#     save_path = os.path.join(upload_dir, f.name)

#     if os.path.exists(save_path):
#         raise ValueError("A file with this name already exists.")

#     with open(save_path, 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

def handle_uploaded_file(request):
    if request.method == 'POST':
        upload_file = request.FILES.get('file')
        if not upload_file:
            return JsonResponse({'error': 'No file uploaded.'}, status=400)

        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        save_path = os.path.join(upload_dir, upload_file.name)

        # Check if file already exists
        if os.path.exists(save_path):
            return JsonResponse({'error': 'A file with this name already exists.'}, status=409)

        # Save the file
        with open(save_path, 'wb+') as destination:
            for chunk in upload_file.chunks():
                destination.write(chunk)

        return JsonResponse({'success': True, 'filename': upload_file.name})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
# End Browser Image

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

# Start Blog 
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


@api_view(['GET', 'POST'])
@csrf_exempt
def blog_comments(request):
    if request.method == 'GET':
        blog_id = request.GET.get('blog_id')
        if blog_id:
            try:
                blog_id = int(blog_id)
                comments = Comment.objects.filter(blog_id=blog_id, is_active=True).values()
            except ValueError:
                return JsonResponse({"error": "Invalid blog_id"}, status=400)
        else:
            comments = Comment.objects.filter(is_active=True).values()
        return JsonResponse(list(comments), safe=False)

    elif request.method == 'POST':
        try:
            # For application/json
            if request.content_type == "application/json":
                data = json.loads(request.body)
                blog_id = data.get('blog_id')
                name = data.get('name')
                email = data.get('email')
                comment_text = data.get('comment')

            # For form-data or x-www-form-urlencoded
            else:
                blog_id = request.POST.get('blog_id')
                name = request.POST.get('name')
                email = request.POST.get('email')
                comment_text = request.POST.get('comment')

            if not all([blog_id, name, email, comment_text]):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            comment = Comment.objects.create(
                blog_id=blog_id,
                name=name,
                email=email,
                comment=comment_text,
                created_at=timezone.now()
            )

            return JsonResponse({"success": True, "comment_id": comment.id}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
# End Blog


# Start About Page Get APi
@api_view(['GET'])
def get_about_us(request):
    try:
        about = AboutUs.objects.first()
        serializer = AboutUsSerializer(about, context={'request': request})
        return Response(serializer.data)
    except:
        return Response({"error": "About Us content not found."}, status=404)
    
# End About Page


# Start Product Catalogues
@api_view(['GET'])
def product_catalogue_list(request):
    catalogues = ProductCatalogue.objects.all()
    serializer = ProductCatalogueSerializer(catalogues, many=True, context={'request': request})
    return Response(serializer.data)

# End Product Catalogues