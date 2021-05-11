from django.shortcuts import render
from .models import Domain

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

	# end_result = zip(domain_list, record_result)

	# def cleaned_record_result(result_list):
	# 	output = ''
	# 	for i in result_list:
	# 		output = output + i + '<br>'
	# 	return output




	# output = dict(zip(domain_list, record_result)) 
	obj_list = []

	for obj in domain_list:
		
		obj = Domain( record_name = obj, record_type= record_val, record_result =  get_records(obj))
		obj_list.append(obj)
		

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
