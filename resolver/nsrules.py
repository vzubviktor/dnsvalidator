from .models import Domain, NSrecord


### Creates objects associated with ns records
def ns_create(result_list):
	ns_objects = []
	for result in result_list:
		 ns_object = NSrecord(domain = result)
		 ns_objects.append(ns_object)
	return ns_objects


### defines rules for ns records
def ns_rules(objects):
	output = []
	status = 'Not delegated to Emarsys'
	comment = ''
	domain_list = [ i.domain for i in objects]

	test_list = []
	

    	




	### Rule 1
	if len(domain_list) == 5:
		check_list = [
		'ns4.dnsmadeeasy.com.',
		'ns3.dnsmadeeasy.com.',
		'ns0.dnsmadeeasy.com.',
		'ns2.dnsmadeeasy.com.',
		'ns1.dnsmadeeasy.com.',
		]
		compare_list = []
		for i in check_list:
			if i in domain_list:
				compare_list.append(i)
			else:
				pass
		if len(compare_list) == len(check_list):

			status = 'Probably delegated to Emarsys'
			comment = 'It could be delegated to Emarsys, but vanity setup is not configured in DNSMadeEasy'
		else:
			pass
	# else:
	# 	pass
	


	### Rule 2

	elif len(domain_list) == 4:
		check_list = [
		'ns1.emarsys.net.',
		'ns2.emarsys.net.',
		'ns3.emarsys.net.',
		'ns4.emarsys.net.',
		]
		domain_list.sort()
		check_list.sort()
		if domain_list == check_list:
			status = 'Delegated to Emarsys'
			comment = ''
		else:
			pass
	

	### Rule 3

	elif 'The DNS query name does not exist' in str(domain_list[0]):
		status ='No NS records'
		comment = 'Sometimes the NS records will NOT SHOW until the setup in DNS Made Easy is completed.'

	### if no rules apply	

	else:
		pass





	output.append(status)
	output.append(comment)
	return output 









