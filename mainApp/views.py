from django.shortcuts import render,HttpResponseRedirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from shop.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRTE_KEY
import razorpay
from django.conf import settings
from django.db.models import Q
from random import randint
import os
from .models import *

def home_page(request):
    product = Product.objects.all()
    product = product[::-1]
    if(request.method=='POST'):
        try:
            email = request.POST.get('email')
            n = NewsLatter()
            n.email = email
            n.save()
        except:
            pass
        return HttpResponseRedirect("/")
    return render(request, "index.html",{"Products":product})

def shop_page(request,mc,sc,br):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    brand = Brand.objects.all()
    if(request.method=="POST"):
        search = request.POST.get("search")
        product = Product.objects.filter(Q(name__icontains=search))
    else:
        if(mc=="All" and sc=="All" and br=="All"):
            product = Product.objects.all()
        elif(mc!="All" and sc=="All" and br=="All"):
            product = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc))
        elif(mc=="All" and sc!="All" and br=="All"):
            product = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc))
        elif(mc=="All" and sc=="All" and br!="All"):
            product = Product.objects.filter(brand=Brand.objects.get(name=br))
        elif(mc!="All" and sc!="All" and br=="All"):
            product = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc))
        elif(mc!="All" and sc=="All" and br!="All"):
            product = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br))
        elif(mc=="All" and sc!="All" and br!="All"):
            product = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc),brand=Brand.objects.get(name=br))
        else:
            product = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc),brand=Brand.objects.get(name=br))
        product = product[::-1]
    return render(request,"shoppage.html",{"Products":product,
                                           "Maincategory":maincategory,
                                           "Subcategory":subcategory,
                                           "Brand":brand,
                                           "mc":mc,"sc":sc,"br":br})

def login_page(request):
    if(request.method=='POST'):
        username = request.POST.get("username")
        password = request.POST.get("lpassword")
        user = auth.authenticate(username=username,password=password)
        if(user is not None):
            auth.login(request,user)
            if(user.is_superuser):
                return HttpResponseRedirect("/admin/")
            else:
                return HttpResponseRedirect("/profile/")
        else:
            messages.error(request,"Invalid User Name or Password")
    return render(request, "login.html")

def sign_up(request):
    if(request.method=="POST"):
        actype = request.POST.get('actype')
        if(actype=="saller"):
            u = Seller()
        else:
            u = Buyer()
        u.name = request.POST.get("name")
        u.username = request.POST.get("username")
        u.number = request.POST.get("number")
        u.email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        u.name = request.POST.get("name")
        if(password == confirm_password):
            try:
                user = User.objects.create_user(username=u.username, password=password, email=u.email)
                user.save()
                u.save()
                subject = 'Thanks to Create an Account with Us : Team Online Bazar'
                message = """
                    Thanks %s Create an Account with Us
                    Keep Shoping With US
                    http://localhost:8000
                    """%(u.name)
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [u.email, ]
                send_mail( subject, message, email_from, recipient_list )
                return HttpResponseRedirect("/login/")
            except:
                messages.error(request,"User Name Already Taken")
                return render(request, "signup.html")
        else:
            messages.error(request,"Confirm Password does not matched Please Enter Correct Password")
    return render(request, "signup.html")

@login_required(login_url='/login/')
def seller_profile(request):
    user = User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        try:
            seller = Seller.objects.get(username=request.user)
            product = Product.objects.filter(seller=seller)
            product = product[::-1]
            return render(request,"sellerprofile.html",{"User": seller,"Products":product})
        except:
            buyer = Buyer.objects.get(username=request.user)
            wishlist = Wishlist.objects.filter(buyer=buyer)
            checkout = Checkout.objects.filter(buyer=buyer)
            checkout = checkout[::-1]
            return render(request,"buyerprofile.html",{"User": buyer,"Wishlist":wishlist,"Orders":checkout})

    
