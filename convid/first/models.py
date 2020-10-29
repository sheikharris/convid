from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=600,default="bio of this shop will be show here.")
    location = models.CharField(max_length=300, default="Location")
    dist = models.CharField(max_length=300, default="Location")
    phone_no = models.IntegerField(null=True, default=1231231231)
    img=models.ImageField(upload_to='img/')
    status=models.BooleanField(default=False)
    shop_name=models.CharField(max_length=300, default="shop name")
    checked=models.BooleanField(default=False)


    def __str__(self):
        return self.shop_name

class Section(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,unique=False)
    section_name=models.CharField(max_length=150, default="Section name")
    description= models.TextField(max_length=600,default="Section description")
    img=models.ImageField(upload_to='img/')
    status=models.BooleanField(default=True)
