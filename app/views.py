from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .models import LoginData,item,cart, address, order
from .forms import RegForm, LoginForm, addressForm
from django.contrib.auth.decorators import login_required
from django.views import View
from django.core.mail import EmailMessage

def signup(request,*args,**kwargs):
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    if request.POST:
        if user.is_authenticated:
            return redirect("home")
        form = RegForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email,password=raw_password)
            login(request,account)
            return redirect("home")
        else:
            request.session['form'] = form._errors
            return redirect('signup')
    form2 = RegForm()
    data = request.session.get('form',False)
    form2._errors = data
    if data:
        del request.session['form']
    else:
        form2 = RegForm()
    return render(request,"page/signup.html",{"form":form2})
def logout_view(request):
    logout(request)
    return redirect("home")

    
def login_view(request,*args,**kwargs):
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email'].lower()
            raw_password = request.POST['password']
            account = authenticate(email=email,password=raw_password)
            if account:
                login(request,account)
                return redirect("home")
            else:
                request.session['data'] = f"Email id or Password is incorrect. Please try again with correct email id and password"
                return redirect("login")
        else:
            request.session['form'] = form._errors
            return redirect("login")
    data = request.session.get('data',False)
    form2 = request.session.get('form',False)
    mainform = LoginForm()
    mainform._errors = form2
    if form2:
        del request.session['form']
    else:
        mainform = LoginForm()
    if data:
        del request.session['data']
    return render(request,"page/login.html",{"form":mainform,"nologin":data})


@login_required(login_url='/login/')
def home(request):
    obj = {
        "object": item.objects.all()
    }
    return render(request, "page/home.html",obj)
@login_required(login_url='/login/')
def cart_data(request):
    data = cart.objects.filter(userId=request.user)
    sum=0
    for i in data:
        sum = sum + i.nameId.price
    obj = {
        "object": data,
        "itemAmount":data.count(),
        "itemSum":sum,
    }
    return render(request, "page/cart.html",obj)
@login_required(login_url='/login/')
def add_to_cart(request,id):
    data = item.objects.get(pk = id)
    return render(request, "page/details.html",{"data":data})
@login_required(login_url='/login/')
def add_to_cart_main(request,id):
    data = item.objects.get(pk = id)
    newdata = cart(userId = request.user, nameId = data, number=0)
    try:
        cart.objects.get(userId=request.user, nameId=id)
    except:
        newdata.save()
    return redirect("cart_data")

@login_required(login_url='/login/')
def add_to_cart_delete(request,id):
    try:
        data = cart.objects.get(userId=request.user, pk=id)
        data.delete()
    except:
        pass
    return redirect("cart_data")

def address_view(request):
    form = addressForm()
    if request.POST:
        form = addressForm(request.POST)
        if form.is_valid():
            savepost = form.save(commit=False)
            savepost.userId = request.user
            savepost.save()
            return redirect("cart_data")
        else:
            pass
    return render(request, "page/address.html",{"form":form})
def order_view(request):
    data = order.objects.filter(userId=request.user)
    return render(request, "page/order.html",{"data":data})
def order_delete(request,id):
    if request.POST:
        data = order.objects.get(userId=request.user,pk=id)
        data.delete()
    return redirect("order") 

def buy_now(request):
    data = cart.objects.filter(userId=request.user)
    addressData = address.objects.filter(userId = request.user)
    sum=0
    for i in data:
        sum = sum + i.nameId.price
    obj = {
        "object": data,
        "itemSum":sum,
        "data": addressData,
    }
    if request.POST:
        obj["error"] = "Please select a Address, You have not selected any."
        try:
            request.POST["address"]
            addressdata = request.POST["address"]
        except:
            return render(request, "page/buynow.html", obj)
        arr=""
        try:
            for i in data:
                arr = arr + "> " + str(i.nameId.name) + "<br>"
                itemAmount = request.POST[f'itemAmount{i.nameId.id}']
                d = order(userId = request.user,address=addressdata,number= itemAmount,nameId=i.nameId)
                d.save()
            cart.objects.all().delete()
        except:
            return redirect("cart_data") 
        message = "Hi "+f"{request.user.username}"+"<br> You have Purchased <br>"+f"{arr}"+"<br> Total of: "+f"{sum}"+"<br> Thank you for purchasing"
        msg = EmailMessage(
            'Orders',
            message,
            'pallavraj23102000@gmail.com',
            [request.user.email]
        )
        msg.content_subtype = "html"
        msg.send()
        return redirect("order")
    return render(request, "page/buynow.html", obj)


def address_delete(request,id):
    data = address.objects.get(pk = id)
    if request.method == "POST":
        data.delete()
        return redirect("buy_now")
    return redirect("address_edit",id)
def address_edit(request,id):
    data = address.objects.get(pk = id)
    if request.POST:
        form = addressForm(request.POST)
        if form.is_valid():
            savedata = form.save(commit=False)
            savedata.userId = request.user
            savedata.id = id
            savedata.save()
            return redirect("buy_now")
        else:
           return render(request, "page/adddress-edit.html",{"data":data,"form":form,"id":id}) 
    return render(request, "page/address-edit.html",{"data":data,"id":id})
