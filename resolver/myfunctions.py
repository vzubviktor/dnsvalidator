# ### pulls up dns records
# def get_records(domain):
# # import dns.resolver
# 	final_answers=[]

# 	try:
# 		answers=dns.resolver.resolve(domain, record_val)
# 		for value in answers:
# 			final_answers.append(value.to_text())			
# 	except Exception as e:
# 		final_answers.append(e)
# 	return final_answers

# ### IF PTR record - processe ip to get pter record

# def get_ptr(address):
# 	final_answers=[]
# 	try:
# 		domain_address = dns.reversename.from_address(address)
# 		ptr_record = dns.resolver.resolve(domain_address, 'PTR')[0]
# 		final_answers.append(ptr_record)
# 	except Exception as e:
# 		final_answers.append(e)
# 	return final_answers