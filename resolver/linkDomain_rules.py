import re


### Rules for Link domain 
def linkDomain_rules(answers, correct_answer):
	
	comment = ''
	status = ''
	output = []
	for answer in answers:

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

def bounces_rules(answers, correct_answer):

	comment = ''
	status = ''
	output = []
	for answer in answers:

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
def key5_rules(answers, correct_answer):
	comment = ''
	status = ''
	output = []
	for answer in answers:

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


def key6_rules(answers, correct_answer):
	comment = ''
	status = ''
	output = []
	for answer in answers:


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
		if record.startswith('v=spf1'):
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
		if record.startswith('v=DMARC1'):
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

def key_sender_rules(record_val, key_answer):
	comment = ''
	status = 'Invalid'
	output = []
	for answer in key_answer:
		
		if record_val == 'key2':
			valid_key = 'v=DKIM1;k=rsa;p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCqFwlkVVM4irVCuSD/bs1ewUWLU/0c8qOdhw4/YXXZugQapNKUpcpmaFwZ3Dw380eIm8fFUfv96ObYEPeDBb32KcOjQfHV6cquwMfnIy7iZtC+3lloRJKKc/fHDgaP81l8fOEwpm7F4jXqa3Qh775JlsrptFfBoMAyQ0XDgUQI1QIDAQAB'
			if answer == valid_key:
				status = 'Valid'
				comment = 'DKIM for Emarsys EMEA&APAC'

		elif record_val == 'key4':
			valid_key = 'v=DKIM1;k=rsa;p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC89LipD0a30WgIjdxc8BLDMsSMUf8HoXJttcZQKn3R5kdsxd2L4DXP/UVJ0/0jQJwljc2eTXJRshlTU7s8Wdu50MsMfBAu7Ky8WNjR867hw7ACpRmessTDgyASj9gOEBCXmEw0rtn3havJkzF/1kAVKhx0get3XdGMHnFA9ya0KwIDAQAB'
			if answer == valid_key:
				status = 'Valid'
				comment = 'DKIM for Emarsys AMERICAs'

		elif record_val == 'key5':
			valid_key = 'v=DKIM1;k=rsa;p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCtuwC9wykvNVY0H+4ZBSRtI3ZkNf+BYhxlU066j3FUhOiju0BxS4Px+6T4E2hzIMX9OpTfil8RCYgNSz/XRHGJ/6VYPyiGAGyqvdbiO9wHsbQJ/GREu5rhamsPvoxf0AidaqlpQ8fM6ITe+VbtRMeVGLKlei1St7elNSWt1wijKQIDAQAB'
			if answer == valid_key:
				status = 'Valid'
				comment = 'DKIM for Emarsys SAP'
			

		elif record_val == 'key6':
			valid_key = 'v=DKIM1;k=rsa;p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCpk27eqCMMWoFX72YasAzxzLpld+DECX7ny2bsUknsehh9OkLe2sI0cy38z+CSAQk8X0gGRaiBV6wTZbhpuPgC+DU9oTwyzWY0lKiO3AHctHIDIxVu5iBV0SoNomV42qb5nRzMY+HL/Ri+Ul8RQj3YFsBluRhvuG1AtfL2oXD9YwIDAQAB'
			if answer == valid_key:
				status = 'Valid'
				comment = 'DKIM for Emarsys SAP'

		else:
			status = 'Invalid'
			comment = ''

	output.append(status)
	output.append(comment)
	return output

### Rules for custom selector and key
def custom_sender_rules(value, key_answer, key):
	comment = key_answer
	status = value
	output = []
	for answer in key_answer:
		if value == answer:
			status = 'Valid'
			if key == 'key2':
				comment = 'DKIM for Emarsys EMEA&APAC'
			elif key == 'key4':
				comment = 'DKIM for Emarsys AMERICAs'
			elif key == 'key5':
				comment = 'DKIM for Emarsys SAP'
			elif key == 'key6':
				comment = 'DKIM for Emarsys SAP'
			else:
				comment = ''
		else:
			status = 'Invalid'
			comment = 'The values are not matching'
	output.append(status)
	output.append(comment)
	return output


def spf_rules(records):
	comment = ''
	status = ''
	spf_records= []
	for i in records:
		if i.startswith('v=spf1'):
			spf_records.append(i)
		
	output = []
	for record in spf_records:
	
		if 'include:emarsys.net' in record and 'include:emarsys.us' in record :
			if 'include:emsmtp.com' in record or 'include:emsmtp.us' in record:
				status = 'Valid'
				comment = 'Legacy sender Domain SPF for both CSA and non-CSA'
			else:
				status = 'Valid'
				comment = 'Sender Domain SPF for both CSA and non-CSA'
		elif  'include:emarsys.net' in record :
			if 'include:emsmtp.com' in record:
				status = 'Valid'
				comment = 'Legacy sender Domain SPF for CSA'
			else:
				status = 'Valid'
				comment = 'Sender Domain SPF for CSA'
		elif 'include:emarsys.us' in record :
			if 'include:emsmtp.us' in record:
				status = 'Valid'
				comment = 'Legacy sender Domain SPF for non-CSA'
			else:
				status = 'Valid'
				comment = 'Sender Domain SPF for non-CSA'
		
		elif 'include:spf.emarsys.net' in record :
			status = 'Valid'
			comment = 'Sender Domain SPF for SAP Emarsys'
		
		
		else: 
			status = 'Invalid'
			comment =  'SPF does not contain required values'

		

	if not spf_records:
		 
		status = 'Invalid'
		comment =  'No SPF record found'
		output.append(status)
		output.append(comment)
		return output
	else:
		output.append(status)
		output.append(comment)
		return output














