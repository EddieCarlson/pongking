from django.db import models
from django.contrib.auth.models import User
	

class Award(models.Model):
	name = models.CharField(max_length=50)
	#image
	
	def __unicode__(self):
		return self.name


class Game(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	
	winner1 = models.CharField(max_length=40)
	winner2 = models.CharField(max_length=40, blank=True, null=True)
	loser1 = models.CharField(max_length=40)
	loser2 = models.CharField(max_length=40, blank=True, null=True)
	
	win1delta = models.FloatField()
	win2delta = models.FloatField(null=True)
	lose1delta = models.FloatField()	
	lose2delta = models.FloatField(null=True)
	
	win_type = models.IntegerField(null=True)
	recorder = models.ForeignKey(User)
	cup_spread = models.IntegerField(null=True)	
	
	def __unicode__(self):
		if not self.winner2 == "" and not self.loser2 == "":
			return self.winner1 + " " + self.winner2 + " / " + self.loser1 + " " + self.loser2
		else: 
			return self.winner1 + " / " + self.loser1

class League(models.Model):
	name = models.CharField(max_length=40)
	
	def __unicode__(self):
		return self.name


class Player(models.Model):
	name = models.CharField(max_length=40, unique=True)
	mean = models.FloatField(default=25)
	stdev = models.FloatField(default=25/3.0)
	games = models.ManyToManyField(Game, blank=True, null=True)
	awards = models.ManyToManyField(Award, blank=True, null=True)
	level = models.DecimalField(max_digits=4, decimal_places=1, default=0)
	rank = models.IntegerField(default=0)#TODO maybe need to change
	#take out default
	league = models.ForeignKey(League, blank=True, null=True)
	user = models.ForeignKey(User, blank=True, null=True)
		
	def __unicode__(self):
		return self.name

	
