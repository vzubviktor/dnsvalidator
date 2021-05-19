from django.db import models

class Domain(models.Model):
	record_name = models.CharField(max_length=1000)
	record_type = models.CharField(max_length=1000)
	record_result = models.CharField(max_length=10000)
	status = models.CharField(max_length=100000,  null = True)
	comment = models.CharField(max_length=100000, null = True)


	def __str__(self):
	 	return self.record_name

	def get_result(self):
	 	return self.record_result

class MXrecord(models.Model):
	# record_name = models.CharField(max_length=1000, null=True)
	priority = models.CharField(max_length=1000)
	domain   = models.CharField(max_length=1000)

	def __str__(self):
	 	return self.priority

	def __str__(self):
	 	return self.domain

class NSrecord(models.Model):
	domain   = models.CharField(max_length=1000)



