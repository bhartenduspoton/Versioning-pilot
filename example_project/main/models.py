from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime


class Project(models.Model):
    user = models.ForeignKey(User)
    customerID=models.IntegerField(default=1,null=False,blank=False)
    projectID=models.IntegerField(default=1,null=False,blank=False)
    projectName=models.CharField(default='default',max_length=200,null=False,blank=False)
    date = models.DateTimeField(auto_now_add=True, blank=True)


class UserData(models.Model):
    project = models.ForeignKey(Project)
    version = models.IntegerField(default=1,null=True,blank=True)
    file_path=models.CharField(blank=True,max_length=200, null=True)
    processed = models.BooleanField(blank=True,default=False)
    excelsheet = models.FileField(upload_to='documents/')
    file_name=models.CharField(blank=True,max_length=200, null=True)
    comments = models.CharField(blank=True,max_length=1000, null=True)
    created_on =   models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_on =   models.DateTimeField(auto_now=True, auto_now_add=False)
    
    

    

class Comment(models.Model):
    UserData = models.ForeignKey(UserData)  
    comments = models.CharField(blank=True,max_length=1000, null=True)


class Upload(models.Model):
    docfile = models.FileField(upload_to='documents/')
