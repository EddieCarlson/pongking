from django.db import models
from django.contrib.auth.models import User

from pongking.players.models import Player

class Game(models.Model):
	date = models.DateTimeField(auto_now_add=True)

	#TODO replace with manytomany fields! limiting to 2 players per side, plus breaking reverse lookup ability
	winner1 = models.ForeignKey(Player, related_name="win_set1")
	winner2 = models.ForeignKey(Player, blank=True, null=True, related_name="win_set2")
	loser1 = models.ForeignKey(Player, related_name="lose_set1")
	loser2 = models.ForeignKey(Player, blank=True, null=True, related_name="lose_set2")
	
	win1delta = models.FloatField()
	win2delta = models.FloatField(null=True)
	lose1delta = models.FloatField()	
	lose2delta = models.FloatField(null=True)
	
	win_type = models.IntegerField(null=True)
	recorder = models.ForeignKey(User)#TODO should be player for consistency
	cup_spread = models.IntegerField(null=True)	
	
	def __unicode__(self):
		if self.winner2 and self.loser2:
			return self.winner1 + " " + self.winner2 + " / " + self.loser1 + " " + self.loser2
		else: 
			return self.winner1 + " / " + self.loser1
