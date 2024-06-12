from django.http import HttpResponse
from django.shortcuts import render

def product(request):
    return render(request, 'goods/product.html')

def catalog(request):
    return render(request, 'goods/catalog.html')
