from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# mpgsurfacesapp/views.py


# mpgsurfacesapp/views.py

from django.http import JsonResponse
from .models import Product

def product_list_api(request):
    products = Product.objects.all()
    data = [
        {
            'id': product.id,
            'name': product.name,
            'price': str(product.price),  # DecimalField needs str() for JSON
        }
        for product in products
    ]
    return JsonResponse({'products': data})

