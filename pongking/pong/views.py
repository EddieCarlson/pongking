from operator import itemgetter

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime, timedelta
import random, math

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

def navbar(request):
	
	
	return render_to_response('navbar.html', {}, context_instance=RequestContext(request))

def mobileMenu(request):
	
	return render_to_response('mobilemenu.html', {}, context_instance=RequestContext(request))

def mobileRank(request):
	rank = ['Sean Holt </td> <td> 17.4', 'Eddie Carlson </td> <td> 16.4', 'Daniel Rodriguez </td> <td> 14.2']
	return render_to_response('mobilerank.html', {'rank' : rank}, context_instance=RequestContext(request))

#saves the given player, associates the player with a new user, saves the player
def addUser(player, email, pw):
	player.save()
	u = User.objects.create_user(email, email, pw)
	u.save()
	player.user  = u 
	player.save()

def L(u,s):
	return max(int(u-(3*s))+1,0)

def addGame(request):
	p = ['Eddie Carlson | Sean Holt', 'Riley Strong | Phil Kimmey', 'Jason Bourne | Neo']
	message = ""
	if request.method == 'POST':
		message = "game recorded"
		error = "game not recorded: "
		game = Game()
		game.recorder = request.user	
		player_names = getPlayerNames(request, game)	
		game.cupspread = request.POST.get('cupspread')

		
		#win1, lose1 must not be blank. win2, lose2 can be blank. finds all errors	
		error += validateNames(player_names, request.user) 
		
		if len(error) > 25:
			message = error
		else:
			ratingChange(player_names, game)
			game.save()


	#have sean do (if messasge: report message) empty message evaluates to false
	return render_to_response('addgame.html', {'message' : message, 'p':p}, context_instance=RequestContext(request))

def addGameMobile(request):
	p = ['Eddie Carlson & Sean Holt', 'Riley Strong & Phil Kimmey', 'Jason Bourne & Neo']
	message = ""
	if request.method == 'POST':
		message = "game recorded"
		error = "game not recorded: "
		game = Game()
		game.recorder = request.user	
		player_names = getPlayerNames(request, game)	
		game.cupspread = request.POST.get('cupspread')

		
		#win1, lose1 must not be blank. win2, lose2 can be blank. finds all errors	
		error += validateNames(player_names, request.user) 
		
		if len(error) > 25:
			message = error
		else:
			ratingChange(player_names, game)
			game.save()
		p = ['sean', 'eddie']

	#have sean do (if messasge: report message) empty message evaluates to false
	return render_to_response('addgamemobile.html', {'message' : message, 'p':p}, context_instance=RequestContext(request))


#returns an array containing the names of the four players in a game. 
#returns "" for extra players if 1v1 game
def getPlayerNames(request, game):	
	win1 = request.POST.get('winner1')
	lose1 = request.POST.get('loser1')
	win2 = request.POST.get('winner2')
	lose2 = request.POST.get('loser2')
	
	game.winner1 = win1
	game.loser1 = lose1

	if not win2 == "":
		game.winner2 = win2
		game.loser2 = lose2	
		return [win1,win2,lose1,lose2]
	
	return [win1,lose1]

	
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
def validateNames(names, user):
	error = ""
	league = user.player_set.all()[0].league
	valid_names = [p.name for p in league.player_set.all()]
	for name in names:
		if name not in valid_names:
			error += "invalid name: " + name + " "
	return error		
	


def ratingChange(player_names, game):
	allp = Player.objects.all()
	players = [allp.get(name=n) for n in player_names]
	u = [p.u for p in players]
	s = [p.s for p in players]
	
	ci = 0
	for si in s:
		ci += pow(si,2)
	ci += (625./18)
	c = math.sqrt(ci)
	
	if len(u) == 2:	
		t = (u[0]-u[1])/c
	else:
		t = (u[0] + u[1] - u[2] - u[3])/c
	
	S = 0
	for n in range(60):
		S += (pow(-1,n) * pow((t/math.sqrt(2)),(2*n+1))) / (math.factorial(n)*(2*n+1))
	
	v = math.exp(-pow(t,2)/2.)/(math.sqrt(2)*S+math.sqrt(math.pi/2))
	w = v * (v+t)

	size = int(len(u)/2)
	for i in range(size):
		u[i] += pow(s[i], 2) * v/c
	for i in range(size):
		u[i+size] -= pow(s[i+size], 2) * v/c
	
	for i in range(len(s)):
		s[i] = math.sqrt(pow(s[i],2) * (1-((pow(s[i],2)*w/pow(c,2)))))

	L = []
	for i in range(len(s)):
		L.append(u[i]-(3*s[i]))
	
	game.win1delta = L[0]
	if len(s) == 2:
		game.lose1delta = L[1]
	else:
		game.win2delta = L[1]
		game.lose1delta = L[2]
		game.lose2delta = L[3]
	
	for i in range(len(u)):
		players[i].u = u[i]
		players[i].s = s[i]
		players[i].save()



def loginpage(request):
	message = ""
	if request.method == "POST":
		email = request.POST.get("email")
		pw = request.POST.get("pw")
		user = authenticate(username=email, password=pw)
		if user is not None and user.is_active:
			login(request, user)
			return HttpResponseRedirect('addgame/')
			#return render_to_response('recordgame.html',{},context_instance=RequestContext(request))
		else: 
			message += "incorrect email/password"
	return render_to_response('login.html', {'message' : message}, context_instance=RequestContext(request))









