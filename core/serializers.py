from rest_framework import serializers
from bs4 import BeautifulSoup
from .models import *

def make_image_urls_absolute(html_content, request):
    soup = BeautifulSoup(html_content, "html.parser")
    for img in soup.find_all("img"):
        src = img.get("src")
        if src and src.startswith("/"):
            img["src"] = request.build_absolute_uri(src)
    return str(soup)

# About Page

class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = '__all__'

# End About

# Start Product Catalogues Page
class ProductCatalogueSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductCatalogue
        fields = ['id', 'name', 'thumbnail_url', 'pdf_url']

    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        if obj.thumbnail:
            return request.build_absolute_uri(obj.thumbnail.url)
        return None

    def get_pdf_url(self, obj):
        request = self.context.get('request')
        if obj.pdf_file:
            return request.build_absolute_uri(obj.pdf_file.url)
        return None
    
# End Product Catalogues