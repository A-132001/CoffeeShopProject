from django.shortcuts import render,get_object_or_404
from .models import Product
def products(request):
    pro = Product.objects.all()
    name = None
    description = None
    PriceFrom = None
    PriceTo = None
    CaseSensitive = None
    if "CaseSensitive" in request.GET:
        CaseSensitive = request.GET['CaseSensitive']
        if not CaseSensitive:
            CaseSensitive = "off"
    
    if 'SearchName' in request.GET:
        name = request.GET['SearchName']
        if name:
            if CaseSensitive == 'on':
                pro = pro.filter(name__contains=name)
            else:
                pro = pro.filter(name__icontains=name)
            
    if 'SearchDescription' in request.GET:
        description = request.GET['SearchDescription']
        if description:
            if CaseSensitive == "on":
                pro = pro.filter(name__contains=description)
            else:
                pro = pro.filter(name__icontains=description)
            
    if "SearchPriceFrom" in request.GET and "SearchPriceTo" in request.GET:
        PriceFrom = request.GET["SearchPriceFrom"]
        PriceTo = request.GET["SearchPriceTo"]
        if PriceFrom and PriceTo:
            if PriceFrom.isdigit() and PriceTo.isdigit():
                pro = pro.filter(price__gte = PriceFrom,price__lte=PriceTo)
    context = {
        'products': pro
        
    }
    return render(request,'products/products.html',context)

def product(request,pro_id):
    context={
        'pro':get_object_or_404(Product,pk=pro_id)
    }
    return render(request,'products/product.html',context)

def search(request):
    return render(request,'products/search.html')


