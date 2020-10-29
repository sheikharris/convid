from django.shortcuts import render,redirect
from django.contrib.auth.models import User ,auth
from django.contrib import messages
from .models import Profile,Section
from .forms import *


import smtplib


def empcalllog(request):
    if request.user.is_authenticated and request.user.is_staff:
        user=request.user
        dist={
        "username":user.get_username(),
        "shopname":user.last_name,
        "section": user.get_short_name(),

        }
        return render(request,'emplog.html',dist)
    else:
       return redirect('login')

def addorder(request):
    return render(request,'Addorder.html')

def editemp(request,id=None):
    if request.method=="POST":
            a = User.objects.get(id = id)
            a.first_name=request.POST['section']
            a.save()
            name=a.get_username()
            msg=name+" is changed sucessfully !"
            messages.info(request,msg)
            return redirect('viewemp')


    shop=Profile.objects.get(user=request.user)
    a = User.objects.get(id = id)
    b=Section.objects.values()
    username=a.get_username()
    sec=a.get_short_name()

    dist={
    "shop":shop,
    "username":username,
    "section":sec,
    "sec":b,
    "i":a,

    }
    return render(request,"editemp.html",dist)

def editsection(request,id=None):
    if request.method=="POST":
        a = Section.objects.get(id = id)
        name=a.section_name
        name1=request.POST['section_name']
        a.section_name=name1
        a.description=request.POST['section_des']
        #a.img=request.POST['image']
        a.save()
        if name!=name1:
            while True:
                temp=User.objects.filter(first_name=name).values()
                if len(temp)!=0:
                    new_user=User.objects.get(first_name=name)
                    new_user.first_name=name1
                    new_user.save()
                else: break

        msg=name+" is changed sucessfully !"
        messages.info(request,msg)
        return redirect('viewsection')

    shop=Profile.objects.get(user=request.user)
    a = Section.objects.get(id = id)

    dist={
    "shop":shop,
    "sec":a,

    }
    return render(request,"editsection.html",dist)


def deletesection(request,id=None):
    a = Section.objects.get(id = id)
    name=a.section_name
    a.delete()
    msg=name+" is removed !"
    messages.info(request,msg)
    return redirect("viewsection")


def deleteemp(request,id=None):
    a = User.objects.get(id = id)
    name=a.username
    a.delete()
    msg=name+" is removed !"
    messages.info(request,msg)
    return redirect("viewemp")

def openshop(request):
    t = Profile.objects.get(user=request.user)
    t.status = True
    t.save()
    return redirect('shopadmin')

def closeshop(request,id=None):
    t = Profile.objects.get(user=request.user)
    t.status = False
    t.save()
    return redirect('shopadmin')

def shopAdmin(request):
    if request.user.is_authenticated and request.user.is_staff:
        shop=Profile.objects.get(user=request.user)
        sec = Section.objects.filter(user=shop.user)

        dist={'shop':shop,
             'sec': sec
        }
        return render(request,'shopadmin.html',dist)
    else :
       messages.info(request,"Login to enter")
       return redirect("login")


def viewEmp(request):
                shop=Profile.objects.get(user=request.user)
                name=request.user.get_username()
                employers =User.objects.filter(last_name=name).order_by('first_name').values()

                dist={
                "shop":shop,
                "employers":employers,
                }

                return render(request,"viewemp.html",dist)

def viewsection(request):
            shop=Profile.objects.get(user=request.user)
            sec = Section.objects.filter(user=shop.user).order_by('section_name').values()
            dist={
            "shop":shop,
            "sec":sec,
            }

            return render(request,"viewsection.html",dist)

def addEmp(request):
    if request.user.is_authenticated and request.user.is_staff:

        if request.method=="POST":
           username=request.POST['username']
           password1=request.POST['password1']
           password2=request.POST['password2']
           section=request.POST['section']
           email=request.POST['email']
           first_name=str(section)
           last_name=request.user.get_username()

           if password1==password2:
              if User.objects.filter(username=username).exists():
                           messages.info(request,"Username is already taken!")
                           return redirect('addemp')
              elif User.objects.filter(email=email).exists():
                           messages.info(request,"Email id is already taken!")
                           return redirect('addemp')
              elif len(password1)<8:
                           messages.info(request,"Password length must be greater then 7")
                           return redirect('addemp')

              else:
                             user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password1)
                             user.is_active = True
                             user.save();
                             messages.info(request,"Employee Created ...")
                             return redirect('addemp')
           else:
              messages.info(request,"password not maching")
              return redirect('addemp')
        else:
                shop=Profile.objects.get(user=request.user)
                sec = Section.objects.filter(user=shop.user).values()
                dist={
                "shop":shop,
                "sec":sec
                }
                return render(request,'addemp.html',dist)
    else :
       messages.info(request,"Login to enter")
       return redirect("login")

