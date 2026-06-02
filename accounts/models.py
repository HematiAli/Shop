from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from .validators import avatar_upload_path
"""
python manage.py check
"""
class User(AbstractBaseUser, PermissionsMixin):#after AbstractBaseUser next step go to admin add to permissions => group,user_permissions
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager() # باید منیجر رو به مدلم معرفی کنم
    USERNAME_FIELD = "phone_number" # کاربر ها رو براین اساس اعبار سنجی کن ..Should be unique
    REQUIRED_FIELDS = ['email', 'full_name'] #وقتی کریت سوپریوز زدم اینارو ازش بپرس

    def __str__(self):
        return self.email #by default return username_field
    

    

    @property
    def is_staff(self):
        return self.is_admin



class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=avatar_upload_path)

    def __str__(self):
        return self.user.full_name
    


#otp:one time password
class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.phone_number} - {self.code} - {self.created}"
    