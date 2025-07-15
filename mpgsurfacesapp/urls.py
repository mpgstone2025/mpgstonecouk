# mpgsurfacesapp/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('api/products/', product_list_api, name='product-list-api'),
]
