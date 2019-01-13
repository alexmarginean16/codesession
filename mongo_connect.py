from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_pymongo import PyMongo, pymongo
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os
import bcrypt
import shutil
from flask_table import Table, Col
import random
from random import randint
from flask_recaptcha import ReCaptcha
import flask
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter

app = Flask(__name__)

twitter_blueprint = make_twitter_blueprint(api_key='yY7Udfkef6H605h5gLaMwj6TG', api_secret='K7no2ekFvg5Dl7qTOGSd3PNxNEFzfAW4mgoVqiO7rghDjf95Tm')
app.register_blueprint(twitter_blueprint, url_prefix='/twitter_login')

app.config.update({
    'RECAPTCHA_ENABLED': True,
    'RECAPTCHA_SITE_KEY': "6LfsklYUAAAAAD07dM9yIFyMGICcXHDhuYqhBTsN",
    'RECAPTCHA_SECRET_KEY': "6LfsklYUAAAAALAw5kj0aJntgaVDrZrUrGhnMUpl"
})

#RECAPTCHA_ENABLED = True
#RECAPTCHA_SITE_KEY = "6LfsklYUAAAAAD07dM9yIFyMGICcXHDhuYqhBTsN"
#RECAPTCHA_SECRET_KEY = "6LfsklYUAAAAALAw5kj0aJntgaVDrZrUrGhnMUpl"
#RECAPTCHA_THEME = "dark"
#RECAPTCHA_TYPE = "image"
#RECAPTCHA_SIZE = "compact"
#RECAPTCHA_RTABINDEX = 10

recaptcha = ReCaptcha()
recaptcha.init_app(app)

app.config['MONGO_DBNAME'] = 'csmongo'
app.config['MONGO_URI'] = 'mongodb://csmongo:csmongo1@ds143388.mlab.com:43388/csmongo'

mongo = PyMongo(app)

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/twitter')
def twitter_login():
    if not twitter.authorized:
        return redirect(url_for('twitter.login'))

    account_info = twitter.get('account/settings.json')
    account_info_more = twitter.get('account/verify_credentials.json')
    if account_info.ok:
    	account_info_json = account_info.json()
    	account_info_more_json = account_info_more.json()

    	users = mongo.db.users
    	existing_user = users.find_one({'username' : account_info_json['screen_name']})
    	if existing_user is None:
    		users.insert({'username' : account_info_json['screen_name'], 'email' : 'utilizator twitter', 'password' : '-', 'firstname' : account_info_more_json['name'], 'lastname' : '', 'points' : 10, 'gamesp' : 0, 'gamesw' : 0, 'ac1' : 0, 'ac2' : 0, 'ac3' : 0, 'ac4' : 0, 'ac5' : 0, 'ac6' : 0, 'online' : 1, 'ingame' : 0, 'admin' : 0, 'imglink' : account_info_more_json['profile_image_url_https']})
    		session['username'] = account_info_json['screen_name']
    		shutil.copy('static/images/person_blank.png', 'static/img/'+session['username']+'.png')
    	else:
    		session['username'] = account_info_json['screen_name']
    		return redirect(url_for('index'))

@app.route('/')
def index():
	if 'username' in session:
		users = mongo.db.users
		login_user = users.find_one({'username' : session['username']})
		if login_user['admin'] == 1:
			return redirect(url_for('admin'))
		games = mongo.db.games
		items = users.find({'online' : 1}).sort('username', pymongo.ASCENDING)

		game_user = games.find_one({'player1' : session['username']})
		if game_user and game_user['sursa1'] == 0:
			return render_template('index2.html', user = items, uname = session['username'], usrn = game_user['player2'], grad = '1')

		game_user = games.find_one({'player2' : session['username']})
		if game_user and game_user['sursa2'] == 0:
			return render_template('index2.html', user = items, uname = session['username'], usrn = game_user['player1'], grad = '2')

		return render_template('index.html', user = items, uname = session['username'])
	else:
		return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		if recaptcha.verify():

			users = mongo.db.users
			login_user = users.find_one({'email' : request.form['email']})

			if login_user:
				if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
					session['username'] = login_user['username']#request.form['username']
					login_user['online'] = 1
					users.save(login_user)
					return redirect(url_for('index'))
			error = 'Numele de utilizator sau parola sunt gresite'
			return render_template('login.html', error=error)
		else:
			error = 'Invalid captcha'
			return render_template('login.html', error=error)
	else:
		return render_template('login.html')


