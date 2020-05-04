from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.postgres.fields import ArrayField

# Create your models here.


class User(AbstractUser):
	profilePics = models.FileField(upload_to="ProfilePic/", default="default.jpg")
	phonenum = models.TextField()
	job_title = models.CharField(max_length=20)
	job_description = models.CharField(max_length=200)
	about = models.TextField()
	resume = models.FileField(upload_to="Resume/")
	nationality = models.CharField(max_length=20)
	contact_address = models.CharField(max_length=100)
	# checkNote = models.BooleanField(default=True)
	# certificates = ArrayField(models.CharField(max_length=100), blank=True)
	# skills = ArrayField(models.CharField(max_length=100), blank=True)

	def __str__(self):
		return self.username


class Project(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=35)
	picture = models.FileField(upload_to="ProjectPic/", default="defaultproject.jpg")
	short_desc = models.CharField(max_length=500)
	full_desc = models.TextField()
	pub_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

class Comment(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	pub_date = models.DateTimeField(auto_now_add=True)
	comment = models.CharField(max_length=1000, default=None)


	def __str__(self):
		return self.author.first_name, '-', self.author.last_name

class View(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	user = models.CharField(max_length=100)

class Contact(models.Model):
	name = models.CharField(max_length=500)
	email = models.EmailField()
	message = models.TextField()
	pub_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

# class Notification(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
# 	message = models.CharField(max_length=500)
# 	slug = models.SlugField(max_length=200)
# 	active = models.BooleanField(default=True)
# 	pub_date = models.DateTimeField(auto_now_add=True)