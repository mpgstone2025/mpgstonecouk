from django.contrib import admin
from django.utils.html import format_html
from .models import *
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# Register your models here.

admin.site.site_header = "MPGStone.co.uk"
admin.site.site_title = "MPGStone Admin Portal"
admin.site.index_title = "Welcome to MPGStone Admin"


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'is_active')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'category_name', 'slug', 'is_active', 'product_count')  # Added product_count
    list_display_links = ('image_tag', 'category_name')  # Make 'image' and 'name' clickable

    def product_count(self, obj):
        return obj.product.count()
    product_count.short_description = 'Product Count'

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'

