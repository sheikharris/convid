from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

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



]


from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
