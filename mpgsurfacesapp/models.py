from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class PageMeta(models.Model):
    PAGE_CHOICES = [
        ('products', 'Products'),
        ('about', 'About Us'),
        ('contact', 'Contact Us'),
        ('terms', 'Terms & Conditions'),
        ('privacy', 'Privacy Policy'),
        ('catalogue', 'Product Catalogue'),
        ('category', 'Category'),
        ('blogs', 'Blogs'),
    ]

    page = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)
    
    # Meta tags
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    meta_image = models.ImageField(upload_to='pages/meta_images/', blank=True, null=True)
    # Open Graph
    og_title = models.CharField(max_length=255, blank=True, null=True)
    og_description = models.TextField(blank=True, null=True)

    # Twitter
    twitter_title = models.CharField(max_length=255, blank=True, null=True)
    twitter_description = models.TextField(blank=True, null=True)

    # SEO & Robots
    meta_keywords = models.TextField(blank=True, null=True)
    canonical_url = models.URLField(blank=True, null=True)
    robots_tag = models.CharField(
        max_length=255,
        default="INDEX, FOLLOW, MAX-IMAGE-PREVIEW:LARGE, MAX-SNIPPET:-1, MAX-VIDEO-PREVIEW:-1"
    )

    # Optional
    publisher = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return dict(self.PAGE_CHOICES).get(self.page, self.page)
    
# End