import dns.resolver
import dns.reversename
import csv
import io
from django.contrib.admin.utils import flatten

from resolver.mxrules import *
from resolver.nsrules import *
from resolver.linkDomain_rules import *


### Function to process csv
def process_csv(csv_file):
		domain_list = []
		csvf = io.TextIOWrapper(csv_file, encoding="utf-8", )
		reader = csv.reader(csvf, )
		for value in reader:
			domain_list.append(value)
		return flatten(domain_list)


## Function to get main records

def spf_records(records):
	result = []
	for record in records:
		if record.startswith('v=spf1'):
			result.append(record)
	return result

def spf_recordsCsv(records):
	result = []
	for record in records:
		if record.startswith('"v=spf1'):
			result.append(record)
	return result


def get_records(domain,record_val):
# import dns.resolver
	final_answers=[]

	try:
		answers=dns.resolver.resolve(domain, record_val)
		for value in answers:
			final_answers.append(value.to_text())			
	except Exception as e:
		final_answers.append(str(e))
	return final_answers


### Function to get PTR record 

def get_ptr(address):
		final_answers=[]
		try:
			domain_address = dns.reversename.from_address(address)
			ptr_record = dns.resolver.resolve(domain_address, 'PTR')[0]
			final_answers.append(ptr_record)
		except Exception as e:
			final_answers.append(e)
		return final_answers


### Get chosen  records for domain, applies rules, creates status and comment 
	### and create objects to be displayed at front end, 

def make_objlist(record_val, domain_list):
	obj_list = []

	if record_val == 'PTR':
		for obj in domain_list:
			record_result = get_ptr(obj)
			obj_list.append(obj)
	
	elif record_val == 'MX':
		for obj in domain_list:
			record_result = get_records(obj, record_val)
			mx_objects = mx_create(record_result)
			stat_and_comm = mx_rules(mx_objects)
			obj = Domain( record_name = obj,
						  record_type= record_val,
						  record_result =  record_result,
						  status = stat_and_comm[0],
						  comment = stat_and_comm[1] )
			obj_list.append(obj)

	elif record_val == 'TXT':
		for obj in domain_list:
			record_result = [ i.replace('"','') for i in  get_records(obj, record_val)]
			obj = Domain( record_name = obj,
			              record_type= record_val, 
			              record_result =  record_result, 
			              status = '', 
			              comment = '' )
			obj_list.append(obj)
			
	
	

	elif record_val == 'NS':
		for obj in domain_list:
			record_result = get_records(obj,record_val)
			ns_objects = ns_create(record_result)
			stat_and_comm = ns_rules(ns_objects)
			obj = Domain( record_name = obj,
			              record_type= record_val, 
			              record_result =  record_result, 
			              status = stat_and_comm[0], 
			              comment = stat_and_comm[1] )
			obj_list.append(obj)
	
	else:
		for obj in domain_list:
			record_result = get_records(obj,record_val)
			# mx_objects = mx_create(record_result)
			# stat_and_comm = mx_rules(mx_objects)
			obj = Domain( record_name = obj,
			              record_type= record_val,
			              record_result =  record_result,
			              status = '',
			              comment = '' )
			obj_list.append(obj)

	return obj_list


### creates output for multiple domains and multiple records
def multi_output(domain, record_val):
		

		if record_val == 'PTR':
			
			record_result = get_ptr(domain, record_val)
			obj = Domain( record_name = domain, record_type= record_val, record_result =  record_result, status = '' , comment = '' )
			return obj

		elif record_val == '':
			pass

		elif record_val == 'MX':
			record_result = get_records(domain, 'MX')
			stat_and_comm = new_mx_rules(record_result)
			obj = Domain( record_name = domain, record_type= 'MX', record_result =  record_result, status = stat_and_comm[0], comment = stat_and_comm[1] )
			return obj


		### create objects for MX records and applies rules
		elif record_val == 'mxForCRP':


			record_result = get_records(domain, 'MX')
			mx_objects = mx_create(record_result)
			stat_and_comm = mx_rules(mx_objects)
			obj = Domain( record_name = domain, record_type= 'MX for CRP', record_result =  record_result, status = stat_and_comm[0], comment = stat_and_comm[1] )
			return obj

		### create objects for NS records and applies rules

		elif record_val == 'NS':
			
			record_result = get_records(domain, record_val)
			ns_objects = ns_create(record_result)
			stat_and_comm = ns_rules(ns_objects)
			obj = Domain( record_name = domain, record_type= record_val, record_result =  record_result, status = stat_and_comm[0], comment = stat_and_comm[1] )
			return obj
		
		### create objects for SPF records and applies rules

		elif record_val == 'SPF':
			
			record_result = [ i.replace('"','') for i in  get_records(domain, 'TXT')]
			stat_and_comm = spf_rules(record_result)
			obj = Domain( record_name = domain, record_type= record_val, record_result =  spf_records(record_result), status = stat_and_comm[0], comment = stat_and_comm[1] )
			return obj

		### create objects for DMARC records and applies rules

		elif record_val == 'DMARC':
			dmarc_domain = '_dmarc.' + domain
			dmarc_answer = [ i.replace('"','') for i in  get_records(dmarc_domain, 'TXT')]
			stat_and_comm = dmarc_sender_rules(dmarc_answer)
			obj = Domain( record_name = dmarc_domain, record_type= 'DMARC', record_result =  dmarc_answer, status = stat_and_comm[0], comment = stat_and_comm[1] )
			return obj

		

		### create objects for Custom dkim key and selector records and applies rules

		elif ':' in record_val:
			custom = record_val.split(':')
			key = custom[0]
			value = custom[1]
			key_domain  = key + '._domainkey.' + domain
			key_answer = [ i.replace('"','') for i in  get_records(key_domain, 'TXT')]
			stat_and_comm = custom_sender_rules(value, key_answer, key)
			obj = Domain( record_name = key_domain, record_type= 'DKIM', record_result =  key_answer, status = stat_and_comm[0], comment = stat_and_comm[1] )
			return obj

		elif 'key' in record_val and not ':'  in record_val:
			key_domain  = record_val + '._domainkey.' + domain
			key_answer = [ i.replace('"','') for i in  get_records(key_domain, 'TXT')]
			stat_and_comm = key_sender_rules(record_val, key_answer)
			obj = Domain( record_name = key_domain, record_type= 'DKIM', record_result =  key_answer, status = stat_and_comm[0], comment = stat_and_comm[1] )
			return obj


		### create objects for domains and records with no rules
		else:
			
			record_result = get_records(domain, record_val)
			# mx_objects = mx_create(record_result)
			# stat_and_comm = mx_rules(mx_objects)
			obj = Domain( record_name = domain, record_type= record_val, record_result =  record_result, status = '' , comment = '' )
			return obj





