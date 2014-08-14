from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

class Notification(models.Model):
    title=models.CharField(max_length=100)
    message=models.TextField()
    viewed=models.BooleanField(default=False)
    acting_user=models.CharField(max_length=100)
    time=models.DateTimeField()
    def __unicode__(self):
        return self.message

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    Notifications = models.ManyToManyField(Notification,blank=True,null=True)

    def __unicode__(self):
        return self.user.username


class Product(models.Model):
    title=models.CharField(max_length=150,blank=True)
    image1=models.ImageField(upload_to= 'item_image',blank=True)
    image2=models.ImageField(upload_to= 'item_image',blank=True,null=True)
    image3=models.ImageField(upload_to= 'item_image',blank=True,null=True)
    description=models.CharField(max_length=1000)
    price=models.FloatField(blank=True)
    time=models.DateTimeField('date last edited',blank=True)
    
    owner=models.ForeignKey(UserProfile,related_name="owner of Product",blank=True,null=True)
    
    subscribers=models.ManyToManyField(UserProfile,related_name="list of subscribers",blank=True,null=True) 
    placed_users=models.ManyToManyField(UserProfile,related_name="for placed_users",blank=True,null=True)
    
    def __unicode__(self):
        return self.title
