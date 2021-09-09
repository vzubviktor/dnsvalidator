from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.admin.utils import flatten
from .models import Domain, MXrecord, NSrecord
import dns.resolver
import dns.reversename
from resolver.mxrules import *
from resolver.nsrules import *
from resolver.linkDomain_rules import *
import csv
import io

# 	

def index(request):
	return render(request, 'index.html')






def compute(request):

### Gets Raw data from input and cleans for processsing	

	### check box list
	

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

	
	response = HttpResponse(content_type = 'text/csv')
	writer  = csv.writer(response, lineterminator='\n')
	writer.writerow(['domain' , 'DNS record', 'status' , 'comment'])
	for obj in obj_list:
		str_record_result = '\n'.join(obj.record_result)
		writer.writerow( [obj.record_name, str_record_result, obj.status, obj.comment] )
	response['Content-Disposition'] = 'attachment; filename="result.csv"'

	return response





def compute_multi(request):
	domains = request.POST['domains']
	delimitor = request.POST['delimitor']
	domain_list= domains.split(delimitor)
	if request.method == 'POST':
		records  = request.POST.getlist('records')

	def get_records(domain, record_val):
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
			final_answers.append(e)
		return final_answers

### finalizes object for output to frontend

	obj_list = []

	### creates objects for PTR record

	def final_output(domain, record_val):
		

		if record_val == 'PTR':
			
			record_result = get_ptr(domain, record_val)
			obj = Domain( record_name = domain, record_type= record_val, record_result =  record_result, status = '' , comment = '' )
			return obj


		### create objects for MX records and applies rules
		elif record_val == 'MX':

			
			record_result = get_records(domain, record_val)
			mx_objects = mx_create(record_result)
			stat_and_comm = mx_rules(mx_objects)
			obj = Domain( record_name = domain, record_type= record_val, record_result =  record_result, status = stat_and_comm[0], comment = stat_and_comm[1] )
			return obj

		### create objects for NS records and applies rules

		elif record_val == 'NS':

			
			record_result = get_records(domain, record_val)
			ns_objects = ns_create(record_result)
			stat_and_comm = ns_rules(ns_objects)
			obj = Domain( record_name = domain, record_type= record_val, record_result =  record_result, status = stat_and_comm[0], comment = stat_and_comm[1] )
			return obj


		### create objects for domains and records with no rules
		else:
			
			record_result = get_records(domain, record_val)
			# mx_objects = mx_create(record_result)
			# stat_and_comm = mx_rules(mx_objects)
			obj = Domain( record_name = domain, record_type= record_val, record_result =  record_result, status = '' , comment = '' )
			return obj

	for domain in domain_list:
		result_list = []
		for record in records:
			result_list.append(final_output(domain, record))
		obj_list.append(result_list)

	return render(request, 'multiple.html', { 'obj_list' : obj_list })









### link subdomain and sender domain view 
def linkDomain(request):
	sender_domain = request.POST['senderDomain']
	link_subdomain = request.POST['linkDomain']
	obj_list = []
	
	### checking cname record

	def check_cname_domain(domain):
	
		final_answers=[]

		try:
			answers=dns.resolver.resolve(domain, 'CNAME')
			for value in answers:
				final_answers.append(value.to_text())			
		except Exception as e:
			final_answers.append(str(e))
		return final_answers[0]

	### get link domain functions 
	
	def correct_link_domain(domain):
		return domain.replace('.', '-') + '.emarsys.net.'

	### create object for output and applies linkDomain rules 

	link_answer = check_cname_domain(link_subdomain)
	correct_link_answer = correct_link_domain(link_subdomain)
	stat_and_comm = linkDomain_rules(link_answer, correct_link_answer)
	obj = Domain( record_name = link_subdomain, record_type= 'CNAME', record_result =  link_answer, status = stat_and_comm[0], comment = stat_and_comm[1] )
	obj_list.append(obj)



	###  sender domain functions
		
		### create object for output and applies Bounces rules 

	def bounces_sender_domain(domain):
		bounces_domain  = 'bounces.' + domain
		return check_cname_domain(bounces_domain)
	
	bounces_answer = bounces_sender_domain(sender_domain)
	correct_bounces_answer = 'bounces.emarsys.net.'
	stat_and_comm = bounces_rules(bounces_answer, correct_bounces_answer)
	obj = Domain( record_name = sender_domain, record_type= 'CNAME', record_result =  bounces_answer, status = stat_and_comm[0], comment = stat_and_comm[1] )
	obj_list.append(obj)


		### create object for output and applies  key5.dkim Rules

	def key5_sender_domain(domain):
		key5_domain = 'key5._domainkey.' + domain
		return check_cname_domain(key5_domain)

	key5_answer = key5_sender_domain(sender_domain)
	correct_key5_answer = 'key5.dkim.emarsys.net.'
	stat_and_comm = key5_rules(key5_answer, correct_key5_answer)
	obj = Domain( record_name = sender_domain, record_type= 'CNAME', record_result =  key5_answer, status = stat_and_comm[0], comment = stat_and_comm[1] )
	obj_list.append(obj)

		### create object for output and applies  key6.dkim Rules

	def key6_sender_domain(domain):
		key6_domain = 'key6._domainkey.' + domain
		return check_cname_domain(key6_domain)

	key6_answer = key6_sender_domain(sender_domain)
	correct_key6_answer = 'key6.dkim.emarsys.net.'
	stat_and_comm = key6_rules(key6_answer, correct_key6_answer)
	obj = Domain( record_name = sender_domain, record_type= 'CNAME', record_result =  key6_answer, status = stat_and_comm[0], comment = stat_and_comm[1] )
	obj_list.append(obj)

		### create object for output and applies  mx Rules

	def mx_sender_domain(domain):
		
	
		final_answers=[]

		try:
			answers=dns.resolver.resolve(domain, 'MX')
			for value in answers:
				final_answers.append(value.to_text())			
		except Exception as e:
			final_answers.append(str(e))
		return final_answers

	mx_answer = mx_sender_domain(sender_domain)
	stat_and_comm = mx_sender_rules(mx_answer)
	obj = Domain( record_name = sender_domain, record_type= 'MX', record_result =  mx_answer, status = stat_and_comm[0], comment = stat_and_comm[1] )
	obj_list.append(obj)

		### create object for output and applies  TXT Rules
	
	def txt_sender_domain(domain):
		
	
		final_answers=[]

		try:
			answers=dns.resolver.resolve(domain, 'TXT')
			for value in answers:
				final_answers.append(value.to_text())			
		except Exception as e:
			final_answers.append(str(e))
		return final_answers
		
	txt_answer = txt_sender_domain(sender_domain)
	stat_and_comm = txt_sender_rules(txt_answer)
	obj = Domain( record_name = sender_domain, record_type= 'TXT', record_result =  txt_answer, status = stat_and_comm[0], comment = stat_and_comm[1] )
	obj_list.append(obj)

		### create object for output and applies  DMARC Rules

	def dmarc_sender_domain(domain):
		dmarc_domain = '_dmarc.' + domain
		return txt_sender_domain(dmarc_domain)

	dmarc_answer = dmarc_sender_domain(sender_domain)
	stat_and_comm = dmarc_sender_rules(dmarc_answer)
	obj = Domain( record_name = sender_domain, record_type= 'DMARC', record_result =  dmarc_answer, status = stat_and_comm[0], comment = stat_and_comm[1] )
	obj_list.append(obj)
		









	
	return render(request, 'linkDomain.html', {'obj_list' : obj_list})

