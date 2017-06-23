# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
	def validate(self, data):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
		NAME_REGEX = re.compile(r'^[0-9]+$')
		errors = []
		for item in data:
			if len (data[item]) < 1:
				errors.append(item.replace("_", " ").title() + " is a required field")
		if len(data['first_name']) < 2 or len(data['last_name']) < 2:
			errors.append("First Name and Last Name must be at least 2 characters long")
		if not data['first_name'].isalpha():
			errors.append("First name must contain only letters")
		if not data['last_name'].isalpha():
			errors.append("Last name must contain only letters")
		


		return errors


class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	Password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.email

	objects = UserManager()
