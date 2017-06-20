# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
import serial, pickle, os, time
import serial.tools.list_ports
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RenameForm


SNo = '756333130333512092F1'	#Arduino Serial Number
DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Relay states when starting server ...
state = {'relay1' : False, 'relay2' : False, 'relay3' : False, 'relay4': False, 'relay5': True}
base_ip = 'http://192.168.12.1'

name_file = open(os.path.join(DIR, 'controller/names.dat'), "wb")
names = {'name1':'Appliance 1', 'name2':'Appliance 2', 'name3':'Appliance 3', 'name4':'Appliance 4',}
pickle.dump(names, name_file)
name_file.close()

def read_names():
	name_file = open(os.path.join(DIR, 'controller/names.dat'), "rb")
	names = pickle.load(name_file)
	name_file.close()
	for x in names:
		if len(names[x])<12:
			names[x] += " "*(12-len(names[x]))
	return names

def find_arduino(SN):
	for pinfo in serial.tools.list_ports.comports():
		if pinfo.serial_number == SN:
			return serial.Serial(pinfo.device)
serial_port = find_arduino(SNo)


class CommandExecutor(LoginRequiredMixin, View):
	def get(self, request, slug,  *args, **kwargs):	# 'slug' is the command recieved
		serial_port.write(str(slug))
		if slug in '1 2 3 4 5'.split():
			state['relay'+slug] = not state['relay'+slug]
		names = read_names()
		return HttpResponseRedirect(base_ip+"/control/")

class Renamer(LoginRequiredMixin, View):
	def get(self, request, slug,  *args, **kwargs):	# 'slug' is the command recieved
		'''slug is of the form    name1-XXXXXXXXXX'''
		name_file = open(os.path.join(DIR, 'controller/names.dat'), "rb")
		names = pickle.load(name_file)
		name_file.close()

		x = slug.split("-")
		if x[0] in 'name1name2name3name4':
			names[x[0]] = x[1]

		name_file = open(os.path.join(DIR, 'controller/names.dat'), "wb")
		pickle.dump(names, name_file)
		name_file.close()
		serial_port.write(('%s%s' %({'name1':'rena', 'name2':'renb', 'name3':'renc', 'name4':'rend', }[x[0]],x[1])).encode('latin-1'))
		return HttpResponseRedirect('/control')


class Renamer_selector(LoginRequiredMixin, View):
	def get(self, request, slug,  *args, **kwargs):	# 'slug' is the command recieved
		name_file = open(os.path.join(DIR, 'controller/names.dat'), "rb")
		names = pickle.load(name_file)
		name_file.close()
		form = RenameForm(('name%d' %(int(slug))))
		#form.save(('name%d' %(int(slug))))
		context={'appliance':names['name%d' %(int(slug))], 'form':form,}
		return render(request, "rename.html", context)

	def post(self, request, *args, **kwargs):
		print request.POST, 
		return HttpResponseRedirect("/rename/name%d-%s"%(int(kwargs['slug']), request.POST['new_name']))


class Controller(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):	# 'slug' is the command recieved
		names = read_names()
		context={'url1' : base_ip+"/command/1", 'url2' : base_ip+"/command/2", 'url3' : base_ip+"/command/3", 'url4' : base_ip+"/command/4", 'url5' : base_ip+"/command/5" , 'name1' : names['name1'], 'name2' : names['name2'], 'name3' : names['name3'], 'name4' : names['name4'],'btn1state':'checked' if state['relay1'] else '', 'btn2state':'checked' if state['relay2'] else '', 'btn3state':'checked' if state['relay3'] else '', 'btn4state':'checked' if state['relay4'] else '', 'btn5state':'checked' if state['relay5'] else ''}
		return render(request, "control.html", context)

class HomeView(View):
	def get(self, request, *args, **kwargs):
		print("At Home Now!")
		return HttpResponseRedirect(base_ip+"/control/")