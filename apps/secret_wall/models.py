# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Count
import re, bcrypt, datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta

# Create your models here.

#------------------------------------User & Manager--------------------------
class UserManager(models.Manager):
	def register(self, data):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
		errors = []
		today = datetime.datetime.now()
		for item in data:
			if len (data[item]) < 1:
				errors.append(item.replace("_", " ").title() + " is a required field")
		if len(data['first_name']) < 2 or len(data['last_name']) < 2:
			errors.append("First Name and Last Name must be at least 2 characters long")
		if not data['first_name'].isalpha():
			errors.append("First name must contain only letters")
		if not data['last_name'].isalpha():
			errors.append("Last name must contain only letters")
		if not EMAIL_REGEX.match(data['email']):
			errors.append("Please enter a valid email address")
		try:
			User.objects.get(email = data['email'])
			errors.append("That email is already registered")
		except:
			pass
		try:
			if relativedelta(today, datetime.datetime.strptime(data['birthday'], "%Y-%m-%d")).years < 13:
				errors.append("You must be at least 13 years old to register")
			else:
				pass
		except:
			pass
		if data['password'] != data['pw_confirm']:
			errors.append("Passwords don't match!")
		if len(errors) == 0:
			hashed_pw = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
			user = User.objects.create(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], birthday=data['birthday'], password=hashed_pw)
			return user
		else:
			return errors

	def login(self, data):
		errors = []
		try:
			user = User.objects.get(email = data['email'])
			print "Found email!"
			print user.email, user.password
		except:
			print "no email"
			errors.append("Email not found")
			return errors
		if bcrypt.hashpw(data['password'].encode(), user.password.encode()) == user.password:
			print "-" * 50
			print "Good password!"
			print "-" * 50
		else:
			print "-" * 50
			print "Bad password!!"
			print "-" * 50
			errors.append("Incorrect password")
		if len(errors) == 0:
			return user
		else:
			return errors


class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	birthday = models.DateField(null=True)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.first_name

	objects = UserManager()

#------------------------------------Secret & Manager--------------------------

class SecretManager(models.Manager):
	def recent_secrets(self):
		secrets = Secret.objects.filter().annotate(num_likes=Count('likes')).order_by('-created_at')[:5]
		return secrets

	def secrets_rank(self):
		secrets = Secret.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')
		return secrets

	def post(self, new_secret, user):
		if len(new_secret) < 1:
			error = "You must enter a secret before pressing 'post'."
			return error
		else:
			new_secret = Secret.objects.create(secret=new_secret, creator=user)
		return new_secret

	def new_like(self, secret_id, user_id):
		user = User.objects.get(id=user_id)
		secret = Secret.objects.get(id=secret_id)
		result = user.liked_secrets.add(secret)
		return result

	def created_secrets(self, user_id):
		result = Secret.objects.annotate(num_likes=Count('likes')).filter(creator__id=user_id)
		return result

	def user_likes(self, user_id):
		liked_secrets = Secret.objects.annotate(num_likes=Count('likes')).filter(likes__id=user_id)
		return liked_secrets

	def unknown_secrets(self, user_id):
		unknown_secrets = Secret.objects.annotate(num_likes=Count('likes')).exclude(likes__id=user_id).exclude(creator__id=user_id)
		print unknown_secrets
		for secret in unknown_secrets:
			print secret.creator
		return unknown_secrets

class Secret(models.Model):
	secret = models.TextField()
	creator = models.ForeignKey(User, related_name="posted_secrets")
	likes = models.ManyToManyField(User, related_name="liked_secrets")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.secret

	objects = SecretManager()
