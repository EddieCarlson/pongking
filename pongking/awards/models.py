from django.db import models

class Award(models.Model):
	name = models.CharField(max_length=50)
	#TODO add image, more info
	
	def __unicode__(self):
		return self.name
