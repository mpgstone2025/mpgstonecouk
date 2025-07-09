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



class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1

class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductAttributeInline, ProductGalleryInline]
    list_display = ('id', 'image_tag', 'name', 'category', 'short_description')  # 👈 Add image_tag here
    list_display_links = ('image_tag', 'name')  # Make 'id' and 'name' clickable
    search_fields = ('name', 'description')
    list_filter = ['category']
    ordering = ('-id',)
    list_per_page = 50

    def image_tag(self, obj):
        if obj.image:  # assuming your model has an ImageField named `image`
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'  # 👈 This will set the column name to 'Image'

    def short_description(self, obj):
        # Assuming 'description' is a field in the model and is a string
        words = obj.description.split()[:20]  # Split the description into words and take the first 20
        return ' '.join(words)  # Join the words back into a string
    short_description.short_description = 'Description' 

