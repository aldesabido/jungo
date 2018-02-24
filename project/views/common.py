from django.shortcuts import render, get_object_or_404,redirect
from django.utils.dateparse import parse_date
from django.db import models
from django.db.models import Count, Sum, Avg,Min,Q,F,Func
from math import ceil,floor
from django.http import HttpResponse,JsonResponse,StreamingHttpResponse
from random import randint
from datetime import datetime,timedelta,date
from copy import copy
import math,json,time,datetime as idatetime,copy as icopy,decimal,ast,csv,os,copy,re
from django.core import serializers
from operator import itemgetter
from decimal import Decimal
from time import mktime
from django.utils.termcolors import colorize
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import smart_str
from django.conf import settings
from collections import OrderedDict
from django.db.models.functions import Coalesce
from django.forms.models import model_to_dict
from django.utils import timezone


'''
	Just like a Decimal() function but changes the None into 0
'''
class DDecimal(Decimal) :
    def __new__ (self,value=0):
    	if value == None or value == False:
    		value = 0
    	return Decimal(value)



'''
	Decimal and Date Encoder
'''
class DecimalDateEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, Decimal):
			return round(2)

		if isinstance(obj, idatetime.date):
			if isinstance(obj, datetime):
				return str(obj)
			else:
				return str(obj)

		return json.JSONEncoder.default(self, obj)

def post_data(request):
	post_params = json.loads(request.body.decode("utf-8")) if request.body.decode("utf-8") else {}
	return post_params

'''
	colored print in terminal
	str_to_print = The string that you want to print
	fg = color of the text (optional) (default to red)
	bg = background color of the text (optional) (default to white)
'''
def cprint(str_to_print, fg = "white", bg = "blue"):
	print(colorize(str_to_print, fg=fg, bg=bg))

def eprint(string, fg="white", bg="blue"):
	print ("======================================")
	print (colorize(string, fg=fg, bg=bg))
	print ("======================================")

def dprint(string):
	print ("======================================")
	print (string)
	print ("======================================")

'''
	Gets the current date and return depends on what format you want to return
'''

def current_date(to_return = None):
	if to_return == 'month':
		return datetime.today().month
	elif to_return == 'year':
		return datetime.today().year
	elif to_return == 'day':
		return datetime.today().day
	else:
		return datetime.today().date()


	
'''
	just call this function for testing stopper
	instead of calling raise ValueError('test'), just use raise_error() function
'''

def raise_error(msg = "Testing Stopper",is_json_dump = False):
	if is_json_dump:
		msg = json.dumps(msg)
	raise ValueError(msg)

def success_list(to_return_list, to_list = True):
	if to_list:
		to_return_list = to_return_list if to_return_list else []
		to_return_list = list_dates_to_str(to_return_list)
	else:
		to_return_list = to_return_list if to_return_list else {}
		to_return_list = obj_dates_to_str(to_return_list)
	to_return_list = json_encode(to_return_list,to_list)
	return HttpResponse(to_return_list, status = 200)

def success_obj(listt):
	listt = listt if listt else {}
	return HttpResponse(json_encode(listt), status = 200)

def success(to_return = "Successfully saved."):
	return HttpResponse(to_return, status = 200)

def error_list(listt):
	listt = listt if listt else []
	return HttpResponse(json_encode(listt), status = 400)

def error_obj(listt):
	listt = listt if listt else {}
	return HttpResponse(json_encode(listt), status = 400)

def error(to_return = "Something went wrong. Please contact your admin."):
	try:
			
		'''
			If the error is an array of an object, just show the first array index of the first object.
		'''
		has_dict = False
		first_error = None
		for str_return in to_return:
			try:
				dict_return = ast.literal_eval(str_return)
				has_dict = True
				firstkey = str_beautify(dict_return.iterkeys().next())
				firstkeyvalue = str_beautify(dict_return.itervalues().next()[0])
				first_error = firstkeyvalue
				if firstkey not in ["all","All","  all  "]:
					first_error = firstkey+" : "+firstkeyvalue
				else:
					exploded = 	first_error.split('with this client and ')
					if len(exploded) > 1:
						first_error = str_beautify(exploded[1])
				continue
			except Exception as e:
				has_dict = False

		if has_dict:
			to_return = first_error
		else:
			to_return = str_beautify(to_return)
			print(to_return)

		return HttpResponse(to_return, status = 400)
	except Exception as e:
		print(e)
		return HttpResponse(to_return, status = 400)