@app.route('/inregistrare', methods=['POST', 'GET']) 
def inregistrare():
	if request.method == 'POST':
		users = mongo.db.users

		if request.form['username'] == "" or request.form['firstname'] == "" or request.form['lastname'] == "" or request.form['email'] == "" or request.form['password'] == "":
			return render_template('signup.html')

		if request.form['username'] == " " or request.form['firstname'] == " " or request.form['lastname'] == " " or request.form['email'] == " " or request.form['password'] == " ":
			return render_template('signup.html')

		existing_user = users.find_one({'username' : request.form['username']})

		if existing_user is None:
			if request.form['password'] == request.form['passwordrep']:
				hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
				users.insert({'username' : request.form['username'], 'email' : request.form['email'], 'password' : hashpass, 'firstname' : request.form['firstname'], 'lastname' : request.form['lastname'], 'points' : 10, 'gamesp' : 0, 'gamesw' : 0, 'ac1' : 0, 'ac2' : 0, 'ac3' : 0, 'ac4' : 0, 'ac5' : 0, 'ac6' : 0, 'online' : 1, 'ingame' : 0, 'admin' : 0, 'imglink' : None})
				session['username'] = request.form['username']
				shutil.copy('static/images/person_blank.png', 'static/img/'+session['username']+'.png')
				return redirect(url_for('index'))
			else:
				error = 'Parolele nu coincid'
				return render_template('signup.html', error=error)

		else:
			error = 'Deja exista acest nume de utilizator'
			return render_template('signup.html', error=error)

	return render_template('signup.html')

@app.route('/profil')
def profil():
	if 'username' in session:
		users = mongo.db.users
		login_user = users.find_one({'username' : session['username']})

		if login_user['ac1'] is 0 and login_user['gamesp'] >= 1:
			login_user['points'] += 15
			login_user['ac1'] = 1
			users.save(login_user)
		if login_user['ac2'] is 0 and login_user['gamesp'] >= 10:
			login_user['points'] += 15
			login_user['ac2'] = 1
			users.save(login_user)
		if login_user['ac3'] is 0 and login_user['gamesp'] >= 50:
			login_user['points'] += 25
			login_user['ac3'] = 1
			users.save(login_user)
		if login_user['ac4'] is 0 and login_user['gamesw'] >= 1:
			login_user['points'] += 30
			login_user['ac4'] = 1
			users.save(login_user)
		if login_user['ac5'] is 0 and login_user['gamesw'] >= 10:
			login_user['points'] += 40
			login_user['ac5'] = 1
			users.save(login_user)
		if login_user['ac6'] is 0 and login_user['gamesw'] >= 50:
			login_user['points'] += 50
			login_user['ac6'] = 1
			users.save(login_user)
		return render_template('profil.html', usrn = session['username'], uname = session['username'], email = login_user['email'], firstname = login_user['firstname'], lastname = login_user['lastname'], points = login_user['points'], nrjocuri = login_user['gamesp'], nrjocuric = login_user['gamesw'], imglink = login_user['imglink'])
	else:
		return redirect(url_for('login'))

@app.route('/upload', methods=['GET','POST'])
def upload():
	if request.method == 'POST' and 'photo' in request.files:
		file = request.files['photo']
		file.filename = session['username']
		file.save("static/img/"+file.filename+'.png')
		return redirect(url_for('profil'))

	return render_template('upload.html', uname = session['username'])

class ItemTable(Table):
	lastname = Col('Nume')
	firstname = Col('Prenume')
	username = Col('Nume de utilizator')
	points = Col('Punctaj')


@app.route('/clasament', methods=['GET'])
def clasament():
	users = mongo.db.users
	login_user = users.find_one({'username' : session['username']})
	if login_user['admin'] == 1:
		return redirect(url_for('clasamentadmin'))
	items = users.find().sort('points', pymongo.DESCENDING)
	return render_template('clasament.html', user=items, uname=session['username'])

@app.route('/clasamentadmin', methods=['GET'])
def clasamentadmin():
	users = mongo.db.users
	items = users.find().sort('points', pymongo.DESCENDING)
	return render_template('clasament2.html', user=items, uname=session['username'])

@app.route('/editpoints/<usrn>', methods=['POST', 'GET'])
def editpoints(usrn):
	users = mongo.db.users
	that_user = users.find_one({'username' : usrn})
	login_user = users.find_one({'username' : session['username']})
	if login_user['admin'] == 1:
		if request.method == 'POST':
			that_user['points'] = int(request.form['points'])
			that_user['gamesp'] = int(request.form['gamesp'])
			that_user['gamesw'] = int(request.form['gamesw'])
			users.save(that_user)
			return redirect(url_for('clasamentadmin'))
		return render_template('editpoints.html', uname=session['username'], usrn=usrn)
	return redirect(url_for('index'))

