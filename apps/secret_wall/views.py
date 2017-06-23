# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Secret


# Create your views here.
def index(request):
	if 'user_id' in request.session:
		return redirect('/success')
	return render(request, 'secret_wall/index.html')

def register(request):
	result = User.objects.register(request.POST)
	if isinstance(result, list):
		for err in result:
			messages.add_message(request, messages.ERROR, err)
		return redirect('/')
	else:
		request.session['user_id'] = result.id
		return redirect('/success')

def login(request):
	result = User.objects.login(request.POST)
	if isinstance(result, list):
		for err in result:
			messages.add_message(request, messages.ERROR, err)
		return redirect('/')
	else:
		request.session['user_id'] = result.id
		return redirect('/success')

def success(request):
	if 'user_id' not in request.session:
		return redirect('/')
	user = User.objects.get(id=request.session['user_id'])
	context = {
		'username': user.first_name
	}
	return render(request, 'secret_wall/secrets.html', context)

def new_secret(request):
	return redirect('/success')

def logout(request):
	request.session.flush()
	return redirect('/')
