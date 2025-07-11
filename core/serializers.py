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