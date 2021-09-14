
# Importing django modules
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.admin.utils import flatten
from .models import Domain, MXrecord, NSrecord
# Importing python modules 
import dns.resolver
import dns.reversename
# Importing all the functionas that are used in views
from resolver.myfunctions import *
from resolver.linkDomain_rules import *



# create views	

def index(request):
	return render(request, 'index.html')






def compute(request):

	domain_val = request.POST['domains']
	record_val = request.POST['records']
	delimitor = request.POST['delimitor']
	domain_list=domain_val.split(delimitor) # cleaned list of domains 
	obj_list = make_objlist(record_val, domain_list) ### resolve records for given domain and prepare result for output 

	return render(request, 'result.html', {'obj_list' : obj_list})




### process domain or list of domains with single record check 
def compute_csv(request):
	if request.method=='POST':
		csv_file = request.FILES['csv_file']
		record_val = request.POST['records']
	domain_list = process_csv(csv_file)
	obj_list = make_objlist(record_val, domain_lists)### resolve records for given domain and prepare result for output 

	### writes csv files with results and output to frontend 
	response = HttpResponse(content_type = 'text/csv')
	writer  = csv.writer(response, lineterminator='\n')
	writer.writerow(['domain' , 'DNS record', 'status' , 'comment'])
	for obj in obj_list:
		str_record_result = '\n'.join(obj.record_result)
		writer.writerow( [obj.record_name, str_record_result, obj.status, obj.comment] )
	response['Content-Disposition'] = 'attachment; filename="result.csv"'

	return response




### process domain or list of domains with multiple record check 
def compute_multi(request):
	domains = request.POST['domains']
	delimitor = request.POST['delimitor']
	domain_list= domains.split(delimitor)
	if request.method == 'POST':
		records  = request.POST.getlist('records')
	obj_list = []

	
	
	for domain in domain_list:
		result_list = []
		for record in records:
			if record:

				result_list.append(multi_output(domain, record))
		obj_list.append(result_list)

	return render(request, 'multiple.html', { 'obj_list' : obj_list, 'records' : records})




### link subdomain and sender domain view 
def linkDomain(request):
	sender_domain = request.POST['senderDomain']
	link_subdomain = request.POST['linkDomain']
	obj_list = []
	
	### create object for output and applies linkDomain rules 

	link_answer = get_records(link_subdomain,'CNAME')
	correct_link_answer = link_subdomain.replace('.', '-') + '.emarsys.net.'
	stat_and_comm = linkDomain_rules(link_answer, correct_link_answer)
	obj = Domain( record_name = link_subdomain, record_type= 'CNAME', record_result =  link_answer, status = stat_and_comm[0], comment = stat_and_comm[1] )
	obj_list.append(obj)


	###  sender domain functions
		
		### create object for output and applies Bounces rules 

	bounces_domain  = 'bounces.' + sender_domain
	bounces_answer = get_records(bounces_domain,'CNAME')
	correct_bounces_answer = 'bounces.emarsys.net.'
	stat_and_comm = bounces_rules(bounces_answer, correct_bounces_answer)
	obj = Domain( record_name = bounces_domain, record_type= 'CNAME', record_result =  bounces_answer, status = stat_and_comm[0], comment = stat_and_comm[1] )
	obj_list.append(obj)


		### create object for output and applies  key5.dkim Rules

	key5_domain = 'key5._domainkey.' + sender_domain
	key5_answer = get_records(key5_domain,'CNAME')
	correct_key5_answer = 'key5.dkim.emarsys.net.'
	stat_and_comm = key5_rules(key5_answer, correct_key5_answer)
	obj = Domain( record_name = key5_domain, record_type= 'CNAME', record_result =  key5_answer, status = stat_and_comm[0], comment = stat_and_comm[1] )
	obj_list.append(obj)

		### create object for output and applies  key6.dkim Rules

	key6_domain = 'key6._domainkey.' + sender_domain
	key6_answer = get_records(key6_domain,'CNAME')
	correct_key6_answer = 'key6.dkim.emarsys.net.'
	stat_and_comm = key6_rules(key6_answer, correct_key6_answer)
	obj = Domain( record_name = key6_domain, record_type= 'CNAME', record_result =  key6_answer, status = stat_and_comm[0], comment = stat_and_comm[1] )
	obj_list.append(obj)

		### create object for output and applies  mx Rules

	
	mx_answer = get_records(sender_domain,'MX')
	stat_and_comm = mx_sender_rules(mx_answer)
	obj = Domain( record_name = sender_domain, record_type= 'MX', record_result =  mx_answer, status = stat_and_comm[0], comment = stat_and_comm[1] )
	obj_list.append(obj)

		### create object for output and applies  TXT Rules
	
			
	txt_answer = [ i.replace('"','') for i in  get_records(sender_domain,'TXT')]
	stat_and_comm = txt_sender_rules(txt_answer)
	obj = Domain( record_name = sender_domain, record_type= 'TXT', record_result =  txt_answer, status = stat_and_comm[0], comment = stat_and_comm[1] )
	obj_list.append(obj)

		### create object for output and applies  DMARC Rules
	
	dmarc_domain = '_dmarc.' + sender_domain
	dmarc_answer = [ i.replace('"','') for i in  get_records(dmarc_domain,'TXT')]
	stat_and_comm = dmarc_sender_rules(dmarc_answer)
	obj = Domain( record_name = dmarc_domain, record_type= 'DMARC', record_result =  dmarc_answer, status = stat_and_comm[0], comment = stat_and_comm[1] )
	obj_list.append(obj)
		

	return render(request, 'result.html', {'obj_list' : obj_list})

