from django.shortcuts import render,redirect
from django.contrib import messages
from django.utils import timezone
from products.models import Product
from .models import Order,OrderDetails,Payment

def add_to_cart(request):
    if 'pro_id' in request.GET and 'price' in request.GET and 'quantity' in request.GET\
    and request.user.is_authenticated and not request.user.is_anonymous:
        pro_id = request.GET['pro_id']
        qty = request.GET['quantity']
        
        
        # check if user enter correct product id
        if not Product.objects.all().filter(id=pro_id).exists():
            return redirect('products')
        
        # get product from database
        pro = Product.objects.get(id=pro_id)
        
        # to check if user create new details order or complete old order
        order = Order.objects.all().filter(user=request.user,is_finished=False)
        if order:
            old_order = Order.objects.get(user=request.user,is_finished = False)
            if OrderDetails.objects.all().filter(order=old_order,product=pro).exists():
                order_details = OrderDetails.objects.get(order=old_order,product=pro)
                order_details.quantity += int(qty)
                order_details.save()
            else:
                order_details = OrderDetails.objects.create(order = old_order,product = pro,
                    price = pro.price , quantity = qty)
            messages.success(request,'This product added to old order')
        else:
            new_order = Order(user=request.user,order_date=timezone.now(),is_finished=False)
            new_order.save()
            order_details = OrderDetails.objects.create(order = new_order,product = pro,
                price = pro.price , quantity = qty)
            messages.success(request,'You start new order')
            
               
        return redirect('/products/'+request.GET['pro_id'])
    else:
        if 'pro_id' in request.GET:
            messages.error(request,"You Must log in")
            return redirect('/products/'+request.GET['pro_id'])
        else:
            return redirect('products')


def cart(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user,is_finished=False):
            
            order =  Order.objects.get(user=request.user,is_finished=False)
            order_details = OrderDetails.objects.all().filter(order=order)
            total =  0
            for sub in order_details:
                total += sub.price * sub.quantity
            
            context ={
                'order':order,
                'order_details':order_details,
                'total':total
            }
    
    
    return render(request,'orders/cart.html',context)


def remove_from_cart(request,orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id == request.user.id:
            orderdetails.delete()
    return redirect('cart')


def add_qty(request,orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id == request.user.id:
            orderdetails.quantity += 1
            orderdetails.save()
    return redirect('cart')
    
def sub_qty(request,orderdetails_id):
    orderdetails = OrderDetails.objects.get(id=orderdetails_id)
    if orderdetails.quantity > 1 and orderdetails.order.user.id == request.user.id:
        orderdetails.quantity -= 1
        orderdetails.save()
        
    return redirect('cart')


def payment(request):
    context = None
    if request.method == 'POST' and 'btnpayment' in request.POST and\
        'address' in request.POST and 'phone' in request.POST and\
        'card_number' in request.POST and 'expire' in request.POST\
         and 'security_code' in request.POST:
        address = request.POST['address']        
        phone = request.POST['phone']        
        card_number = request.POST['card_number']        
        expire = request.POST['expire']        
        security_code = request.POST['security_code']
        is_added = False
        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user,is_finished=False):
                order =  Order.objects.get(user=request.user,is_finished=False)
                payment = Payment(order=order,address = address,phone=phone,card_number=card_number,expire=expire,security_code=security_code)
                payment.save()
                order.is_finished = True
                order.save()         
                is_added = True
                messages.success(request,"Your payment proccess is successful")
                
        context = {
            'address':address,
            'phone':phone,
            'card_number':card_number,
            'expire':expire,
            'security_code':security_code,
            "is_added":is_added
        }
    
    else:
        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user,is_finished=False):
                
                order =  Order.objects.get(user=request.user,is_finished=False)
                order_details = OrderDetails.objects.all().filter(order=order)
                total =  0
                for sub in order_details:
                    total += sub.price * sub.quantity
                
                context ={
                    'order':order,
                    'order_details':order_details,
                    'total':total
                }
                
    return render(request,'orders/payment.html',context)


def show_orders(request):
    context = None
    all_orders = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        all_orders =  Order.objects.all().filter(user=request.user)
        for order in all_orders:
            # 
            order_details = OrderDetails.objects.all().filter(order=order)
            total =  0
            count = 0
            for sub in order_details:
                total += sub.price * sub.quantity
                count +=1
            order.count = count
            order.total = total
                
                
    context={
        'all_orders':all_orders
    }
    return render(request,'orders/show_orders.html',context)