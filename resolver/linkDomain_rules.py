import re


### Rules for Link domain 
def linkDomain_rules(answer, correct_answer):
	
	comment = ''
	status = ''
	output = []

	if answer == correct_answer:
		status = 'Valid'
		comment = 'Link domain'

	elif 'The DNS' in answer:
		status = 'Invalid'
		comment = 'CNAME record not found'

	elif answer != correct_answer:
		status = 'Invalid'
		comment = 'Incorrect CNAME record'

	else:
		pass

	output.append(status)
	output.append(comment)
	return output



### Rules for sender domain 
	### Rules for bounces

def bounces_rules(answer, correct_answer):

	comment = ''
	status = ''
	output = []

	if answer == correct_answer:
		status = 'Valid'
		comment = 'Return-path domain (rp only)'

	elif 'The DNS' in answer:
		status = 'Invalid'
		comment = 'CNAME record not found'

	elif answer != correct_answer:
		status = 'Invalid'
		comment = 'Incorrect value'

	else:
		pass

	output.append(status)
	output.append(comment)
	return output


	### Rules for bounces
def key5_rules(answer, correct_answer):
	comment = ''
	status = ''
	output = []

	if answer == correct_answer:
		status = 'Valid'
		comment = 'DKIM signature (sign with key5 only)'

	elif 'The DNS' in answer:
		status = 'Invalid'
		comment = 'CNAME record not found'

	elif answer != correct_answer:
		status = 'Invalid'
		comment = 'Incorrect value'

	else:
		pass

	output.append(status)
	output.append(comment)
	return output


def key6_rules(answer, correct_answer):
	comment = ''
	status = ''
	output = []

	if answer == correct_answer:
		status = 'Valid'
		comment = 'DKIM signature (sign with key5 only)'

	elif 'The DNS' in answer:
		status = 'Invalid'
		comment = 'CNAME record not found'

	elif answer != correct_answer:
		status = 'Invalid'
		comment = 'Incorrect value'

	else:
		pass

	output.append(status)
	output.append(comment)
	return output


def mx_sender_rules(records):
	comment = ''
	status = ''
	output = []
	for record in records:
		if 'mx.eemms.net.' in record :
			status = 'Valid'
			comment = 'Emarsys incoming mail server'
		elif 'return0.emarsys.net.' in record or  'return1.emarsys.net.' in record:
			status = 'Invalid'
			comment = 'Mxs return0/1.emarsys.net should not be used'
		elif 'The DNS' in record:
			status = 'Invalid'
			comment = 'MX record(s) not found'
		else:
			status = 'Valid'
			comment = 'Sender domain incoming mail server'
	output.append(status)
	output.append(comment)
	return output

def txt_sender_rules(records):
	comment = ''
	status = ''
	output = []
	for record in records:
		if record.startswith('"v=spf1'):
			if  'include:spf.emarsys.net' in record :
				status = 'Valid'
				comment = 'Sender Domain SPF'
			else: 
				status = 'Invalid'
				comment =  'SPF does not contain include:spf.emarsys.net'

			output.append(status)
			output.append(comment)
			return output

		
		elif 'The DNS' in record:
			status = 'Invalid'
			comment = 'TXT record(s) not found'
		else:
			status = 'Invalid'
			comment = 'SPF record not found'
	output.append(status)
	output.append(comment)
	return output

def dmarc_sender_rules(records):
	comment = ''
	status = ''
	output = []
	for record in records:
		sep = '.*\x3B\s*' + 'p='
		check = re.match(sep, record)
		if record.startswith('"v=DMARC1'):
			if  'p=reject' in record  and check:
				status = 'Valid'
				comment = 'Sender Domain DMARC'
			elif 'p=quarantine' in record and check:
				status = 'Valid'
				comment =  'Sender Domain DMARC. Strengthening to "p=reject" is recommended'
			elif 'p=none' in record and check:
				status = 'Invalid'
				comment =  'Strengthen DMARC to a reject or a quarantine policy ("p=reject" or "p=quarantine")'
			else: 
				status = 'Invalid'
				comment =  'Incorrect DMARC record'

			output.append(status)
			output.append(comment)
			return output

		else:
			status = 'Invalid'
			comment = 'DMARC record not found'

	output.append(status)
	output.append(comment)
	return output







