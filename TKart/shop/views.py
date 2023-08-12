from django.shortcuts import render, redirect
from django.http import HttpResponse


from .models import Product, Contact, Orders, OrderUpdate
from math import ceil

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

def index(request):
    products = Product.objects.all()
    # print(products)
    # n = len(products)
    # noslides = n//4 + ceil((n/4)-(n//4))

    # params = {'no_of_slides':noslides, 'range': range(1,noslides),'product':products }
    # allProds = [[products, range(1,noslides),noslides],
    #             [products, range(1,noslides),noslides]]
    # params = {'allProds':allProds}
    
    allProds = []

    catprods = Product.objects.values('category','id')

    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category = cat)
        n = len(prod)
        noslides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod, range(1,noslides),noslides])
    
    params = {'allProds':allProds}
    return render(request, 'shop/index.html',params)


def searchMatch(query,item):
     if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
          return True
     else:
          return False


def search(request): 
        query = request.GET.get('search')
        allProds = []

        catprods = Product.objects.values('category','id')

        cats = {item['category'] for item in catprods}
        for cat in cats:
            prodtemp = Product.objects.filter(category = cat)
            prod =[item for item in prodtemp if searchMatch(query.lower(), item)]
            n = len(prod)

            noslides = n//4 + ceil((n/4)-(n//4))
            if len(prod)!=0:
                 allProds.append([prod, range(1,noslides),noslides])
                
        params = {'allProds':allProds,'msg':""}
        if len(allProds) == 0 or len(query) < 2:
             params = {'msg':"No Such Item "}
        return render(request, 'shop/search.html',params)
# In this template, you can directly access the values from the params 
# dictionary ({{allProds}} and msg) without 
# using params.allProds and params.msg, as the dictionary is passed directly to the
# template context.

def about(request):
    return render(request,'shop/about.html')

def contact(request):
    res = False
    if request.method == "POST":

        name = request.POST.get('name','')
        email= request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        # print(name,email,phone,desc)

        contact = Contact(name=name, email=email, phone=phone,desc=desc)
        contact.save()
        res = True
        # return render(request,'shop/contact.html',{'res':res})
    return render(request, 'shop/contact.html',{'res':res})


def tracker(request):
            
      if request.method == "POST":
        orderid = request.POST.get('orderId','')
        email= request.POST.get('email','')
        try:
            order = Orders.objects.filter(order_id=orderid,email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id = orderid)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)#default = str isliye likha hai kyoki Object of type date is not JSON serializable
                return HttpResponse(response)
            else:
                    return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
             
      return render(request, 'shop/tracker.html')



def productView(request,myid):
    #fetch product using id
    product = Product.objects.filter(id=myid)
    # print(product)
    return render(request, 'shop/prodview.html',{'product':product[0]})


def checkout(request):
        if request.method == "POST":
            items_json = request.POST.get('itemsJson')
            name = request.POST.get('name','')
            amount = request.POST.get('amount','')
            email= request.POST.get('email','')
            address = request.POST.get('address1','') + " " + request.POST.get('address2','')
            city = request.POST.get('city','')
            state = request.POST.get('state','')
            zip_code = request.POST.get('zip_code','')
            phone = request.POST.get('phone','')

            order = Orders(items_json = items_json,name=name, email=email,address = address,
                        city=city , state=state, zip_code = zip_code, phone=phone,amount=amount)
            order.save()
            update = OrderUpdate(order_id = order.order_id, update_desc = "The order has been Placed")
            update.save()
            thank = True
            id = order.order_id
            return render(request, 'shop/checkout.html', {'thank':thank, 'id':id}) 
            #request paytm to transfer the amount to your account after payment by user
        return render(request, 'shop/checkout.html')

def loginUser(request):
    feed="False"
    if request.method == 'POST':                 #jab ham post nahi laga rahe the tho seedha none print ho raha tha bina details bahre
        print("teuererererererer")
        loginusername = request.POST.get('loginusername')
        loginpassword = request.POST.get('loginpassword')
        user = authenticate(username=loginusername,password=loginpassword)
        print(user)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully logged in")
            print("if")
            feed="True"
            params = {'feed' : feed,'username':loginusername}
            return redirect("/shop") # / krne se pichla wala chala jata hai

        else:
            print("else")
            messages.error(request,"Credectial are invalid")
            return redirect("/shop/login")

    return render(request,'shop/login.html')

def logoutUser(request):
        logout(request)
        messages.success(request,"Successfully logged Out")
        return HttpResponse("LOgout")
     

def signUp(request):
        return render(request,'shop/signUp.html')


        # else:
        #     # return render(request,'shop/signUp.html')
        #     return HttpResponse("404 - Not found")

def handlesignup(request):
            if request.method =="POST":
                username=request.POST['username']
                email=request.POST['email']
                fname=request.POST['fname']
                lname=request.POST['lname']
                pass1=request.POST['pass1']
                pass2=request.POST['pass2']

                print(username,email,pass1,pass2)
            # check for errorneous input
                if len(username) > 15:
                     messages.error(request, "username must be under 15 characters")
                     return redirect('/shop/signUp/')
  
                if not username.isalnum():
                     messages.error(request, "username should only contain letters and numbers")
                     return redirect('/shop/signUp/')
                
                if pass1 != pass2:
                     messages.error(request,"password do not match")
                     return redirect('/shop/signUp/')
                
            # Create the user
                myuser = User.objects.create_user(username, email, pass1)
                myuser.first_name= fname
                myuser.last_name= lname
                # print(myuser)
                myuser.save()
                messages.success(request, " Your TKart account has been successfully created")
                return redirect('/shop/login')
            return HttpResponse("404 not found signup")
     
@csrf_exempt
def handlerequest(request):
     #paytm will send you post request here
     pass


