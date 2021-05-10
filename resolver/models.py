from django.db import models

class Domain(models.Model):
	record_name = models.CharField(max_length=1000)
	record_type = models.CharField(max_length=1000)
	record_result = models.CharField(max_length=10000)

	def __str__(self):
	 	return self.record_name

	def get_result(self):
	 	return self.record_result
