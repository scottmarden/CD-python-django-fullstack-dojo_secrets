# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
	return render(request, 'secret_wall/index.html')

def register(request):
	result = User.objects.validate(request.POST)
	if isinstance(result, list):
		print "WE GOT ERRORS!"
		for err in result:
			messages.add_message(request, messages.ERROR, err)
	return redirect('/')
