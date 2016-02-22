from django.db import models

class Achiever(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.CharField(max_length=50)

	def full_name(self):
		return self.first_name + ' ' + self.last_name