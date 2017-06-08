# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

port = "/dev/ttyACM0"	# server-arduino interface port 

class CommandExecutor(View):
	def get(self, request, slug, *args, **kwargs):	# 'slug' is the command recieved
		return HttpResponse("command recieved: "+str(slug))

class HomeView(View):
	def get(self, request, *args, **kwargs):
		return HttpResponse("At Home Now!")