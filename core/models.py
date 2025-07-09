from django.db import models
# from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from django.utils.timezone import now
from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.html import format_html

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
    og_title = models.CharField(max_length=255, blank=True, null=True)
    og_description = models.TextField(blank=True, null=True)
    twitter_title = models.CharField(max_length=255, blank=True, null=True)
    twitter_description = models.TextField(blank=True, null=True)

    meta_keywords = models.TextField(blank=True, null=True) 
    canonical_url = models.URLField(blank=True, null=True)   
    robots_tag = models.CharField(max_length=255, default="INDEX, FOLLOW, MAX-IMAGE-PREVIEW:LARGE, MAX-SNIPPET:-1, MAX-VIDEO-PREVIEW:-1")
    publisher = models.CharField(max_length=255, blank=True, null=True)  

    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('category_name',)

    def __str__(self):
        return self.category_name 