from django.shortcuts import render
from .models import Domain, MXrecord

def index(request):
	return render(request, 'index.html')

def compute(request):

	domain_val = request.POST['domains']
	record_val = request.POST['records']
	delimitor = request.POST['delimitor']
	domain_list=domain_val.split(delimitor) # cleaned list of domains 

	

	def get_records(domain):
		import dns.resolver
		final_answers=[]

		try:
			answers=dns.resolver.resolve(domain, record_val)
			for value in answers:
				final_answers.append(value.to_text())			
		except Exception as e:
			final_answers.append(e)
		return final_answers

	record_result = [get_records(i) for i in domain_list] # list of records

	obj_list = []
	for obj in domain_list:
		obj = Domain( record_name = obj, record_type= record_val, record_result =  get_records(obj))
		obj_list.append(obj)


		
	def mx_rules(result_list): # creates objects of MX records with prioritie and sender domains 
		mx_split = []
		mx_objects = []
		for result in result_list:
			mx_split.append(result.split(' '))
		for mx in mx_split:
			mx_object = MXrecord(  priority = mx[0], domain = mx[1])
			mx_objects.append(mx_object)
		return mx_objects
	
	













		

	return render(request, 'result.html', { 

	'record_val' : record_val, 
		# 'output' : output, 
	'domain_list' : domain_list, 
	# 'obj_list' : obj_list,
	'record_result' : record_result,
	# 'end_result' : end_result, 
	'obj_list' : obj_list, 
	
	

	 })
# Create your views here.
