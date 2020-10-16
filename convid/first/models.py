from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=600,default="bio of this shop will be show here.")
    location = models.CharField(max_length=300, default="Location")
    dist = models.CharField(max_length=300, default="Location")
    phone_no = models.IntegerField(null=True, default="phone number")
    img=models.ImageField(upload_to='pic')
    status=models.BooleanField(default=False)

    def __str__(self):
        return self.bio