def addSection(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method=="POST":
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                section_name=request.POST['section_name']
                img=form.cleaned_data.get('img')
                section_disc=request.POST['section_des']
                user=request.user
                obj=Section(user=user,section_name=section_name,description=section_disc,img=img)
                obj.save()
                messages.info(request,"section added")
                return redirect("addsection")
            else:
                 messages.info(request,"Select proper image")
                 return redirect("addsection")




        form = ProfileForm()
        shop=Profile.objects.get(user=request.user)
        dist={"shop":shop,"form":form}
        return render(request,'addsection.html',dist)
    else :
       messages.info(request,"Login to enter")
       return redirect("login")
# Create your views here.
def home(request):
 if request.user.is_authenticated :

    if request.method=="POST":
        search=request.POST['search']
        #query="select  * from first_Profile where shop_name like '%"  + search  +   "%' "
        shops=Profile.objects.filter(shop_name__contains=search)
        #shops=Profile.objects.raw(query)

        if len(shops)!=0:
           res="Search Results : "+str(search)
        else :
           res ="No Results found on "+str(search)
        dist={'shops':shops,
               'topic':res}
        return render(request,'Trend.html',dist)

    shops=Profile.objects.filter(checked=True).all()
    res="Trending Shops And Offers"

    dist={'shops':shops,"topic":res}
    return render(request,'Trend.html',dist)
 else:
    messages.info(request,"Login to enter")
    return redirect("login")

def page(request,id=None):
 if request.user.is_authenticated:

    data=Profile.objects.get(id=id)
    #user = User.objects.get(id=id)
    sec = Section.objects.filter(user=data.user)
    #sec=Section.objects.get(id=4)
    print(sec)
    dist={
    'data':data,
    'sec':sec
    }
    return render(request,"shop.html",dist)
 else:
     messages.info(request,"Login to enter ")
     return redirect("login")


def logout(request):
    auth.logout(request)
    return redirect("index")


def index(request):
    if request.user.is_authenticated:
             return redirect("home")
    return render(request,'title.html')


def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None :
            auth.login(request,user)
            if user.get_short_name()=='shop':
                    return redirect('shopadmin')
            if user.get_short_name()!='shop' and user.get_short_name()!='Custom':
                return redirect('empcalllog')
            return redirect('home')
        else:
            messages.info(request,"Username or Password is wrong")
            return redirect("login")

    return render(request,"Login.html")

#function for Category (user / employer)
def choose_cat(request):
    return render(request,"b4_SignUp.html")

def new_shop_signup(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.info(request,"Thank you for registation ,We contant you soon !")
            return redirect('shop_signup')
    else:
        form = ProfileForm()
    return render(request, 'shop_cre.html', {'form' : form})


def shop_signup(request):
    if request.method=='POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            shop_name=request.POST['shopname']
            username=request.POST['username']
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
                    user.is_active = True

                    user.save();
        #phoneno bio location img dist

                    phoneno=request.POST['phoneno']
                    bio=request.POST['bio']
                    location=request.POST['location']
                    img1=form.cleaned_data.get('img')   #name = form.cleaned_data.get("name")

                    #img1="img/"+img1
                    print("%%%%%%%%%%%%%%%%%5")
                    print(img1)
                    print("&&&&&&&&&&&&&&&&&&&&&&")
                    dist=request.POST['dist']

                    obj=Profile(user=user,bio=bio,location=location,dist=dist,phone_no=phoneno,img=img1,shop_name=shop_name)
                    obj.save();

                    messages.info(request,"Thank you for registation ,We contant you soon !")
                    return redirect('shop_signup')

            else:
                messages.info(request,"password not maching")
                return redirect('shop_signup')

    form = ProfileForm()

    return render(request,"shop_cre.html",{"form":form})

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
                  #send_emailto(email) #sending email
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
