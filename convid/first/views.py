from django.shortcuts import render,redirect
from django.contrib.auth.models import User ,auth
from django.contrib import messages
from .models import Profile

import smtplib

# Create your views here.
def home(request):
    if request.method=="POST":
        search=request.POST['search']
        #query="select * from first_Profile where user like '%"  + search  +   "%' AND status = True  "
        #shops=Profile.objects.raw(query)
        #user_id=User(username=search)
        user_id=User.objects.get(username=search).pk

        shops=Profile.objects.filter(status=True,user=user_id).all()
        res="Search Results : "+str(search)
        dist={'shops':shops,
               'topic':res}
        return render(request,'Trend.html',dist)

    shops=Profile.objects.filter(status=True).all()
    res="Trending Shops And Offers"

    dist={'shops':shops,"topic":res}
    return render(request,'Trend.html',dist)

def page(request,id=None):
    data=Profile.objects.get(id=id)
    dist={
    'data':data
    }
    return render(request,"shop.html",dist)

def logout(request):
    auth.logout(request)
    return redirect("/")

def index(request):
    return render(request,'title.html')

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None :
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,"Username or Password is wrong")
            return redirect("login")

    return render(request,"Login.html")

#function for Category (user / employer)
def choose_cat(request):
    return render(request,"b4_SignUp.html")

def shop_signup(request):
    if request.method=='POST':
        username=request.POST['shopname']
        first_name="shop"
        last_name=username

        password1=request.POST['password1']
        email=request.POST['email']
        password2=request.POST['password2']


        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username is already taken!")
                return redirect('shop_signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email id is already taken!")
                return redirect('shop_signup')
            elif len(password1)<8:
                messages.info(request,"Password length must be greater then 7")
                return redirect('shop_signup')

            else:
                  user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password1)
                  user.save();
        #phoneno bio location img dist

                  phoneno=request.POST['phoneno']
                  bio=request.POST['bio']
                  location=request.POST['location']
                  img=request.POST['img']
                  dist=request.POST['dist']

                  obj=Profile(user=user,bio=bio,location=location,dist=dist,phone_no=phoneno,img=img)
                  obj.save();

                  messages.info(request,"Thank you for registation ,We contant you soon !")
                  return redirect('shop_signup')

        else:
            messages.info(request,"password not maching")
            return redirect('shop_signup')

    return render(request,"shop_signup.html")

def send_emailto(rev):
  try:
    sender_email="convid.live@gmail.com"
    rec_email=rev
    password="Convid.live2020"
    message="Thank you for creating account in ConVid"

    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(sender_email,password)
    #print("log in done")
    server.sendmail(sender_email,rec_email,message)
    #print("email send")
  except  :
      print("\n\n0error\n\n")



def signup (request):
    if request.method=='POST':
        username=request.POST['username']
        first_name="Custom"  #to differnt the Custom / employer
        last_name="Convid User" #used to store shop name
        password1=request.POST['password1']
        email=request.POST['email']
        password2=request.POST['password2']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username is already taken!")
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email id is already taken!")
                return redirect('signup')
            elif len(password1)<8:
                messages.info(request,"Password length must be greater then 7")
                return redirect('signup')

            else:
                  user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password1)
                  user.save();
                  send_emailto(email) #sending email
                  return redirect('login')
        else:
            messages.info(request,"password not maching")
            return redirect('signup')


    else:
         return render(request,'SignUp.html')


def aboutus(request):
             return render(request,'aboutus.html')


def contactus(request):
             return render(request,'contact_us.html')
