from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns=[

   path('',views.index,name="index"),
   path('login',views.login,name="login"),
   path('cat_signup',views.choose_cat,name="cat_signup"),
   path('shop_signup',views.shop_signup,name="shop_signup"),
   path('signup',views.signup,name="signup"),
   path('trend',views.home,name="home"),
   path('page/<int:id>',views.page,name="page"),
   path('logout',views.logout,name="logout"),
   path('aboutus',views.aboutus,name="aboutus"),
   path('contactus',views.contactus,name="contactus"),
   path('shopadmin',views.shopAdmin,name='shopadmin'),
   path('addemp',views.addEmp,name='addemp'),
   path('addsection',views.addSection,name='addsection'),
   path('viewemp',views.viewEmp,name='viewemp'),
   path('viewsection',views.viewsection,name='viewsection'),
   path('openshop',views.openshop,name='openshop'),
   path('closeshop',views.closeshop,name='closeshop'),
   path('deletesection/<int:id>',views.deletesection,name="deletesection"),
   path('deleteemp/<int:id>',views.deleteemp,name="deleteemp"),
   path('editsection/<int:id>',views.editsection,name="editsection"),
   path('editemp/<int:id>',views.editemp,name="editemp"),
   path("empcalllog",views.empcalllog,name="empcalllog"),
   path("addorder",views.addorder,name="addorder"),






]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
