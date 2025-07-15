from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from django.utils.timezone import now
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.html import format_html
from django.conf import settings
from django.urls import reverse
from django.utils.html import mark_safe

from tinymce.models import HTMLField
# Create your models here.

# Start Banner Section Model
class Banner(models.Model):
    title = models.CharField(max_length=255, help_text="Main title text for the banner.")
    subtitle = models.CharField(max_length=255, blank=True, null=True, help_text="Subtitle or supporting text.")
    image = models.ImageField(
        upload_to='banners/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
        help_text="Upload a banner image (JPG, PNG, WEBP)."
    )
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    enquiry_button_text = models.CharField(max_length=100, default='Enquire Now', help_text="Text shown on the enquiry button..")

    def __str__(self):
        return self.title or "Banner" 
    
# End Banner Section

# Start Socialmedia Section Model
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

# Start Category Model
class Category(models.Model):
    category_name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=191, unique=True, blank=True)
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

# End Category Model

# Start Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=191, unique=True, blank=True, null=True) # example slug field
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

     # New field for schema markup
    schema_markup = models.TextField(blank=True, null=True, help_text="Add custom JSON-LD schema here")

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
    
# End Product Model

# Start Testimonial Model
class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    verified = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.PositiveIntegerField(default=5)
    title = models.CharField(max_length=255)
    testimonial = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.title}" 
    

# End Testimonial model

# Start Blog Model
class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    content = RichTextUploadingField()  # ✅ Image upload supported
    image = models.ImageField(upload_to='blog_images/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    # category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='blogs', blank=True)
    meta_title = models.CharField(max_length=255, help_text="Meta title for SEO", blank=True)
    meta_description = models.TextField(help_text="Meta description for SEO", blank=True)
    meta_image = models.ImageField(upload_to='blog_images/meta_image/', blank=True, null=True)
    og_title = models.CharField(max_length=255, blank=True, null=True)
    og_description = models.TextField(blank=True, null=True)
    twitter_title = models.CharField(max_length=255, blank=True, null=True)
    twitter_description = models.TextField(blank=True, null=True)

    meta_keywords = models.TextField(blank=True, null=True) 
    canonical_url = models.URLField(blank=True, null=True)   
    robots_tag = models.CharField(max_length=255, default="INDEX, FOLLOW, MAX-IMAGE-PREVIEW:LARGE, MAX-SNIPPET:-1, MAX-VIDEO-PREVIEW:-1")
    publisher = models.CharField(max_length=255, blank=True, null=True)  
    date_posted = models.DateTimeField(default=now)
    # total_views = models.PositiveIntegerField(default=0)

     # New field for schema markup
    schema_markup = models.TextField(blank=True, null=True, help_text="Add custom JSON-LD schema here")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)  # Comment moderation

    def __str__(self):
        return f"Comment by {self.name} on {self.blog.title}"
    
# End Blog Model 



from django.db import models

# Start About Page
class AboutUs(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    image_1 = models.ImageField(upload_to='about/', null=True, blank=True)
    image_1_alt = models.CharField(max_length=255, blank=True, help_text="Alt text for image 1")

    image_2 = models.ImageField(upload_to='about/', null=True, blank=True)
    image_2_alt = models.CharField(max_length=255, blank=True, help_text="Alt text for image 2")

    image_3 = models.ImageField(upload_to='about/', null=True, blank=True)
    image_3_alt = models.CharField(max_length=255, blank=True, help_text="Alt text for image 3")

    image_4 = models.ImageField(upload_to='about/', null=True, blank=True)
    image_4_alt = models.CharField(max_length=255, blank=True, help_text="Alt text for image 4")

    image_5 = models.ImageField(upload_to='about/', null=True, blank=True)
    image_5_alt = models.CharField(max_length=255, blank=True, help_text="Alt text for image 5")

    
    mission = models.TextField()
    mission_image = models.ImageField(upload_to='about/', null=True, blank=True)
    mission_image_alt = models.CharField(max_length=255, blank=True)

    vision = models.TextField()
    vision_image = models.ImageField(upload_to='about/', null=True, blank=True)
    vision_image_alt = models.CharField(max_length=255, blank=True)

    values = models.TextField()
    values_image = models.ImageField(upload_to='about/', null=True, blank=True)
    values_image_alt = models.CharField(max_length=255, blank=True)

    philosophy = models.TextField()
    philosophy_image = models.ImageField(upload_to='about/', null=True, blank=True)
    philosophy_image_alt = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

    def __str__(self):
        return self.title

# End About Page

# Start Product Catalogues
class ProductCatalogue(models.Model):
    name = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='catalogue_thumbnails/')
    pdf_file = models.FileField(upload_to='catalogue_pdfs/')

    def __str__(self):
        return self.name

    def thumbnail_tag(self):
        if self.thumbnail:
            return format_html('<img src="{}" width="100" height="auto" />', self.thumbnail.url)
        return "(No image)"

    def pdf_link(self):
        if self.pdf_file:
            return format_html('<a href="{}" target="_blank">Download PDF</a>', self.pdf_file.url)
        return "(No file)"

    thumbnail_tag.short_description = "Thumbnail"
    pdf_link.short_description = "PDF File"

# End Product Catalogues


# Start Legal Pages
class LegalstaticPage(models.Model):
    PAGE_CHOICES = [
        ('terms', 'Terms & Conditions'),
        ('privacy', 'Privacy Policy'),
        ('cookies', 'Cookies Policy'),
    ]

    page_type = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)
    title = models.CharField(max_length=255)
    content = RichTextUploadingField()

    def __str__(self):
        return self.get_page_type_display()
    
# End Legal Page

# Start Home page relate SEO Field

# class HomePageContent(models.Model):
#     title = models.CharField(max_length=255)
#     content = RichTextUploadingField()
#     # SEO fields
#     meta_title = models.CharField(max_length=255, blank=True, null=True)
#     meta_description = models.TextField(blank=True, null=True)
#     meta_image = models.ImageField(upload_to='homepage/meta_images/', blank=True, null=True)
#     og_title = models.CharField(max_length=255, blank=True, null=True)
#     og_description = models.TextField(blank=True, null=True)
#     twitter_title = models.CharField(max_length=255, blank=True, null=True)
#     twitter_description = models.TextField(blank=True, null=True)

#     meta_keywords = models.TextField(blank=True, null=True) 
#     canonical_url = models.URLField(blank=True, null=True)   
#     robots_tag = models.CharField(max_length=255, default="INDEX, FOLLOW, MAX-IMAGE-PREVIEW:LARGE, MAX-SNIPPET:-1, MAX-VIDEO-PREVIEW:-1")
#     publisher = models.CharField(max_length=255, blank=True, null=True)  

#     schemas = models.ManyToManyField(SchemaBlock, blank=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title