#If the key value is obj, set the id.
def clean_obj(data,array_field = False):
	try:
		for key in data:
			if isinstance(data[key], dict):
				if 'id' in data[key]:
					data[key] = data[key]['id']

		if array_field:
			for key in data:
				if isinstance(data[key], list):
					data[key] = list2str(values_list(data[key]))

		return data
	except Exception as e:
		print(e)

def list2str(arr,separator=","):
	return separator.join(map(str, arr))


def str_beautify(str_to_convert,delimeter = "_"):
	str_to_convert = str(str_to_convert)
	to_return = str_to_convert.replace ("__", "")
	to_return = to_return.replace ("_", " ")
	return to_return.capitalize()


'''
	instead of using json.dumps(list(list_value)) you can use json_encode()
'''

def json_encode(var_list,use_list_function = True):
	if use_list_function:
		var_list = list(var_list)

	return json.dumps(var_list, cls = DecimalDateEncoder)


'''
	lists = a list that contains date(s) that needs to be converted into string
	remove_time = Defaults to True; if false, leave the date as is.
	TODO: needs to remove date_resolved and replace it to dynamic type date
'''

def list_dates_to_str(lists):
	results = []
	for value in lists:
		if isinstance(value,dict):
			results.append(obj_dates_to_str(value))
		else:
			results.append(value)

	return results

def obj_dates_to_str(objs,remove_time = False):
	try:
		for key,value in objs.items():
			if isinstance(objs[key], idatetime.date):

				if isinstance(objs[key], datetime) and remove_time:
					objs[key] = str(objs[key].date())
				else:
					objs[key] = str(objs[key].strftime("%Y-%m-%d %I:%M:%p"))

		objs = obj_decimal_to_float(objs)
		return objs
	except Exception as e:
		raise ValueError(e)

def list_decimal_to_float(lists):
	results = []
	for value in lists:
		results.append(obj_decimal_to_float(value))

	return results

def obj_decimal_to_float(objs):
	try:
		for key,value in objs.items():
			if isinstance(objs[key], decimal.Decimal):
				objs[key] = float(objs[key])

		return objs
	except Exception as e:
		raise ValueError(e)


'''
	Calculate the total_records,total_pages and the start and end of the query.
'''
def generate_sorting(sort_dict = None):
	if not sort_dict:
		sort_dict = {"sort_by" : "id","reverse" : False}

	sort_by = sort_dict.get("sort_by","id")
	if not sort_dict.get("reverse",False):
		return [sort_by,"id"]

	sort_by = "-"+sort_by
	return [sort_by,"-id"]

def generate_pagination(pagination_data,records):
	page = pagination_data["current_page"] - 1
	page_size = pagination_data["limit"]
	total_records = records.count()
	total_pages   = ceil(float(total_records) / page_size)
	starting = page * page_size 
	ending = page_size + starting
	dictt = {
		"total_records" : total_records,
		"total_pages" : total_pages,
		"starting" : starting,
		"ending" : ending,
	}
	return dictt

'''
	{"is_deleted" : True, "company" : "company_id_here"} if and
		{"and" : [{"is_deleted" : True},{"company" : "company_id_here"}]}
'''
def objs_to_and_for_q(filters = {},obj_to_transform = {},type="and"):
	if type not in filters:
		filters[type] = []
	for key in obj_to_transform.keys():
		row = {}
		row[key] = obj_to_transform[key];
		filters[type].append(row)

	return filters

def filter_obj_to_q(obj,or_q = ()):
	q_filters = Q()
	for value in obj.iteritems():
		if value[0] in or_q:
			q_filters |= Q((value[0],value[1]))
		else:
			q_filters &= Q((value[0],value[1]))

	return q_filters
	