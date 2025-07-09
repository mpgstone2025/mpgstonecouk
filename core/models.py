from django.db import models
# from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from django.utils.timezone import now
from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.html import format_html
from django.conf import settings
from django.urls import reverse
from django.utils.html import mark_safe
# Create your models here.

class SocialMediaLink(models.Model):
    
    platform = models.CharField(max_length=50, choices=[
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('pinterest', 'Pinterest'),
        ('other', 'Other'),
    ])
    url = models.URLField(max_length=200, unique=True, blank=True)

    icon_class = models.CharField(max_length=100, blank=True, null=True)  # Font Awesome or custom icon classes
    is_active = models.BooleanField(default=True)  

    class Meta:
        ordering = ['platform']

class Category(models.Model):
    category_name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    short_description = models.TextField(blank=True, null=True)
    description = RichTextField(blank=True, null=True)  # <-- CKEditor field

    # SEO fields
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_image = models.ImageField(upload_to='categories/meta_images/', null=True, blank=True)
    og_title = models.CharField(max_length=255, blank=True, null=True)
    og_description = models.TextField(blank=True, null=True)
    twitter_title = models.CharField(max_length=255, blank=True, null=True)
    twitter_description = models.TextField(blank=True, null=True)

    meta_keywords = models.TextField(blank=True, null=True)
    canonical_url = models.URLField(blank=True, null=True)
    robots_tag = models.CharField(
        max_length=255,
        default="INDEX, FOLLOW, MAX-IMAGE-PREVIEW:LARGE, MAX-SNIPPET:-1, MAX-VIDEO-PREVIEW:-1"
    )
    publisher = models.CharField(max_length=255, blank=True, null=True)

    # Schema field
    schema_markup = models.TextField(blank=True, null=True, help_text="Paste JSON-LD schema markup here")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('category_name',)

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="100" height="auto" />')
        return "No Image"

    image_tag.short_description = 'Image Preview'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)

        # Automatically generate canonical_url if it's not already set
        if not self.canonical_url and self.slug:
            self.canonical_url = f"{settings.SITE_DOMAIN}/product-category/{self.slug}/"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name 
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True) # example slug field
    category = models.ForeignKey(Category,related_name='product', on_delete= models.CASCADE)
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    description = RichTextField(blank=True, null=True)

    # SEO fields
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_image = models.ImageField(upload_to='products/meta_image/', blank=True, null=True)
    og_title = models.CharField(max_length=255, blank=True, null=True)
    og_description = models.TextField(blank=True, null=True)
    twitter_title = models.CharField(max_length=255, blank=True, null=True)
    twitter_description = models.TextField(blank=True, null=True)

    meta_keywords = models.TextField(blank=True, null=True) 
    canonical_url = models.URLField(blank=True, null=True)   
    robots_tag = models.CharField(max_length=255, default="INDEX, FOLLOW, MAX-IMAGE-PREVIEW:LARGE, MAX-SNIPPET:-1, MAX-VIDEO-PREVIEW:-1")
    publisher = models.CharField(max_length=255, blank=True, null=True)  

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Save first to ensure slug and ID are available
        super().save(*args, **kwargs)

        # Only set canonical_url if it hasn't been set yet and category exists
        if not self.canonical_url and self.category and self.slug:
            self.canonical_url = f"{settings.SITE_DOMAIN}/product-category/{self.category.slug}/{self.slug}/"
            # Save again to update canonical_url
            super().save(update_fields=["canonical_url"])

    def __str__(self):
        return self.name
    

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.alt_text or 'Gallery Image'}"
    

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)  # Inactive by default

    def __str__(self):
        return f"Review by {self.name} on {self.product.name}"
    

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, related_name='attributes', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)  # e.g. Materials, Application
    value = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.product.name}"