@login_required(login_url='/login/')
def update_profile(request):
    user = User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        try:
            user = Seller.objects.get(username=request.user)
        except:
            user = Buyer.objects.get(username=request.user)
        if(request.method =='POST'):
            user.name = request.POST.get('name')
            user.email = request.POST.get('email')
            user.phone = request.POST.get('phone')
            user.addressline1 = request.POST.get('addressline1')
            user.addressline2 = request.POST.get('addressline2')
            user.pincode = request.POST.get('pincode')
            user.city = request.POST.get('city')
            user.state = request.POST.get('state')
            if(request.FILES.get("pic")):
                if(user.pic):
                    os.remove("media/"+str(user.pic))
                user.pic=request.FILES.get('pic')
            user.save()
            return HttpResponseRedirect("/profile/")
    return render(request,"updateprofile.html",{"User": user})

@login_required(login_url='/login/')
def addProduct(request):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    brand = Brand.objects.all()
    if(request.method=='POST'):
        p = Product()
        p.name = request.POST.get("name")
        p.maincategory = Maincategory.objects.get(name=request.POST.get("maincategory"))
        p.subcategory = Subcategory.objects.get(name=request.POST.get("subcategory"))
        p.brand = Brand.objects.get(name=request.POST.get("brand"))
        p.stock = request.POST.get("stock")
        p.baseprice = int(request.POST.get("baseprice"))
        p.discount =int(request.POST.get("discount"))
        p.finalprice = p.baseprice-p.baseprice*p.discount/100
        color=""
        if(request.POST.get("red")):
            color=color+"red,"
        if(request.POST.get("white")):
            color=color+"white,"
        if(request.POST.get("black")):
            color=color+"black,"
        if(request.POST.get("green")):
            color=color+"green,"
        if(request.POST.get("pink")):
            color=color+"pink,"
        if(request.POST.get("sky")):
            color=color+"sky,"
        if(request.POST.get("blue")):
            color=color+"blue,"
        if(request.POST.get("maron")):
            color=color+"maron,"
        if(request.POST.get("violet")):
            color=color+"violet,"
        if(request.POST.get("light_green")):
            color=color+"light_green,"
        if(request.POST.get("yellow")):
            color=color+"yellow,"
        if(request.POST.get("purpule")):
            color=color+"purpule,"
        size =""
        if(request.POST.get("XS")):
            size=size+"XS,"
        if(request.POST.get("S")):
            size=size+"S,"
        if(request.POST.get("SM")):
            size=size+"SM,"
        if(request.POST.get("M")):
            size=size+"M,"
        if(request.POST.get("L")):
            size=size+"L,"
        if(request.POST.get("XL")):
            size=size+"XL,"
        if(request.POST.get("XXL")):
            size=size+"XXL,"
        if(request.POST.get("26")):
            size=size+"26,"
        if(request.POST.get("28")):
            size=size+"28,"
        if(request.POST.get("30")):
            size=size+"30,"
        if(request.POST.get("32")):
            size=size+"32,"
        if(request.POST.get("34")):
            size=size+"34,"
        p.color=color
        p.size=size
        p.discription = request.POST.get("discription")
        p.pic1 = request.FILES.get("pic1")
        p.pic2 = request.FILES.get("pic2")
        p.pic3 = request.FILES.get("pic3")
        p.pic4 = request.FILES.get("pic4")
        try:
            p.seller = Seller.objects.get(username=request.user)
        except:
            HttpResponseRedirect("/profile/")
        p.save()
        subject = 'Checkout Our Latest Product on Online Bazar : Team Online Bazar'
        message = """
                    Hey !!!
                    We Add Some Latest Product with best Offers
                    Keep Shoping With US
                    http://localhost:8000/single-product/%d
                    """%(p.id)
        email_from = settings.EMAIL_HOST_USER
        subscriber = NewsLatter.objects.all()
        recipient_list = subscriber
        send_mail( subject, message, email_from, recipient_list )
        return HttpResponseRedirect("/profile/")
    return render(request,"addProduct.html",{"Maincategory":maincategory,"Subcategory":subcategory,"Brand":brand})

