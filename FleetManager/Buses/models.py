from django.db import models

# Create your models here.

class Routes(models.Model):
	stage = models.CharField(max_length = 100)
	route = models.CharField(max_length = 400)

	def __str__(self):
		return "stage"+self.stage+"|"+" route"+self.route
