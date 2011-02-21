from operator import itemgetter

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime, timedelta
import random

from pongking.pong.models import League
from pongking.pong.models import Game
from pongking.pong.models import Player
from pongking.pong.models import Award


def addPlayer(request):
	message = ""
	if request.method == 'POST':
		player = Player()
		player.name = request.POST.get('firstname') + " " + request.POST.get('lastname')
		if request.POST.get('admin')=="1":
			email = request.POST.get("email")
			pw = request.POST.get("pw")
			addUser(player, email, pw)
		player.save()
		message += "new player '" + player.name + "' has been created"	
	
	return render_to_response('addplayer.html', {'message' : message}, context_instance=RequestContext(request))

#saves the given player, associates the player with a new user, saves the player
def addUser(player, email, pw):
	player.save()
	player.user  = User.objects.create_user(player.name,email,pw) 
	player.save()

def addGame(request):
	message = ""
	if request.method == 'POST':
		message = "game recorded"
		error = "game not recorded: "
		game = Game()
		
		player_names = getPlayerNames(request)	
		cups = request.POST.get('cupspread')

		#win1, lose1 must not be blank. win2, lose2 can be blank. finds all errors	
		error += validateNames([player_names[0], player_names[2]], False) + validateNames([player_names[1],player_names[3]], True)
		
		if len(error) > 25:
			message = error
		else:
			psrchange(player_names, cups)
			game.save()

	#have sean do (if messasge: report message) empty message evaluates to false
	return render_to_response('addGame.html', {'message' : message}, context_instance=RequestContext(request))


#returns an array containing the names of the four players in a game. 
#returns "" for extra players if 1v1 game
def getPlayerNames(request):	
	win1 = request.POST.get('winner1')
	lose1 = request.POST.get('loser1')
	win2 = request.POST.get('winner2')
	lose2 = request.POST.get('loser2')
	return [win1,win2,lose1,lose2]

	
def addLeague(request):
	error = ""
	if request.method == 'POST':
		name = request.POST.get('league')#
		if name in [l.name for l in League.objects.all()]:
			error = "A league with the name " + name + " already exists"
		else: 
			l = League()
			l.name = name
			l.save()
	return render_to_response('addLeague.html', {'message' : error}, context_instance=RequestContext(request))


#checks if all names in the given list are names of players in the given league.
#if blank_ok is True, an empty string is acceptable in place of a name. returns a string reporting errors
def validateNames(names, blank_ok):
	error = ""
	league = League.objects.get(name=names[0])
	valid_names = [p.name for p in league.players.all()]
	for name in names:
		if name not in valid_names:
			if name == "" and blank_ok:
				continue
			error = string.join(error, "invalid name: ", name, " ")
	return error		
	
def psrChange(w1, w2, l1, l2):
	w = 2
	q = 8.5
	winteamrank = pow((pow(w1,w) + pow(w2,w)),(1./w))
	loseteamrank = pow((pow(l1,w) + pow(l2,w)),(1./w))
	winQ = pow(10,winteamrank/185)
	loseQ = pow(10,loseteamrank/185)
	winP = winQ/(winQ+loseQ)
	loseP = 1-winP
	print winteamrank
	print loseteamrank
	print winteamrank/loseteamrank
	print "win/lose for team 1"	
	print winP
	print loseP
	#print "Ks"
	#print "lose:" + str(getK(w1)*winP) + " win: " + str(getK(w1)*loseP)
	#print getK(w2)*winP
	#print getK(l1)
	print
	w1 += getK(w1)*loseP
	w2 += getK(w2)*loseP
	print w1
	print w2
	l1 -= getK(l1)*winP
	l2 -= getK(l2)*winP	
	print l1
	print l2


def getK(p):
	return min(40, (40 - ( (p - 1430) / 8.5)))
