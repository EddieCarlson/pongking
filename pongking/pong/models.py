from django.db import models
from django.contrib.auth.models import User
	

class Award(models.Model):
	name = models.CharField(max_length=50)
	#image
	
	def __unicode__(self):
		return self.name


class Game(models.Model):
	date=models.DateTimeField(auto_now_add=True)
	winner1 = models.CharField(max_length = 40)
	winner2 = models.CharField(max_length = 40, blank=True, null=True)
	loser1 = models.CharField(max_length = 40)
	loser2 = models.CharField(max_length = 40, blank=True, null=True)
	wintype = models.IntegerField(null=True)
	
	def __unicode__(self):
		return self.name


class League(models.Model):
	name = models.CharField(max_length=40)
	
	def __unicode__(self):
		return self.name


class Player(models.Model):
	name = models.CharField(max_length=40)
	psr = models.IntegerField(default=1500)
	games = models.ManyToManyField(Game, null=True)
	awards = models.ManyToManyField(Award, null=True)
	adminstatus = models.BooleanField()
	rank = models.IntegerField(null=True, blank=True)
	#take out default
	league = models.ForeignKey(League, default=1)
	user = models.ForeignKey(User, null=True)
		
	def __unicode__(self):
		return self.name

	
