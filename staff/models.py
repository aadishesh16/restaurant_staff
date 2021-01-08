from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render,redirect
from django.utils import timezone

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username,password=None,**kwargs):
		if not email:
			raise ValueError('Users must have an email address')


		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password,**kwargs):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,)

		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True

		user.save(using=self._db)
		return user




class NewUser(AbstractBaseUser):
    email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
    username 				= models.CharField(max_length=30, unique=True)
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    restaurant_admin		= models.BooleanField(default=False)
    hiring_manager			= models.BooleanField(default=False)
    restaurant 				= models.CharField(max_length=100)
    location 				= models.CharField(max_length=100)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
	    return self.email

    def has_perm(self, perm, obj=None):
	    return self.is_admin

    def has_module_perms(self, app_label):
	    return True
    def save(self, *args, **kwargs):
	    self.location = self.location.upper()
	    return super(NewUser, self).save(*args, **kwargs)


class JobPosting(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='job_content_type')
	location = models.CharField(max_length=100)
	title= models.CharField(max_length=200)
	description = models.TextField()
	restaurant= models.CharField(max_length=120)
	date_posted = models.DateTimeField(default=timezone.now)


	def __str__(self):
		return self.title



	def get_absolute_url(self):
		return reverse('joblist-detail', kwargs= {'pk':self.pk})
	def save(self, *args, **kwargs):
	    self.location = self.location.upper()
	    return super(JobPosting, self).save(*args, **kwargs)


class Restaurant(models.Model):
	rest_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='restaurant_content_type')
	rest_name = models.CharField(max_length=100)
	location  = models.CharField(max_length=100)

	def __str__(self):
		return self.rest_name

	def save(self, *args, **kwargs):
	    self.location = self.location.upper()
	    return super(Restaurant, self).save(*args, **kwargs)

class JobApplication(models.Model):
	job_desc = models.ForeignKey(JobPosting,on_delete=models.CASCADE)
	job_user = models.EmailField(max_length=60)
	job_file = models.FileField(upload_to="resumes")

	def __str__(self):
		return self.job_user