@login_required(login_url='/login/')
def deleteProduct(request,num):
    try:
        p = Product.objects.get(id=num)
        seller = Seller.objects.get(username=request.user)
        if(p.seller == seller):
            p.delete()
        return HttpResponseRedirect("/profile/")
    except:
        HttpResponseRedirect("/profile/")

@login_required(login_url='/login/')
def editProduct(request,num):
    p = Product.objects.get(id=num)
    seller = Seller.objects.get(username=request.user)
    if(p.seller == seller):
        maincategory = Maincategory.objects.exclude(name=p.maincategory)
        subcategory = Subcategory.objects.exclude(name=p.subcategory)
        brand = Brand.objects.exclude(name=p.brand)
        if(request.method=='POST'):
            p.name = request.POST.get("name")
            p.maincategory = Maincategory.objects.get(name=request.POST.get("maincategory"))
            p.subcategory = Subcategory.objects.get(name=request.POST.get("subcategory"))
            p.brand = Brand.objects.get(name=request.POST.get("brand"))
            p.stock = request.POST.get("stock")
            p.baseprice = int(request.POST.get("baseprice"))
            p.discount =int(request.POST.get("discount"))
            p.finalprice = p.baseprice-p.baseprice*p.discount/100
            color=""
            if(request.POST.get("red")):
                color=color+"red,"
            if(request.POST.get("white")):
                color=color+"white,"
            if(request.POST.get("black")):
                color=color+"black,"
            if(request.POST.get("green")):
                color=color+"green,"
            if(request.POST.get("pink")):
                color=color+"pink,"
            if(request.POST.get("sky")):
                color=color+"sky,"
            if(request.POST.get("blue")):
                color=color+"blue,"
            if(request.POST.get("maron")):
                color=color+"maron,"
            if(request.POST.get("violet")):
                color=color+"violet,"
            if(request.POST.get("light_green")):
                color=color+"light_green,"
            if(request.POST.get("yellow")):
                color=color+"yellow,"
            if(request.POST.get("purpule")):
                color=color+"purpule,"
            size =""
            if(request.POST.get("XS")):
                size=size+"XS,"
            if(request.POST.get("S")):
                size=size+"S,"
            if(request.POST.get("SM")):
                size=size+"SM,"
            if(request.POST.get("M")):
                size=size+"M,"
            if(request.POST.get("L")):
                size=size+"L,"
            if(request.POST.get("XL")):
                size=size+"XL,"
            if(request.POST.get("XXL")):
                size=size+"XXL,"
            if(request.POST.get("26")):
                size=size+"26,"
            if(request.POST.get("28")):
                size=size+"28,"
            if(request.POST.get("30")):
                size=size+"30,"
            if(request.POST.get("32")):
                size=size+"32,"
            if(request.POST.get("34")):
                size=size+"34,"
            p.color=color
            p.size=size
            p.discription = request.POST.get("discription")
            if(request.FILES.get("pic1")):
                if(p.pic1):
                    os.remove("media/"+str(p.pic1))
                p.pic1 = request.FILES.get("pic1")
            if(request.FILES.get("pic2")):
                if(p.pic2):
                    os.remove("media/"+str(p.pic2))
                p.pic2 = request.FILES.get("pic2")
            if(request.FILES.get("pic3")):
                if(p.pic3):
                    os.remove("media/"+str(p.pic3))
                p.pic3 = request.FILES.get("pic3")
            if(request.FILES.get("pic4")):
                if(p.pic4):
                    os.remove("media/"+str(p.pic4))
                p.pic4 = request.FILES.get("pic4")
            p.save()
            return HttpResponseRedirect("/profile/")
        return render(request,"editProduct.html",{"Product":p,"Maincategory":maincategory,"Subcategory":subcategory,"Brand":brand})
    return HttpResponseRedirect("/profile/")

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")

def singleProduct(request,num):
    p = Product.objects.get(id=num)
    color = p.color.split(",")
    color = color[:-1]
    size = p.size.split(",")
    size = size[:-1]
    return render(request,"singleProduct.html",{"Product":p,"Color":color,"Size":size})

