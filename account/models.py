from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    image = models.ImageField(upload_to='profiles_pics', default='defaultprofilepic.jpg')
    password_reset_code = models.CharField(max_length=6,default="")

    def __str__(self):
        return self.user.first_name