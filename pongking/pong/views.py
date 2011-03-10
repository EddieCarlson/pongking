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


def add_player(request):
	message = ""
	if request.method == 'POST':
		player = Player()
		player.name = request.POST.get('firstname') + " " + request.POST.get('lastname')
		if request.POST.get('admin')=="1":
			email = request.POST.get("email")
			pw = request.POST.get("pw")
			add_user(player, email, pw)
		player.save()
		message += "new player '" + player.name + "' has been created"	
	
	return render_to_response('addplayer.html', {'message' : message}, context_instance=RequestContext(request))

def navbar(request):
	
	return render_to_response('navbar.html', {}, context_instance=RequestContext(request))

def mobile_menu(request):
	
	return render_to_response('mobilemenu.html', {}, context_instance=RequestContext(request))

def mobile_rank(request):
	players = Player.objects.all()#TODO Eddie make this eventually for leagues
	return render_to_response('mobilerank.html', {'players' : players}, context_instance=RequestContext(request))

#saves the given player, associates the player with a new user, saves the player
def add_user(player, email, pw):
	player.save()
	u = User.objects.create_user(email, email, pw)
	u.save()
	player.user  = u 
	player.save()

def get_level(u,s):
	return max(int(u-(3*s))+1,0)

def add_game(request):
	p = ['Eddie Carlson | Sean Holt', 'Riley Strong | Phil Kimmey', 'Jason Bourne | Neo']
	players = Player.objects.all()#TODO Eddie make this eventually for leagues
	message = ""
	if request.method == 'POST':
		message = "game recorded"
		error = "game not recorded: "
		game = Game()
		game.recorder = request.user	
		player_names = get_player_names(request, game)	
		game.cupspread = request.POST.get('cupspread')

		
		#win1, lose1 must not be blank. win2, lose2 can be blank. finds all errors	
		error += validate_names(player_names, request.user) 
		
		if len(error) > 25:
			message = error
		else:
			rating_change(player_names, game)
			game.save()


	#have sean do (if messasge: report message) empty message evaluates to false
	return render_to_response('addgame.html', {'message' : message, 'p':p, 'players': players}, context_instance=RequestContext(request))

def add_game_mobile(request):
	p = ['Eddie Carlson & Sean Holt', 'Riley Strong & Phil Kimmey', 'Jason Bourne & Neo']
	players = Player.objects.all()#TODO Eddie make this eventually for leagues
	message = ""
	if request.method == 'POST':
		message = "game recorded"
		error = "game not recorded: "
		game = Game()
		game.recorder = request.user	
		player_names = get_player_names(request, game)	
		game.cupspread = request.POST.get('cupspread')

		
		#win1, lose1 must not be blank. win2, lose2 can be blank. finds all errors	
		error += validate_names(player_names, request.user) 
		
		if len(error) > 25:
			message = error
		else:
			ratingChange(player_names, game)
			game.save()
		p = ['sean', 'eddie']

	#have sean do (if messasge: report message) empty message evaluates to false
	return render_to_response('addgamemobile.html', {'message' : message, 'p':p, 'players': players}, context_instance=RequestContext(request))


#returns an array containing the names of the four players in a game. 
#returns "" for extra players if 1v1 game
def get_player_names(request, game):	
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

	
def add_league(request):
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
def validate_names(names, user):
	error = ""
	league = user.player_set.all()[0].league
	valid_names = [p.name for p in league.player_set.all()]
	for name in names:
		if name not in valid_names:
			error += "invalid name: " + name + " "
	return error		
	


def rating_change(player_names, game):
	allp = Player.objects.all()
	players = [allp.get(name=n) for n in player_names]
	means = [p.mean for p in players]
	stdevs = [p.stdev for p in players]
	
	ci = 0
	for si in stdevs:
		ci += pow(si,2)
	ci += (625./18)
	c = math.sqrt(ci)
	
	if len(means) == 2:	
		t = (means[0]-means[1])/c
	else:
		t = (means[0] + means[1] - means[2] - means[3])/c
	
	S = 0
	for n in range(60):
		S += (pow(-1,n) * pow((t/math.sqrt(2)),(2*n+1))) / (math.factorial(n)*(2*n+1))
	
	v = math.exp(-pow(t,2)/2.)/(math.sqrt(2)*S+math.sqrt(math.pi/2))
	w = v * (v+t)

	size = int(len(means)/2)
	for i in range(size):
		means[i] += pow(stdevs[i], 2) * v/c
	for i in range(size):
		means[i+size] -= pow(stdevs[i+size], 2) * v/c
	
	for i in range(len(stdevs)):
		stdevs[i] = math.sqrt(pow(stdevs[i],2) * (1-((pow(stdevs[i],2)*w/pow(c,2)))))

	L = []
	for i in range(len(stdevs)):
		L.append(means[i]-(3*stdevs[i]))
	
	game.win1delta = L[0]
	if len(stdevs) == 2:
		game.lose1delta = L[1]
	else:
		game.win2delta = L[1]
		game.lose1delta = L[2]
		game.lose2delta = L[3]
	
	for i in range(len(means)):
		players[i].mean = means[i]
		players[i].stdev = stdevs[i]
		players[i].level = get_level(means[i],stdevs[i])
		players[i].save()



def login_page(request):
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









