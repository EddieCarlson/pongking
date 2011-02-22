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
	
	win1delta = models.FloatField()
	win2delta = models.FloatField(null=True)
	lose1delta = models.FloatField()	
	lose2delta = models.FloatField(null=True)
	
	wintype = models.IntegerField(null=True)
	recorder = models.ForeignKey(User)
	cupspread = models.IntegerField(null=True)	
	
	def __unicode__(self):
		if not self.winner2 == "":
			return self.winner1 + " " + self.winner2 + " / " + self.loser1 + " " + self.loser2
		else: 
			return self.winner1 + " / " + self.loser1

class League(models.Model):
	name = models.CharField(max_length=40)
	
	def __unicode__(self):
		return self.name


class Player(models.Model):
	name = models.CharField(max_length=40, unique=True)
	u = models.FloatField(default=25)
	s = models.FloatField(default=25/3.)
	games = models.ManyToManyField(Game, null=True)
	awards = models.ManyToManyField(Award, null=True)
	rank = models.IntegerField(null=True, blank=True)
	#take out default
	league = models.ForeignKey(League, default=1)
	user = models.ForeignKey(User, null=True)
		
	def __unicode__(self):
		return self.name

	
