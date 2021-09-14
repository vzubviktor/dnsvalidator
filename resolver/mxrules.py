### gets dns records for domain value
from django.shortcuts import render
from .models import Domain, MXrecord
import dns.resolver


# record_result = [get_records(i) for i in domain_list] # list of records



###  creates objects of MX records with priorities and sender domains

def mx_create(result_list): 
	mx_split = []
	mx_objects = []

	for result in result_list:
		try: 
			mx_split.append(result.split(' '))
			
		except:
			mx_object = MXrecord( priority = 'error', domain = result)
			mx_objects.append(mx_object)


	if mx_split:
		for mx in mx_split:
			mx_object = MXrecord(  priority = mx[0], domain = mx[1])
			mx_objects.append(mx_object)
	


	return mx_objects

### define rules and  process mx record objects through rules

def mx_rules(objects):
	comment = ''
	status = ''
	output = []
	priority_list = [ i.priority for i  in objects]
	domain_list = [ i.domain for i in objects]
	old_record_list = [ 
				'e3uspmta1.emarsys.net.',
				'e3uspmta2.emarsys.net.',
				'e3uspmta3.emarsys.net.',
				'e3uspmta4.emarsys.net.',
				'e3uspmta5.emarsys.net.',
				'e3uspmta6.emarsys.net.',
				'e3uspmta7.emarsys.net.',
				'e3uspmta8.emarsys.net.',
				'e3uspmta9.emarsys.net.',
				'e3uspmta10.emarsys.net.',
				'suitepmta02.emarsys.net.',
				'suitepmta01.emarsys.net.',
				'return1.emarsys.net.',
				'return0.emarsys.net.',
				]

	 

	# Extra case to handle errors

	# if 'error' in priority_list:
	# 	status = domain_list[0]
	# 	comment = ' An error occured. Please read status '
	# else:
	# 	pass



	# Table case 1

	if 'emarsys.net.' not  in domain_list or 'mx.eemms.net.' not in domain_list : 
		try:
			for i in objects:
				if 'emarsys.net' in i.domain or 'mx.eemms.net.' in i.domain:
					pass
			else:
				status = 'Invalid'
				comment = 'Wrong returnpath configuration. No matching MX records found'
		except:
			status = 'Invalid'
			comment = 'Wrong returnpath configuration. No matching MX records found'

	else:
		pass

	# Table case 2

	if (len(set(domain_list))==2):
		if 'return1.emarsys.net.' in domain_list and 'return0.emarsys.net.' in domain_list:
			if (len(set(priority_list))==1):
				status = 'Valid'
				comment = 'Correct returnpath configuration'

	else: 
		pass

	# Table case 3 

	if (len(set(domain_list))==1):
		if 'mx.eemms.net.' in domain_list:
			status = 'Invalid'
			comment = 'Wrong returnpath configuration. MX record  matching the Suite Reply Management'
	else:
		pass

	# Table case 4

	if 'return1.emarsys.net.' in domain_list and 'return0.emarsys.net.' in domain_list: 
		if (len(set(domain_list)) > 2):
			if (len(set(priority_list))==1):
				status = 'Invalid'
				comment = 'Wrong returnpath configuration. The extra mail servers should be removed'
			else:
				emarsys_list = []
				other_list = []
				for i in objects:
					if i.domain == 'return0.emarsys.net.' or i.domain == 'return1.emarsys.net.':
						emarsys_list.append(i.priority)
					else:
						other_list.append(i.priority)
				if emarsys_list[0] == emarsys_list[1]:
					if emarsys_list[0] in other_list:
						status = 'Invalid'
						comment = 'Wrong returnpath configuration. The extra mail servers should be removed'
					else:
						pass
				else:
					pass
		else:
			pass
	else:
		pass

	# Table case 5

	if 'return1.emarsys.net.' in domain_list and 'return0.emarsys.net.' in domain_list: 
		if (len(set(domain_list)) > 2):
			emarsys_list = []
			other_list = []
			for i in objects:
				if i.domain == 'return0.emarsys.net.' or i.domain == 'return1.emarsys.net.':
					emarsys_list.append(int(i.priority))
				else:
					other_list.append(int(i.priority))
			for li in other_list:
				if li > emarsys_list[0] and li > emarsys_list[1]:
						status = 'Valid'
						comment = 'Partially correct returnpath configuration. Required MX records are present but there are additional records with lower priorities'
				else:
					status = ''
					comment = ''
					pass
		else:
			pass
	else:
		pass

	# Table case 5a

	if 'return1.emarsys.net.' in domain_list and 'return0.emarsys.net.' in domain_list: 
		if (len(set(domain_list)) > 2):
			emarsys_list = []
			other_list = []
			for i in objects:
				if i.domain == 'return0.emarsys.net.' or i.domain == 'return1.emarsys.net.':
					emarsys_list.append(int(i.priority))
				else:
					other_list.append(int(i.priority))
			if (len(set(emarsys_list)) > 1):

				for li in other_list:
					if li > emarsys_list[0] and li > emarsys_list[1]:
						status = 'Invalid'
						comment = 'Incomplete returnpath configuration. Required MX records are found but the priority is wrong and there are also other records with lower priority'
					else:
						pass
			else: 
				pass			
		else:
			pass
	else:
		pass


	# Table case 5b

	if 'return1.emarsys.net.' in domain_list and 'return0.emarsys.net.' in domain_list: 
		if (len(set(domain_list)) > 2):
			emarsys_list = []
			other_list = []
			for i in objects:
				if i.domain == 'return0.emarsys.net.' or i.domain == 'return1.emarsys.net.':
					emarsys_list.append(int(i.priority))
				else:
					other_list.append(int(i.priority))
			if (len(set(emarsys_list)) == 1):

				for li in other_list:
					if li < emarsys_list[0] and li < emarsys_list[1]:
						status = 'Invalid'
						comment = 'Wrong returnpath configuration. Emarsys records should have have the highest priority (the lower number the higher the priority)'
					else:
						pass
			else: 
				pass			
		else:
			pass
	else:
		pass




	# Table 6 case

	if 'return0.emarsys.net.' in domain_list and 'return1.emarsys.net.' not in domain_list: 
		status = 'Invalid'
		comment ='Incomplete returnpath configuration. return1.emarsys.net record is missing'
	else:
		pass

	# Table 7 case

	if 'return1.emarsys.net.' in domain_list and 'return0.emarsys.net.' not in domain_list: 
		status = 'Invalid'
		comment ='Incomplete returnpath configuration. return0.emarsys.net record is missing'
	else:
		pass

	# Table 8 case

	if 'mx.eemms.net.' in domain_list and (len(set(domain_list)) > 1):
		emarsys_list = []
		other_list = []
		for i in objects:
			if i.domain == 'mx.eemms.net.':
				emarsys_list.append(int(i.priority))
			else:
				other_list.append(int(i.priority))
		for li in other_list:
			if li > emarsys_list[0]:
				status = 'Invalid'
				comment = 'Wrong returnpath configuration. MX record matching the Suite Reply Management, but there are also other records with a lower priority. Replies will be managed by Emarsys'
			else:
				pass
	else:
		pass

	# Table 9 case - refered to table case 1

	# Table 10 case 

	if 'return1.emarsys.net.' in domain_list and 'return0.emarsys.net.' in domain_list:
		if (len(set(domain_list)) == 2):
			if (len(set(priority_list))!=1):
				status = 'Invalid'
				comment = 'Incomplete returnpath configuration. Required MX records are found but the priority is invalid. Emarsys records should have the highest priority'
			else:
				pass
		else:
			pass
	else:
		pass

	# Table 11 case 
	if 'mx.eemms.net.' in domain_list and (len(set(domain_list)) > 1):
		emarsys_list = []
		other_list = []
		for i in objects:
			if i.domain == 'mx.eemms.net.':
				emarsys_list.append(int(i.priority))
			else:
				other_list.append(int(i.priority))
		for li in other_list:
			if li < emarsys_list[0]:
				status = 'Invalid'
				comment = 'Wrong returnpath configuration. MX record matching the Suite Reply Management, but it has a lower priority. Replies will not be managed by Emarsys'
			else:
				pass
	else:
		pass


	# table 13 case:

	

	if (len(set(priority_list))==1):
		if 'return1.emarsys.net.' in domain_list and 'return0.emarsys.net.' in domain_list:
			if (len(set(domain_list)) == 2):
				pass
				

		else:
			emarsys_list = []
			other_list = []
			
			for i in objects:
				if i.domain in  old_record_list:
					emarsys_list.append(i.priority)
				else:
					other_list.append(i.priority)
			if len(emarsys_list) == len(domain_list):
				status = 'Valid'
				comment = 'Legacy returnpath configuration. New MX setup should be advised'
			else:
				pass

		
	else:
		pass

	# table 14 case:

	if (len(set(priority_list))!=1):
		if 'return1.emarsys.net.' in domain_list and 'return0.emarsys.net.' in domain_list:
			if (len(set(domain_list)) == 2):
				pass
				

		else:
			emarsys_list = []
			other_list = []
			
			for i in objects:
				if i.domain in  old_record_list:
					emarsys_list.append(i.priority)
				else:
					other_list.append(i.priority)
			if len(emarsys_list) == len(domain_list):
				status = 'Invalid'
				comment = 'Incomplete legacy returnpath configuration. Priorities are invalid. New MX setup should be advised'
			else:
				pass

		
	else:
		pass



	# table 15 case:
	if (len(set(priority_list))!=1):
		if 'return1.emarsys.net.' in domain_list and 'return0.emarsys.net.' in domain_list:
			if (len(set(domain_list)) == 2):
				pass
				
		else:
			emarsys_list = []
			other_list = []
			
			for i in objects:
				if i.domain in  old_record_list:
					emarsys_list.append(int(i.priority))
				else:
					other_list.append(int(i.priority))
			if len(emarsys_list) != len(domain_list):
				for i in other_list:
					for j in emarsys_list:
						if j > i:
							status = 'Invalid'
							comment = 'Wrong returnpath configuration. Emarsys records should have have the highest priority (the lower number the higher priority) '
						else:
							pass

			else:
				pass

		
	else:
		pass

	# table 15a case: 

	if (len(set(priority_list))!=1):
		if 'return1.emarsys.net.' in domain_list and 'return0.emarsys.net.' in domain_list:
			if (len(set(domain_list)) == 2):
				pass
				
		else:
			emarsys_list = []
			other_list = []
			check_list = []
			
			for i in objects:
				if i.domain in  old_record_list:
					emarsys_list.append(i)
				elif i.domain == 'mx.eemms.net':
					emarsys_list.append(i)
					check_list.append(i)
				else:
					pass
			if len(emarsys_list) == len(domain_list):
				for i in check_list:
					for j in emarsys_list:
						if j.priority > i.priority and j.domain != i.domain:
							status = 'Invalid'
							comment = 'Wrong returnpath configuration. MX record matching the Suite Reply Management. Replies will be managed by Emarsys'
						else:
							pass
			else:
				pass
		
	else:
		pass


	# table 16 case: 
	if (len(set(priority_list))!=1):
		if 'return1.emarsys.net.' in domain_list and 'return0.emarsys.net.' in domain_list:
			if (len(set(domain_list)) == 2):
				pass
				

		else:
			emarsys_list = []
			other_list = []
			
			for i in objects:
				if i.domain in  old_record_list:
					emarsys_list.append(int(i.priority))
				else:
					other_list.append(int(i.priority))
			if len(emarsys_list) != len(domain_list):
				for i in other_list:
					for j in emarsys_list:
						if j < i:
							status = 'Valid'
							comment = 'Legacy returnpath configuration. New MX setup should be advised. There are other records with a lower priority '
						else:
							pass

			else:
				pass

		
	else:
		pass

	# table 16 a case
	if (len(set(priority_list))!=1):
		if 'return1.emarsys.net.' in domain_list and 'return0.emarsys.net.' in domain_list:
			if (len(set(domain_list)) == 2):
				pass
				

		else:
			emarsys_list = []
			other_list = []
			
			for i in objects:
				if i.domain in  old_record_list:
					emarsys_list.append(int(i.priority))
				else:
					other_list.append(int(i.priority))
			if len(emarsys_list) != len(domain_list):
				if len(set(emarsys_list)) != 1:

					for i in other_list:
						for j in emarsys_list:
							if j > i:
								status = 'Invalid'
								comment = 'Incomplete legacy returnpath configuration. The legacy returnpath MX records are found but the priority is invalid. Emarsys records should have the highest priority'
							else:
								pass
				else:
					pass

			else:
				pass

		
	

	elif 'error' in priority_list:
		if 'The DNS query name does not exist' in str(domain_list[0]) or 'The DNS response does not contain' in str(domain_list[0]) :
			status = 'Invalid'
			comment = 'Wrong returnpath configuration. MX not found'

		elif 'All nameservers failed to answer' in str(domain_list[0]):
			status = 'Invalid'
			comment = 'Wrong returnpath configuration. DNS query failed'
		else:
			pass
	else:
		pass




	output.append(status)
	output.append(comment)
	return output 


