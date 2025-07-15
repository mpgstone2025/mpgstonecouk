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


# Start Social Media Admin dashboard 
@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'is_active')
# End Social Media Admin dashboard 
 
 # Start Category Admin dashboard 
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

 # End Category Admin dashboard 

 # Start Product Admin dashboard 
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


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'display_rating', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'email', 'comment')

    def display_rating(self, obj):
        return '★' * obj.rating + '☆' * (5 - obj.rating)
    display_rating.short_description = 'Rating'

# End Product Admin dashboard 

 # Start Testimonials Admin dashboard 
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'verified', 'rating')
    list_filter = ('verified', 'rating')
    search_fields = ('name', 'title', 'testimonial')
    readonly_fields = ('profile_image_preview',)
    fields = ('name', 'verified', 'profile_image', 'profile_image_preview', 'rating', 'title', 'testimonial')
    
    def profile_image_preview(self, obj):
        if obj.profile_image:
            return mark_safe(f'<img src="{obj.profile_image.url}" width="100" height="100" style="object-fit:cover; border-radius:8px;" />')
        return "No image"

    profile_image_preview.short_description = 'Image Preview'

# End Testimonials Admin dashboard 

# Start Banner Admin dashboard 
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'enquiry_button_text')
    search_fields = ('title', 'subtitle', 'alt_text')
    list_filter = ('title',)
    readonly_fields = ()

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'subtitle',
                'image',
                'alt_text',
                'enquiry_button_text',
            )
        }),
    )

# End Banner Admin dashboard 


# Start Blog Admin dashboard 

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'date_posted', 'preview_image', 'meta_title', 'publisher')
    list_filter = ('date_posted',)
    search_fields = ('title', 'slug', 'description', 'meta_title', 'meta_description', 'meta_keywords')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('date_posted',)
    ordering = ('-date_posted',)

    fieldsets = (
        ('Main Content', {
            'fields': ('title', 'slug', 'description', 'content', 'image', 'alt_text')
        }),
        ('SEO Settings', {
            'classes': ('collapse',),
            'fields': (
                'meta_title', 'meta_description', 'meta_keywords',
                'canonical_url', 'robots_tag', 'meta_image'
            )
        }),
        ('Open Graph / Twitter Card', {
            'classes': ('collapse',),
            'fields': (
                'og_title', 'og_description',
                'twitter_title', 'twitter_description',
            )
        }),
        ('Schema Markup (JSON-LD)', {
            'classes': ('collapse',),
            'fields': ('schema_markup',),
        }),
        ('Metadata', {
            'fields': ('publisher', 'date_posted')
        }),
    )

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return "-"
    preview_image.short_description = 'Image'


@admin.register(Comment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'blog', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at', 'blog')
    search_fields = ('name', 'email', 'comment')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_active=True)
    approve_comments.short_description = "Mark selected comments as active"

# End Blog Admin dashboard 

# Start About Page Admin dashboard 
@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title',)
# End

# Start Product Catalogues
@admin.register(ProductCatalogue)
class ProductCatalogueAdmin(admin.ModelAdmin):
    list_display = ('name', 'thumbnail_tag', 'pdf_link')
    readonly_fields = ('thumbnail_tag', 'pdf_link')
# End

# Start Legal Page
@admin.register(LegalstaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ('page_type', 'title')
    search_fields = ('title', 'page_type')

