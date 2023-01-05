from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class MyManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("User must have an eamil address")
        if not username:
            raise ValueError("User must have an username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,username,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class LoginData(AbstractBaseUser):
    username = models.CharField(max_length=30)
    email = models.EmailField(verbose_name="email",max_length=255,unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login",auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=16,default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyManager()

    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self,perm,obj=None):
        return True


class item (models.Model):
    name = models.CharField(max_length = 120,default="")
    discription = models.JSONField()
    price = models.IntegerField(default=0)
    in_stock = models.IntegerField(default=0)
    img = models.ImageField(upload_to='',default="")
    def __str__(self):
        return  f'{self.name} - {self.price}'

class cart(models.Model):
    userId = models.ForeignKey(LoginData,on_delete=models.CASCADE, default="")
    nameId = models.ForeignKey(item,on_delete=models.CASCADE)
    number = models.IntegerField()
    def __str__(self):
        return f'{self.nameId} - {self.number}'

class address(models.Model):
    userId = models.ForeignKey(LoginData,on_delete=models.CASCADE, default="")
    Full_Name = models.CharField(max_length= 120, blank=False)
    Mobile_number = models.CharField(max_length= 20, blank=False)
    Pincode = models.CharField(max_length= 6, blank=False)
    House_no_or_Building = models.CharField(max_length= 120, blank=False)
    Area = models.CharField(max_length= 120, blank=False)
    Landmark = models.CharField(max_length= 120)
    Town_or_City = models.CharField(max_length= 120)
    State = models.CharField(max_length= 120)
    
class order(models.Model):
    userId = models.ForeignKey(LoginData,on_delete=models.CASCADE, default="")
    address = models.CharField(max_length= 1000)
    number = models.IntegerField()
    nameId = models.ForeignKey(item,on_delete=models.CASCADE)