def wishlist(request,num):
    try:
        buyer = Buyer.objects.get(username=request.user)
        p = Product.objects.get(id=num)
        wishlist = Wishlist.objects.filter(buyer=buyer)
        flag = False
        for i in wishlist:
            if(i.product==p):
                flag=True
                break
        if(flag==False):
            w = Wishlist()
            w.buyer = buyer
            w.product = p
            w.save()
        return HttpResponseRedirect("/profile/")
    except:
       return HttpResponseRedirect("/profile/")
    
    
@login_required(login_url='/login/')
def deleteWishlist(request,num):
    try:
        w = Wishlist.objects.get(id=num)
        buyer = Buyer.objects.get(username=request.user)
        if(w.buyer == buyer):
            w.delete()
        return HttpResponseRedirect("/profile/")
    except:
        HttpResponseRedirect("/profile/")

def addToCart(request):
    pid = request.POST.get("pid")
    color = request.POST.get("color")
    size = request.POST.get("size")
    cart = request.session.get("cart",None)
    if(cart):
        if(pid in cart.keys() and color==cart[pid][1] and size==cart[pid][2]):
            pass
        else:
            count = len(cart.keys())
            count = count+1
            cart.setdefault(str(count),[pid,1,color,size])
    else:
        cart = {"1":[pid,1,color,size]}
    request.session["cart"] = cart
    return HttpResponseRedirect("/cart/")

def cartPage(request):
    cart = request.session.get("cart",None)
    total=0
    shopping=0
    final = 0
    if(cart):
        for values in cart.values():
            p = Product.objects.get(id=int(values[0]))
            total = total+p.finalprice*values[1]
        if(len(cart.values())>=1 and total>1000):
            shopping = 150
        final = total+shopping
    return render(request,"cart.html",{"Cart":cart,"Total":total,"Shopping":shopping,"Final":final})

def updateCart(request,id,num):
    cart = request.session.get("cart",None)
    if(cart):
        if(num=="-1"):
            if(cart[id][1]>1):
                q = cart[id][1]
                q = q-1
                cart[id][1] = q
        else:
            q = cart[id][1]
            q = q+1
            cart[id][1] = q
        request.session["cart"] = cart
    return HttpResponseRedirect("/cart/")

def deleteCart(request,id):
    cart = request.session.get("cart",None)
    if(cart):
        cart.pop(id)
        request.session['cart'] = cart
    return HttpResponseRedirect("/cart/")


client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRTE_KEY))
@login_required(login_url='/login/')
def checkPage(request):
    cart = request.session.get("cart",None)
    total=0
    shopping=0
    final = 0
    if(cart):
        for values in cart.values():
            p = Product.objects.get(id=int(values[0]))
            total = total+p.finalprice*values[1]
        if(len(cart.values())>=1 and total>1000):
            shopping = 150
        final = total+shopping
    try:
        buyer = Buyer.objects.get(username=request.user)
        if(request.method=="POST"):
            mode = request.POST.get("mode")
            check = Checkout()
            check.buyer = buyer
            check.total = total
            check.shopping = shopping
            check.final = final
            check.save()
            check_id = Checkout.objects.get(id=check.id)
            for value in cart.values():
                cp = CheckOutProduct()
                p = Product.objects.get(id=int(value[0]))
                cp.name = p.name
                cp.size = value[3]
                cp.color = value[2]
                cp.pic = p.pic1.url
                cp.price = p.finalprice
                cp.qty = value[1]
                cp.total = p.finalprice*value[1]
                cp.checkout = check_id
                cp.save()
            request.session['cart']={}
            if(mode=="cod"):
                return HttpResponseRedirect("/confirmation/")
            else:
                orderAmount = check.final*100
                orderCurrency = 'INR'
                paymentOrder = client.order.create(dict(amount=orderAmount,currency=orderCurrency))
                paymentId = paymentOrder['Id']
                check.mode = 'Net Banking'
                check.save()
                return render(request,"pay.html",
                              {"amount": orderAmount,
                            "api_key":RAZORPAY_API_KEY,
                            "order_id":paymentId,
                            "User":buyer})
        return render(request,"checkout.html",{"Cart":cart,"Total":total,"Shopping":shopping,"Final":final,"Buyer":buyer})
    except:
        return HttpResponseRedirect("/profile/")


