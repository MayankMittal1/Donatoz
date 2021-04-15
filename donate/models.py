from enum import Flag
from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.

class Organization(models.Model):
    id=models.AutoField(primary_key=True)
    email=models.EmailField(unique=True)
    name=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    address=models.TextField(blank=True)
    pincode=models.CharField(max_length=10,blank=True)
    image=models.ImageField(upload_to='profile_image_organization/',null=True, blank=True, default='userdefault.png')
    balance=models.PositiveIntegerField(default=0)
    phonenumber=models.CharField(max_length=12)

class User(models.Model):
    id=models.AutoField(primary_key=True)
    firstName=models.CharField(max_length=50)
    lastName=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=50)
    image=models.ImageField(upload_to='profile_image_user/',null=True, blank=True, default='userdefault.png')
    donated=models.PositiveIntegerField(default=0)
    phonenumber=models.CharField(max_length=12)
    gender=models.TextField(blank=True)
    dob=models.TextField(blank=True)
    organizations=models.ManyToManyField(Organization,related_name="organization")

class Transaction(models.Model):
    id=models.AutoField(primary_key=True)
    type=models.CharField(max_length=10, null=False)
    description=models.CharField(max_length=120, blank=True, null=True)
    amount=models.BigIntegerField(max_length=10)
    organization=models.ForeignKey(Organization,on_delete=CASCADE)
    user=models.ForeignKey(User,on_delete=CASCADE,null=True,blank=True)
    timestamp=models.DateTimeField(auto_now=True)