def multi_output_csv(domain, record_val):
		

		if record_val == 'PTR':
			
			record_result = get_ptr(domain, record_val)
			obj = Domain( record_name = domain, record_type= record_val, record_result =  record_result, status = '' , comment = '' )
			return obj

		elif record_val == '':
			pass


		elif record_val == 'MX':
			record_result = get_records(domain, 'MX')
			stat_and_comm = new_mx_rules(record_result)
			obj = Domain( record_name = domain, record_type= 'MX', record_result =  record_result, status = stat_and_comm[0], comment = stat_and_comm[1] )
			return obj


		### create objects for MX records and applies rules
		elif record_val == 'mxForCRP':

			record_result = get_records(domain, 'MX')
			mx_objects = mx_create(record_result)
			stat_and_comm = mx_rules(mx_objects)
			obj = Domain( record_name = domain, record_type= 'MX for CRP', record_result =  record_result, status = stat_and_comm[0], comment = stat_and_comm[1] )
			return obj

		### create objects for NS records and applies rules

		elif record_val == 'NS':
			
			record_result = get_records(domain, record_val)
			ns_objects = ns_create(record_result)
			stat_and_comm = ns_rules(ns_objects)
			obj = Domain( record_name = domain, record_type= record_val, record_result =  record_result, status = stat_and_comm[0], comment = stat_and_comm[1] )
			return obj
		
		### create objects for SPF records and applies rules

		elif record_val == 'SPF':
			
			record_result = [ i.replace('"','') for i in  get_records(domain, 'TXT')]
			stat_and_comm = spf_rules(record_result)
			obj = Domain( record_name = domain, record_type= record_val, record_result =  spf_recordsCsv(get_records(domain, 'TXT')), status = stat_and_comm[0], comment = stat_and_comm[1] )
			return obj

		### create objects for DMARC records and applies rules

		elif record_val == 'DMARC':
			dmarc_domain = '_dmarc.' + domain
			dmarc_answer = [ i.replace('"','') for i in  get_records(dmarc_domain, 'TXT')]
			stat_and_comm = dmarc_sender_rules(dmarc_answer)
			obj = Domain( record_name = dmarc_domain, record_type= 'DMARC', record_result =  get_records(dmarc_domain, 'TXT'), status = stat_and_comm[0], comment = stat_and_comm[1] )
			return obj

		

		### create objects for Custom key and selector records and applies rules

		elif ':' in record_val:
			custom = record_val.split(':')
			key = custom[0]
			value = custom[1]
			key_domain  = key + '._domainkey.' + domain
			key_answer = [ i.replace('"','') for i in  get_records(key_domain, 'TXT')]
			stat_and_comm = custom_sender_rules(value, key_answer, key)
			obj = Domain( record_name = key_domain, record_type= 'DKIM', record_result =  get_records(key_domain, 'TXT'), status = stat_and_comm[0], comment = stat_and_comm[1] )
			return obj

		elif 'key' in record_val and not ':'  in record_val:
			key_domain  = record_val + '._domainkey.' + domain
			key_answer = [ i.replace('"','') for i in  get_records(key_domain, 'TXT')]
			stat_and_comm = key_sender_rules(record_val, key_answer)
			obj = Domain( record_name = key_domain, record_type= 'DKIM', record_result =  get_records(key_domain, 'TXT'), status = stat_and_comm[0], comment = stat_and_comm[1] )
			return obj


		### create objects for domains and records with no rules
		else:
			
			record_result = get_records(domain, record_val)
			# mx_objects = mx_create(record_result)
			# stat_and_comm = mx_rules(mx_objects)
			obj = Domain( record_name = domain, record_type= record_val, record_result =  record_result, status = '' , comment = '' )
			return obj