@app.route('/profilpublic/<usrn>')
def profilpublic(usrn):
	if usrn and 'username' in session:
		users = mongo.db.users
		login_user = users.find_one({'username' : usrn})

		if login_user['ac1'] is 0 and login_user['gamesp'] >= 1:
			login_user['points'] += 15
			login_user['ac1'] = 1
			users.save(login_user)
		if login_user['ac2'] is 0 and login_user['gamesp'] >= 10:
			login_user['points'] += 15
			login_user['ac2'] = 1
			users.save(login_user)
		if login_user['ac3'] is 0 and login_user['gamesp'] >= 50:
			login_user['points'] += 25
			login_user['ac3'] = 1
			users.save(login_user)
		if login_user['ac4'] is 0 and login_user['gamesw'] >= 1:
			login_user['points'] += 30
			login_user['ac4'] = 1
			users.save(login_user)
		if login_user['ac5'] is 0 and login_user['gamesw'] >= 10:
			login_user['points'] += 40
			login_user['ac5'] = 1
			users.save(login_user)
		if login_user['ac6'] is 0 and login_user['gamesw'] >= 50:
			login_user['points'] += 50
			login_user['ac6'] = 1
			users.save(login_user)
		return render_template('profil.html', usrn = usrn, uname = session['username'], email = login_user['email'], firstname = login_user['firstname'], lastname = login_user['lastname'], points = login_user['points'], nrjocuri = login_user['gamesp'], nrjocuric = login_user['gamesw'], imglink = login_user['imglink'])
	else:
		return redirect(url_for('index'))

@app.route('/remove')
def remove():
	if 'username' in session:
		users = mongo.db.users
		login_user = users.find_one({'username' : session['username']})
		users.remove(login_user)
		session.pop('username', None)
		return redirect(url_for('index'))

@app.route('/alege')
def alege():
	if 'username' in session:
		users = mongo.db.users
		login_user = users.find_one({'username' : session['username']})
		error = None
		if login_user['ingame'] is 0:
			games = mongo.db.games
			game_user = games.find_one({'player1' : session['username']})
			if game_user:
				error = 'Solutia ta nu a fost inca corectata'
				return render_template('alege.html', uname = session['username'], error=error)
			game_user = games.find_one({'player2' : session['username']})
			if game_user:
				error = 'Solutia ta nu a fost inca corectata'
				return render_template('alege.html', uname = session['username'], error=error)

			grad = 1
			items = users.find({'online' : 1, 'ingame' : 0}).sort('username', pymongo.ASCENDING)
			return render_template('alege.html', grad=grad, user = items , uname = session['username'], error=error)
		else:
			error = 'Esti deja intr-un joc sau solutia ta inca nu a fost corectata'
			return render_template('alege.html', uname = session['username'], error=error)

	return redirect(url_for('index'))

@app.route('/injoc/<usrn>/<grad>', methods=['POST', 'GET'])
def injoc(usrn,grad):
	if 'username' in session:
		users = mongo.db.users
		login_user = users.find_one({'username' : session['username']})
		
		if request.method == 'POST':
			if grad == '1':
				games = mongo.db.games
				game_user = games.find_one({'player1' : session['username']})
				game_user['sursa1'] = request.form['solutie']
				game_user['trimis1'] = 1
				games.save(game_user)
				login_user['ingame'] = 0
				users.save(login_user)
				return redirect(url_for('index'))
			if grad == '2':
				games = mongo.db.games
				game_user = games.find_one({'player2' : session['username']})
				game_user['sursa2'] = request.form['solutie']
				game_user['trimis2'] = 1
				games.save(game_user)
				login_user['ingame'] = 0
				users.save(login_user)
				return redirect(url_for('index'))

		if usrn:
			if usrn == session['username']:
				return redirect(url_for('index'))
			else:
				if login_user['ingame'] == 0 and grad == '1':
					games = mongo.db.games
					game_user = games.find_one({'player2' : session['username']})
					if game_user:
						return redirect(url_for('index'))


					prob = mongo.db.prob
					items = prob.find().sort("nr", pymongo.DESCENDING).limit(1)
					nr_prob = int(items[0]["nr"])


					random_number = random.randint(1, nr_prob)
					prob_curenta = prob.find_one({'nr' : random_number})

					games.insert({'player1' : session['username'], 'player2' : usrn, 'sursa1' : 0, 'sursa2' : 0, 'corectat' : 0, 'trimis1' : 0, 'trimis2' : 0, 'numeprob' : prob_curenta['nume'], 'enunt' : prob_curenta['enunt'], 'in' : prob_curenta['datedeintrare'], 'out' : prob_curenta['datedeiesire']})
					login_user['ingame'] = 1
					users.save(login_user)

					game_user = games.find_one({'player1' : session['username']})

					return render_template('game.html', grad=grad, usrn=usrn, uname=session['username'], numeprob=game_user['numeprob'], enunt=game_user['enunt'], intrare=game_user['in'], iesire=game_user['out'])
				else:
					games = mongo.db.games
					login_user['ingame'] = 1
					users.save(login_user)

					game_user = games.find_one({'player1' : session['username']})
					if game_user:
						return render_template('game.html', grad=grad, usrn=usrn, uname=session['username'], numeprob=game_user['numeprob'], enunt=game_user['enunt'], intrare=game_user['in'], iesire=game_user['out'])
					else:
						game_user = games.find_one({'player2' : session['username']})
						return render_template('game.html', grad=grad, usrn=usrn, uname=session['username'], numeprob=game_user['numeprob'], enunt=game_user['enunt'], intrare=game_user['in'], iesire=game_user['out'])
		else:
			return redirect(url_for('index'))

