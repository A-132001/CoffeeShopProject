from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
import re
from django.contrib import auth
from products.models import Product
def signin(request):
    if request.method == "POST" and 'btnsignin' in request.POST:
        username = request.POST['UserName']
        password = request.POST['Password']
        user = auth.authenticate(username=username,password=password) 
        if user != None:
            if 'RememberMe' not in request.POST:
                request.session.set_expiry(0)
            auth.login(request,user)
        else:
            messages.error(request,'Username or password not vaild')

        
    return render(request,'accounts/signin.html')

def logout(request):
    auth.logout(request)
    return redirect('index')
    
    
def signup(request):
    if request.method == "POST" and 'btnsignup' in request.POST:
        # define my varibles
        fname = None
        lname = None
        address1 = None
        address2 = None
        city = None
        zip = None
        state = None
        email = None
        username = None
        password = None
        agree = None
        is_added = None
        # check if fileds in request
        if 'FirstName'  in request.POST:fname = request.POST['FirstName']
        else:
            messages.error(request,"Error in your first name")
        if 'LastName'  in request.POST:lname = request.POST['LastName']
        else:
            messages.error(request,"Error in your last name")
        if 'Address1'  in request.POST:address1 = request.POST['Address1']
        else:
            messages.error(request,"Error in your address1 ")
        if 'Address2'  in request.POST:address2 = request.POST['Address2']
        else:
            messages.error(request,"Error in your address2 ")
        if 'City'  in request.POST:city = request.POST['City']
        else:
            messages.error(request,"Error in your city ")
        if 'State'  in request.POST:state = request.POST['State']
        else:
            messages.error(request,"Error in your State ")
        if 'Zip'  in request.POST:zip = request.POST['Zip']
        else:
            messages.error(request,"Error in your zip number")
        if 'Email'  in request.POST:email = request.POST['Email']
        else:
            messages.error(request,"Error in your email")
        if 'UserName'  in request.POST:username = request.POST['UserName']
        else:
            messages.error(request,"Error in your username")
        if 'Password'  in request.POST:password = request.POST['Password']
        else:
            messages.error(request,"Error in your password")
        if 'Agree'  in request.POST:agree = request.POST['Agree']
        
        if fname and lname and address1 and address2 and city and state and zip\
        and username and password and email:
            if agree == 'on':
                if User.objects.filter(username=username).exists():
                    messages.error(request,"This username is exists")
                else:
                    if User.objects.filter(email=email).exists():
                       messages.error(request,"This email is exists")
                    else:
                        pattern = "^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$"
                        if re.match(pattern,email):
                            user = User.objects.create_user(first_name=fname,last_name =lname,
                                                            password=password,email=email,
                                                            username=username)
                            user.save()
                            userprofile = UserProfile(user=user,address1 = address1 ,
                                                    address2=address2,
                                                    zip_number = zip,
                                                    city= city,state=state)
                            userprofile.save()
                            # clear the fileds in form
                            fname=lname=address1=address1=city=state=zip=username=password=email=''
                            
                            messages.success(request,"Your account is created successfully")
                            is_added = True
                        else:
                            messages.error(request,'Please enter vaild email')
            else:
                messages.error(request," please Agree on the terms")
        else:
            messages.error(request,f"Check empty fileds")
        
        context = {
            'fname': fname,
            'lname': lname,
            'city': city,
            'state': state,
            'zip' : zip,
            'user':username,
            'pass': password,
            'email': email,
            'agree': agree,
            'address1':address1,
            'address2':address2,
            'is_added':is_added
        }
        return render(request,'accounts/signup.html',context)
    else:
        return render(request,'accounts/signup.html')

def profile(request):
    if request.method == "POST" and 'btnsave' in request.POST:
        if request.user != None and request.user.id != None:
            userprofile = UserProfile.objects.get(user=request.user)
            if request.POST['lname'] and request.POST['fname']\
            and request.POST['address1'] and request.POST['address2']\
            and request.POST['city'] and request.POST['state']\
            and request.POST['zip'] and request.POST['username']\
            and request.POST['password'] and request.POST['email']:
                request.user.first_name = request.POST['fname']
                request.user.last_name = request.POST['lname']
                # request.user.email = request.POST['email']
                # request.user.username = request.POST['username']
                if not request.POST['password'].startswith("pbkdf2_sha256$"):
                    request.user.set_password(request.POST['password'])
                userprofile.address1 = request.POST['address1']
                userprofile.address2 = request.POST['address2']
                userprofile.city = request.POST['city']
                userprofile.state = request.POST['state']
                userprofile.zip_number = request.POST['zip']
                request.user.save()
                userprofile.save()
                auth.login(request,request.user)
                messages.success(request,"Your data saved successfuly")
            else:
                messages.error(request,"Check your values and elements")
        return redirect('profile')
    else: 
        user =None
        if request.user.is_anonymous:
            user = None
        else:
            user = request.user
        if user != None:
            
            userprofile = UserProfile.objects.get(user=user)
            context = {
                'fname':user.first_name,
                'lname':user.last_name,
                'username':user.username,
                'password':user.password,
                'email':user.email,
                'address1':userprofile.address1,
                'address2':userprofile.address2,
                'city':userprofile.city,
                'state':userprofile.state,
                'zip':userprofile.zip_number
            }
            
            return render(request,'accounts/profile.html',context)
        else:
            return render(request,'accounts/profile.html')


def favorite_pro(request,pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        product = Product.objects.get(pk=pro_id)
        if UserProfile.objects.filter(user=request.user,pro_favorite=product).exists():
            messages.info(request,"The product are aleady in Favorites products ")
        else:
            userprofile = UserProfile.objects.get(user=request.user)
            userprofile.pro_favorite.add(product)
            messages.success(request,"You put the product in your favorite list ")
    else:
        messages.error(request,"You must be logged")
    
    return redirect('/products/'+ str(pro_id))

def favorite_products(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        userinfo = UserProfile.objects.get(user=request.user)
        pro = userinfo.pro_favorite.all()
        context = {
            'products':pro
        }
        
    return render(request,'products/products.html',context)