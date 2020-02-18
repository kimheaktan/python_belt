from django.db import models
from django.contrib import messages
from django.contrib.messages import get_messages
import re

class UserManager(models.Manager):
    def reg_valid(self, request):
        if len(request.POST['password']) < 8:
            messages.error(request, "Password must consist of at least 8 characters")

        if request.POST["password"] != request.POST["password_confirm"]:
            messages.error(request, "Password must match confirm password")

        if len(request.POST["first_name"]) < 3:
            messages.error(request, "First Name must be at least 3 characters")

        if len(request.POST["last_name"]) < 3:
            messages.error(request, "Last Name must be at least 3 characters")

        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(request.POST['email']):
            messages.error(request,'Invalid email address!')

        storage = messages.get_messages(request)
        storage.used = False
        return len(storage) == 0

class JobManager(models.Manager):
    def job_valid(self, request):
        # if len(request.POST['title']) < 1:
        #     messages.error(request, 'A job must be provided')

        if len(request.POST['title']) < 3:
            messages.error(request, "A job must consist of at least 3 characters")

        if len(request.POST['description'])  < 1:
            messages.error(request, "A description must be provided")

        if len(request.POST['description']) < 3:
            messages.error(request,'A description must consister of at least 3 characters')

        if len(request.POST['location'])  < 1:
            messages.error(request, "A location must be provided")

        if len(request.POST['location']) < 3:
            messages.error(request,'A location must consister of at least 3 characters')

        storage = messages.get_messages(request)
        storage.used = False
        return len(storage) == 0

class EditJobManager(models.Manager):
    def edit_valid(self, request):

        if len(request.POST['edit_title']) < 3:
            messages.error(request, "A new job must consist of at least 3 characters ")

        if len(request.POST['edit_description']) < 3:
            messages.error(request, "A new description must be at least 3 characters")

        if len(request.POST['edit_location']) < 3:
            messages.error(request, "A new location must be at least 3 characters")
            
        storage = messages.get_messages(request)
        storage.used = False
        return len(storage) == 0


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255) 
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    creater = models.ForeignKey(User,related_name='created_jobs')
    got = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    objects = JobManager()

class EditJob(models.Model):
    objects = EditJobManager()