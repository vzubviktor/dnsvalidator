from django.shortcuts import render
from .models import Domain, MXrecord
import dns.resolver

def index(request):
	return render(request, 'index.html')

def compute(request):

### Gets Raw data from input and cleans for processsing	

	domain_val = request.POST['domains']
	record_val = request.POST['records']
	delimitor = request.POST['delimitor']
	domain_list=domain_val.split(delimitor) # cleaned list of domains 

	
### gets dns records for domain value

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

		# Table case 1

		if 'emarsys.net.' not  in domain_list or 'mx.eemms.net.' not in domain_list :  ### REWRITE TIS RULE TO LOOK PRETTY + Rewrite the rule
			status = 'Wrong returnpath configuration'
			comment = 'no matching MX records found'
		else:
			pass

		# Table case 2

		if (len(set(domain_list))==2):
			if 'return1.emarsys.net.' in domain_list and 'return0.emarsys.net.' in domain_list:
				if (len(set(priority_list))==1):
					status = 'Correct returnpath configuration'

		else: 
			pass

		# Table case 3 

		if (len(set(domain_list))==1):
			if 'mx.eemms.net.' in domain_list:
				status = 'Wrong returnpath configuration'
				comment = 'MX record found matching suite Reply Management'
		else:
			pass

		# Table case 4

		if 'return1.emarsys.net.' in domain_list and 'return0.emarsys.net.' in domain_list: 
			if (len(set(domain_list)) > 2):
				if (len(set(priority_list))==1):
					status = 'Wrong returnpath configuration'
					comment = 'mx.eemms.net (or the domain there) should be removed'
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
							status = 'Wrong returnpath configuration'
							comment = 'mx.eemms.net (or the domain there) should be removed'
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
							status = 'Correct returnpath configuration *'
							comment = 'required MX records are present but there are additional records with lower priorities'
					else:
						status = ''
						comment = ''
						pass
			else:
				pass
		else:
			pass


		# Table 6 case

		if 'return0.emarsys.net.' in domain_list and 'return1.emarsys.net.' not in domain_list: 
			status = 'Invalid returnpath configuration'
			comment ='return1.emarsys.net record is missing'
		else:
			pass

		# Table 7 case

		if 'return1.emarsys.net.' in domain_list and 'return0.emarsys.net.' not in domain_list: 
			status = 'Invalid returnpath configuration'
			comment ='return0.emarsys.net record is missing'
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
					status = 'Wrong returnpath configuration'
					comment = 'MX record found matching suite Reply Management, but there are also other mx records with lower priorities'
				else:
					pass
		else:
			pass

		# Table 9 case - refered to table case 1

		# Table 10 case 

		if 'return1.emarsys.net.' in domain_list and 'return0.emarsys.net.' in domain_list:
			if (len(set(domain_list)) == 2):
				if (len(set(priority_list))!=1):
					status = 'Invalid returnpath configuration'
					comment = 'require MX records are found but the priority is wrong'
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
					status = 'Wrong returnpath configuration'
					comment = 'MX record found matching suite Reply Management, but there are also other mx records with higher priorities. Reply management will not be managed by Emarsys'
				else:
					pass
		else:
			pass




		output.append(status)
		output.append(comment)
		return output 













	



### finalizes object for output to frontend

	
	obj_list = []

	for obj in domain_list:
		record_result = get_records(obj)
		mx_objects = mx_create(record_result)
		stat_and_comm = mx_rules(mx_objects)
		obj = Domain( record_name = obj, record_type= record_val, record_result =  record_result, status = stat_and_comm[0], comment = stat_and_comm[1] )
		obj_list.append(obj)

	













		

	return render(request, 'result.html', { 

	'record_val' : record_val, 
		# 'output' : output, 
	'domain_list' : domain_list, 
	# 'obj_list' : obj_list,
	# 'record_result' : record_result,
	# 'end_result' : end_result, 
	'obj_list' : obj_list, 
	
	

	 })
# Create your views here.
