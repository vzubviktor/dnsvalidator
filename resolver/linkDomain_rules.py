def linkDomain_rules(answer, correct_answer):
	
	comment = ''
	status = ''
	output = []

	if answer == correct_answer:
		status = 'Valid'
		comment = 'Link domain'

	
		
	elif answer != correct_answer:
		status = 'Invalid'
		comment = 'Incorrect CNAME record'

	else:
		status = 'Invalid'
		comment = 'CNAME record not found'


	output.append(status)
	output.append(comment)
	return output


