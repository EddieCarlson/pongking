from django.db import models
from django.contrib.auth.models import User

from pongking.leagues.models import League
from pongking.awards.models import Award

class Player(models.Model):
	name = models.CharField(max_length=40, unique=True)
	mean = models.FloatField(default=25)
	stdev = models.FloatField(default=25/3.0)
	awards = models.ManyToManyField(Award, blank=True, null=True)
	level = models.DecimalField(max_digits=4, decimal_places=1, default=0)
	rank = models.IntegerField(default=0)#TODO maybe need to change
	#take out default
	league = models.ForeignKey(League, blank=True, null=True)
	user = models.ForeignKey(User, blank=True, null=True)
		
	def __unicode__(self):
		return self.name