@login_required(login_url='/login/')
def paymentSuccess(request,rpid,roid,rsid):
    buyer = Buyer.objects.get(username=request.user)
    check = Checkout.objects.filter(buyer=buyer)
    check = check[::-1]
    check = check[0]
    check.paymentId = rpid
    check.orderId = roid
    check.paymentsignature = rsid
    check.paymentstatus = 2
    check.save()
    return HttpResponseRedirect('/confirmation/')

@login_required(login_url='/login/')
def paynow(request,num):
    try:
        buyer = Buyer.objects.get(username=request.user)
    except:
        return HttpResponseRedirect('/profile/')
    check = Checkout.objects.get(id=num)
    orderAmount = check.final*100
    orderCurrency = 'INR'
    paymentOrder = client.order.create(dict(amount=orderAmount,currency=orderCurrency))
    paymentId = paymentOrder['id']
    check.mode = 'Net Banking'
    check.save()
    return render(request,"pay.html",
                              {"amount": orderAmount,
                            "api_key":RAZORPAY_API_KEY,
                            "order_id":paymentId,
                            "User":buyer})

def confirmationPage(request):
    buyer = Buyer.objects.get(username=request.user)
    subject = 'Thanks to Shopping with Us : Team Online Bazar'
    message = """
                    Hey !!!
                    We Add Some Latest Product with best Offers
                    Keep Shoping With US
                    http://localhost:8000/%d
                    """%(buyer.name)
    email_from = settings.EMAIL_HOST_USER
    subscriber = NewsLatter.objects.all()
    recipient_list = [buyer.email, ]
    send_mail( subject, message, email_from, recipient_list )
    return render(request,"confirmation.html")

def contact(request):
    if(request.method=="POST"):
        c = Contact()
        c.name = request.POST.get("name")
        c.phone = request.POST.get("phone")
        c.email = request.POST.get("email")
        c.subject = request.POST.get("subject")
        c.message = request.POST.get("message")
        c.save()
        subject = 'Query Has Been Submitted | Team Online Bazar'
        message = """
                    Thanks to Share Your Query with US
                    Our Team Will Contact You Soon
                    Keep Shoping With US
                    http://localhost:8000"""
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [c.email, ]
        send_mail( subject, message, email_from, recipient_list )
        messages.success(request,"Your Query has been Submitted !!!!! Our Team Will Contat You Soon")
    return render(request,"contact.html")

def forgetUsername(request):
    if(request.method=="POST"):
        username = request.POST.get("username")
        user = User.objects.get(username=username)
        if(user is not None):
            try:
                user = Buyer.objects.get(username=username)
            except:
                user = Seller.objects.get(username=username)
            num = randint(100000,9999999)
            request.session['otp'] = num
            request.session['user'] = username
            subject = 'OTP for Rest Password : Team Online Bazar'
            message = """
                    OTP: %d
                    Keep Shoping With US
                    http://localhost:8000
                    """%num

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return HttpResponseRedirect("/forget-otp/")
        else:
            messages.error(request,"Username Not Found")
    return render(request,"forget_username.html")

def forgetOtp(request):
    if(request.method=="POST"):
        otp = int(request.POST.get("otp"))
        sesionOTP = request.session.get('otp',None)
        if(otp==sesionOTP):
            return HttpResponseRedirect("/forget-password/")
        else:
            messages.error(request,"Invalid OTP, Please Enter Correct OTP ")
    return render(request,"forget_otp.html")


def forgetPassword(request):
    if(request.method=="POST"):
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        if(password==cpassword):
            user = User.objects.get(username=request.session.get("user"))
            user.set_password(password)
            user.save()
            return HttpResponseRedirect("/login/")
        else:
            messages.error(request,"Password and Confirm Password Does't Matched, Please Enter Correct")
    return render(request,"forget_password.html")