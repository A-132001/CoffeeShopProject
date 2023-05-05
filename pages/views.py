from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product
def index(request):
    context = {
            'products':Product.objects.all
        }
    return render(request,'pages/index.html',context)

def about(request):
    return render(request,'pages/about.html')


def coffee(request):
    return render(request, 'pages/coffee.html')