def new_mx_rules(records):
	comment = ''
	status = ''
	output = []
	for record in records: #тут надо изменить, что она будет единственной в рекорде (там еще приоритет выдается, но он всегда число)
		if 'mx.eemms.net.' in record :
			status = 'Valid'
			comment = 'Emarsys Reply Management configuration'
		elif 'e3uspmta1.emarsys.net.' in record or 'e3uspmta2.emarsys.net.' in record or 'e3uspmta3.emarsys.net.' in record or 'e3uspmta4.emarsys.net.' in record or 'e3uspmta5.emarsys.net.' in record or 'e3uspmta6.emarsys.net.' in record or 'e3uspmta7.emarsys.net.' in record or 'e3uspmta8.emarsys.net.' in record or 'e3uspmta9.emarsys.net.' in record or 'e3uspmta10.emarsys.net.' in record or 'suitepmta02.emarsys.net.' in record or 'suitepmta01.emarsys.net.' in record or 'return1.emarsys.net.' in record or 'return0.emarsys.net.' in record:
			status = 'Unknown'
			comment = 'Custom Returnpath MX records should be checked with "MX CRP" checkbox'
		
		elif 'The DNS' in record:
			status = 'Invalid'
			comment = 'MX record(s) not found'
		else:
			status = 'Valid'
			comment = 'Customer domain incoming mail server'
	output.append(status)
	output.append(comment)
	return output