from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.admin.utils import flatten
from .models import Domain, MXrecord, NSrecord
import dns.resolver
import dns.reversename
from resolver.mxrules import *
from resolver.nsrules import *
import csv
import io

# 	

def index(request):
	return render(request, 'index.html')

def compute(request):

### Gets Raw data from input and cleans for processsing	

	### check box list
	# if request.method == 'POST':
 #    records  = request.POST.getlist('records ')
 	# for val in record val:


	domain_val = request.POST['domains']
	record_val = request.POST['records']
	delimitor = request.POST['delimitor']
	domain_list=domain_val.split(delimitor) # cleaned list of domains 
    

    ### pulls up dns records
	def get_records(domain):
	# import dns.resolver
		final_answers=[]

		try:
			answers=dns.resolver.resolve(domain, record_val)
			for value in answers:
				final_answers.append(value.to_text())			
		except Exception as e:
			final_answers.append(e)
		return final_answers

	### IF PTR record - processe ip to get pter record

	def get_ptr(address):
		final_answers=[]
		try:
			domain_address = dns.reversename.from_address(address)
			ptr_record = dns.resolver.resolve(domain_address, 'PTR')[0]
			final_answers.append(ptr_record)
		except Exception as e:
			final_answers.append(e)
		return final_answers


	
### finalizes object for output to frontend

	
	obj_list = []

	### creates objects for PTR record

	if record_val == 'PTR':
		for obj in domain_list:
			record_result = get_ptr(obj)
			obj = Domain( record_name = obj, record_type= record_val, record_result =  record_result, status = '' , comment = '' )
			obj_list.append(obj)





	### create objects for MX records and applies rules
	elif record_val == 'MX':

		for obj in domain_list:
			record_result = get_records(obj)
			mx_objects = mx_create(record_result)
			stat_and_comm = mx_rules(mx_objects)
			obj = Domain( record_name = obj, record_type= record_val, record_result =  record_result, status = stat_and_comm[0], comment = stat_and_comm[1] )
			obj_list.append(obj)

	### create objects for NS records and applies rules

	elif record_val == 'NS':

		for obj in domain_list:
			record_result = get_records(obj)
			ns_objects = ns_create(record_result)
			stat_and_comm = ns_rules(ns_objects)
			obj = Domain( record_name = obj, record_type= record_val, record_result =  record_result, status = stat_and_comm[0], comment = stat_and_comm[1] )
			obj_list.append(obj)


	### create objects for domains and records with no rules
	else:
		for obj in domain_list:
			record_result = get_records(obj)
			# mx_objects = mx_create(record_result)
			# stat_and_comm = mx_rules(mx_objects)
			obj = Domain( record_name = obj, record_type= record_val, record_result =  record_result, status = '' , comment = '' )
			obj_list.append(obj)


		

	return render(request, 'result.html', { 

	'record_val' : record_val, 
		# 'output' : output, 
	'domain_list' : domain_list, 
	
	# 'record_result' : record_result,
	# 'end_result' : end_result, 
	'obj_list' : obj_list, 
	
	

	 })
# Create your views here.

def compute_csv(request):
	if request.method=='POST':
		csv_file = request.FILES['csv_file']
		record_val = request.POST['records']

	def process_csv(csv_file):
		domain_list = []
		csvf = io.TextIOWrapper(csv_file, encoding="utf-8", )
		reader = csv.reader(csvf, )
		for value in reader:
			domain_list.append(value)
		return flatten(domain_list)

	


	
	domain_list = process_csv(csv_file)

	### pulls up dns records
	def get_records(domain):
	# import dns.resolver
		final_answers=[]

		try:
			answers=dns.resolver.resolve(domain, record_val)
			for value in answers:
				final_answers.append(value.to_text())			
		except Exception as e:
			final_answers.append(str(e))
		return final_answers

	### IF PTR record - processe ip to get pter record

	def get_ptr(address):
		final_answers=[]
		try:
			domain_address = dns.reversename.from_address(address)
			ptr_record = dns.resolver.resolve(domain_address, 'PTR')[0]
			final_answers.append(ptr_record)
		except Exception as e:
			final_answers.append(str(e))
		return final_answers


	
### finalizes object for output to frontend

	
	obj_list = []

	### creates objects for PTR record

	if record_val == 'PTR':
		for obj in domain_list:
			record_result = get_ptr(obj)
			obj = Domain( record_name = obj, record_type= record_val, record_result =  record_result, status = '' , comment = '' )
			obj_list.append(obj)





	### create objects for MX records and applies rules
	elif record_val == 'MX':

		for obj in domain_list:
			record_result = get_records(obj)
			mx_objects = mx_create(record_result)
			stat_and_comm = mx_rules(mx_objects)
			obj = Domain( record_name = obj, record_type= record_val, record_result =  record_result, status = stat_and_comm[0], comment = stat_and_comm[1] )
			obj_list.append(obj)

	### create objects for NS records and applies rules

	elif record_val == 'NS':

		for obj in domain_list:
			record_result = get_records(obj)
			ns_objects = ns_create(record_result)
			stat_and_comm = ns_rules(ns_objects)
			obj = Domain( record_name = obj, record_type= record_val, record_result =  record_result, status = stat_and_comm[0], comment = stat_and_comm[1] )
			obj_list.append(obj)


	### create objects for domains and records with no rules
	else:
		for obj in domain_list:
			record_result = get_records(obj)
			# mx_objects = mx_create(record_result)
			# stat_and_comm = mx_rules(mx_objects)
			obj = Domain( record_name = obj, record_type= record_val, record_result =  record_result, status = '' , comment = '' )
			obj_list.append(obj)


	str_record_result = ''.join(obj.record_result)
	response = HttpResponse(content_type = 'text/csv')
	writer  = csv.writer(response)
	writer.writerow(['domain' , 'DNS record', 'status' , 'comment'])
	for obj in obj_list:
		writer.writerow( [obj.record_name, str_record_result, obj.status, obj.comment] )
	response['Content-Disposition'] = 'attachment; filename="result.csv"'


	

	return response






                            




