from django.db import models
from django.contrib.auth.models import User

from pongking.players.models import Player

class Game(models.Model):
	date = models.DateTimeField(auto_now_add=True)

	winners = models.ManyToManyField(Player, related_name="wins")
	losers = models.ManyToManyField(Player, related_name="losses")
	
	win1delta = models.FloatField()
	win2delta = models.FloatField(null=True)
	lose1delta = models.FloatField()	
	lose2delta = models.FloatField(null=True)
	
	win_type = models.IntegerField(null=True)
	recorder = models.ForeignKey(User)#TODO should be player for consistency
	cup_spread = models.IntegerField(null=True)	
	
	def __unicode__(self):
		output = ""
		for winner in self.winners.all():
			output += str(winner) + " "
		return output