@app.route('/testaree')
def testaree():
	prob = mongo.db.prob
	items = prob.find().sort("nr", pymongo.DESCENDING).limit(1)
	nr_prop = int(items[0]["nr"])
	return str(nr_prop)

	#results = list(prob.find().sort("nr", pymongo.DESCENDING).limit(1))
	#return int(results[0]["nr"])


@app.route('/admin')
def admin():
	users = mongo.db.users
	games = mongo.db.games
	items = games.find({'trimis1' : 1, 'trimis2' : 1})
	return render_template('admin.html', solutii = items, uname = session['username'])

@app.route('/solutie/<player1>')
def solu(player1):
	games = mongo.db.games
	users = mongo.db.users
	login_user = users.find_one({'username' : session['username']})
	if login_user['admin'] == 1:
		game_user = games.find_one({'player1' : player1})
		if game_user:
			return render_template('solutie.html', uname = session['username'], player1 = game_user['player1'], player2 = game_user['player2'], sursa1 = game_user['sursa1'], sursa2 = game_user['sursa2'])
		else:
			return redirect(url_for('index'))
	else:
		return redirect(url_for('index'))

@app.route('/puncteaza/<player1>', methods=['POST', 'GET'])
def puncteaza(player1):
	if request.method == 'POST':
		games = mongo.db.games
		users = mongo.db.users
		game_user = games.find_one({'player1' : player1})
		user_one = users.find_one({'username' : game_user['player1']})
		user_two = users.find_one({'username' : game_user['player2']})

		user_one['points'] += int(request.form['pct1'])
		user_two['points'] += int(request.form['pct2'])

		if int(request.form['pct1']) > int(request.form['pct2']):
			user_one['gamesw'] += 1
		else:
			user_two['gamesw'] += 1

		user_one['gamesp'] += 1
		user_two['gamesp'] += 1

		users.save(user_one)
		users.save(user_two)

		games.remove(game_user)
		return redirect(url_for('index'))
	else:
		return redirect(url_for('index'))

@app.route('/adaugaprobleme', methods=['POST', 'GET'])
def adaugaprobleme():
	users = mongo.db.users
	login_user = users.find_one({'username' : session['username']})
	if login_user and login_user['admin'] == 1:
		if request.method == 'POST':
			prob = mongo.db.prob

			items = prob.find().sort("nr", pymongo.DESCENDING).limit(1)
			nr_prob = int(items[0]["nr"]) + 1

			prob.insert({'nr' : nr_prob, 'nume' : request.form['titlu'], 'enunt' : request.form['enunt'], 'datedeintrare' : request.form['datedeintrare'], 'datedeiesire' : request.form['datedeiesire']})
			return redirect(url_for('index'))

		return render_template('adaugaprobleme.html', uname = session['username'])

	return redirect(url_for('index'))

@app.route('/logout')
def logout():
	users = mongo.db.users
	login_user = users.find_one({'username' : session['username']})
	login_user['online'] = 0
	users.save(login_user)
	session.pop('username', None)
	return redirect(url_for('index'))


@app.route('/acasa')
def acasa():
	return render_template('acasa.html')

@app.route('/despre')
def despre():
	return render_template('despre.html')

if __name__ == '__main__':
	app.secret_key = 'mysecret'
	app.run(debug=True)



