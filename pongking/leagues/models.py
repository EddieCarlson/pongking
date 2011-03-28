from django.db import models

class League(models.Model):
	name = models.CharField(max_length=40)
	#TODO add logos, descriptions, stats like founded etc
	
	def __unicode__(self):
		return self.name

