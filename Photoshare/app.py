######################################
# author ben lawson <balawson@bu.edu>
# Edited by: Craig Einstein <einstein@bu.edu>
######################################
# Some code adapted from
# CodeHandBook at http://codehandbook.org/python-web-application-development-using-flask-and-mysql/
# and MaxCountryMan at https://github.com/maxcountryman/flask-login/
# and Flask Offical Tutorial at  http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
# see links for further understanding
###################################################

import flask
from flask import Flask, Response, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
#import flask.ext.login as flask_login
import flask_login
#for image uploading
from werkzeug import secure_filename
import os, base64
# import numpy
# import cv2
from PIL import Image
import datetime
from flask import send_from_directory

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!

#These will need to be changed according to your creditionals
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password' #CHANGE THIS TO YOUR MYSQL PASSWORD
app.config['MYSQL_DATABASE_DB'] = 'photoshare'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#begin code used for login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()
cursor.execute("SELECT email from Users")
users = cursor.fetchall()

def getUserList():
	cursor = conn.cursor()
	cursor.execute("SELECT email from Users")
	return cursor.fetchall()

class User(flask_login.UserMixin):
	pass

@login_manager.user_loader
def user_loader(email):
	users = getUserList()
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	return user

@login_manager.request_loader
def request_loader(request):
	users = getUserList()
	email = request.form.get('email')
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email))
	data = cursor.fetchall()
	pwd = str(data[0][0] )
	user.is_authenticated = request.form['password'] == pwd
	return user


'''
A new page looks like this:
@app.route('new_page_name')
def new_page_function():
	return new_page_html
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
	if flask.request.method == 'GET':
		return '''
			   <form action='login' method='POST'>
				<input type='text' name='email' id='email' placeholder='email'></input>
				<input type='password' name='password' id='password' placeholder='password'></input>
				<input type='submit' name='submit'></input>
			   </form></br>
		   <a href='/'>Home</a>
			   '''
	#The request method is POST (page is recieving data)
	email = flask.request.form['email']
	cursor = conn.cursor()
	#check if email is registered
	if cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email)):
		data = cursor.fetchall()
		pwd = str(data[0][0] )
		if flask.request.form['password'] == pwd:
			user = User()
			user.id = email
			flask_login.login_user(user) #okay login in user
			return flask.redirect(flask.url_for('protected')) #protected is a function defined in this file

	#information did not match
	return "<a href='/login'>Try again</a>\
			</br><a href='/register'>or make an account</a>"

@app.route('/logout')
def logout():
	flask_login.logout_user()
	return render_template('hello.html', message='Logged out')

@login_manager.unauthorized_handler
def unauthorized_handler():
	return render_template('unauth.html')

#you can specify specific methods (GET/POST) in function header instead of inside the functions as seen earlier
@app.route("/register/", methods=['GET'])
def register():
	return render_template('improved_register.html', supress='True')


@app.route("/register/", methods=['POST'])
def register_user():
	try:
		masterId = getUserIdFromEmail("Master@Master.com")
		cursor = conn.cursor()
		email=request.form.get('email')
				# print email
		password=request.form.get('password')
		f = request.files['profilePhoto']
		if f.filename == '':
			photo_data = getUserProfile(masterId)
		else:
			photo_data = base64.standard_b64encode(f.read())
		firstName = request.form.get('firstname')
		lastName = request.form.get('lastname')
		dob = request.form.get('birthday')
		homeTown = request.form.get('hometown')
		gender = request.form.get('gender')
		gender = str(gender)
		bio = request.form.get('bio')
		print "NEXT"
	except Exception as E:
		print E
		print "couldn't find all tokens1" #this prints to shell, end users will not see this (all print statements go to shell)
		return flask.redirect(flask.url_for('register'))
	test =  isEmailUnique(email)
	print test
	if test:
		print cursor.execute("INSERT INTO Users (imgdata, email, password, homeTown, dob, gender, firstName, lastName, bio) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')".format(photo_data, email, password, homeTown, dob, gender, firstName, lastName, bio))
		conn.commit()
		#log user in
		user = User()
		user.id = email
		flask_login.login_user(user)
		return render_template('hello.html', name=email, message='Account Created!')
	else:
		print "couldn't find all tokens2"
		return render_template('accountExists.html')
		#return flask.redirect(flask.url_for('register'))


def getUsersPhotos(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT imgdata, picture_id, caption FROM Pictures WHERE user_id = '{0}'".format(uid))
	return cursor.fetchall() #NOTE list of tuples, [(imgdata, pid), ...]

def getUserProfile(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT imgdata FROM Users WHERE user_id = '{0}'".format(uid))
	return cursor.fetchone()[0]

def getUserIdFromEmail(email):
	cursor = conn.cursor()
	cursor.execute("SELECT user_id  FROM Users WHERE email = '{0}'".format(email))
	return cursor.fetchone()[0]

def isEmailUnique(email):
	#use this to check if a email has already been registered
	cursor = conn.cursor()
	if cursor.execute("SELECT email  FROM Users WHERE email = '{0}'".format(email)):
		#this means there are greater than zero entries with that email
		return False
	else:
		return True

def getHomeTown(uid):
	cursor = conn.cursor()
	cursor.execute("Select homeTown From Users WHERE user_id = '{0}'".format(uid))
	return cursor.fetchone()[0]

def getfirstName(uid):
	cursor = conn.cursor()
	cursor.execute("Select firstName From Users WHERE user_id = '{0}'".format(uid))
	return cursor.fetchone()[0]

def getlastName(uid):
	cursor = conn.cursor()
	cursor.execute("Select lastName From Users WHERE user_id = '{0}'".format(uid))
	return cursor.fetchone()[0]

def getGender(uid):
	cursor = conn.cursor()
	cursor.execute("Select gender From Users WHERE user_id = '{0}'".format(uid))
	return cursor.fetchone()[0]

def getDob(uid):
	cursor = conn.cursor()
	cursor.execute("Select dob from Users WHERE user_id = '{0}'".format(uid))
	return cursor.fetchone()[0]

def getUserPhotoID(imgdata):
	cursor = conn.cursor()
	cursor.execute("Select picture_id from Pictures WHERE imgdata = '{0}'".format(imgdata))
	return cursor.fetchone()[0]


def getUsersTags(uid):
	cursor = conn.cursor()
	cursor.execute("Select tag from Tags WHERE user_id = '{0}'".format(uid))
	return cursor.fetchall()

def getAllTags(tagG):
	cursor = conn.cursor()
	cursor.execute("Select tag from Tags WHERE tag = '{0}'".format(tagG))
	return cursor.fetchall()

def getAid(uid):
	cursor = conn.cursor()
	cursor.execute("Select aid from Users WHERE user_id = '{0}'".format(uid))
	return cursor.fetchone()[0]

def getAllAlbums(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT aid, nameAlbum FROM Album WHERE user_id = '{0}'".format(uid))
	return cursor.fetchall()

def getAidFromPhoto(pid):
	cursor = conn.cursor()
	cursor.execute("SELECT aid From Pictures WHERE picture_id = '{0}'".format(pid))
	return cursor.fetchone()[0]

def getUsersPhotosUpdated(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT imgdata, picture_id, aid FROM Pictures WHERE user_id = '{0}'".format(uid))
	return cursor.fetchall() #NOTE list of tuples, [(imgdata, pid), ...]

def getAllPhotosID():
	cursor = conn.cursor()
	cursor.execute("SELECT DISTINCT picture_id FROM Pictures")
	return cursor.fetchall()

def getAllPhotos2():
	cursor = conn.cursor()
	cursor.execute("SELECT picture_id, imgdata FROM Pictures")
	return cursor.fetchall()

def getAllPidFromImgdata(imgdatas):
	cursor = conn.cursor()
	cursor.execute("Select picture_id FROM Pictures WHERE imgdata ='{0}'".format(imgdatas))
	return cursor.fetchall()

def getAllPhotos(pid):
	cursor = conn.cursor()
	cursor.execute("SELECT imgdata FROM Pictures WHERE picture_id = '{0}'".format(pid))
	return cursor.fetchall()


def getNameFromID(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT email FROM Users WHERE user_id = '{0}'".format(uid))
	return cursor.fetchone()[0]
#end login code


def getGender(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT gender FROM Users WHERE user_id = '{0}'".format(uid))
	return cursor.fetchone()[0]

def getBio(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT bio FROM Users WHERE user_id = '{0}'".format(uid))
	return cursor.fetchone()[0]

def getfName(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT firstName FROM Users WHERE user_id = '{0}'".format(uid))
	return cursor.fetchone()[0]

def getlName(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT lastName FROM Users WHERE user_id = '{0}'".format(uid))
	return cursor.fetchone()[0]

@app.route('/profile')
@flask_login.login_required
def protected():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	print uid
	return render_template('hello.html', name=flask_login.current_user.id, message="Here's your profile", Picturephoto=getUserProfile(uid), homeTown=getHomeTown(uid), birthday=getDob(uid),  gender=getGender(uid), bio=getBio(uid), fName=getfName(uid), lastName=getlName(uid), photos = getUsersPhotos(uid))

#begin photo uploading code
# photos uploaded using base64 encoding so they can be directly embeded in HTML
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
@flask_login.login_required
def upload_file():
	if request.method == 'POST':
		uid = getUserIdFromEmail(flask_login.current_user.id)
		imgfile = request.files['photo']
		caption = request.form.get('caption')
		tag = request.form.get('tag')
		photo_data = base64.standard_b64encode(imgfile.read())
		cursor = conn.cursor()
		cursor.execute("INSERT INTO Pictures (imgdata, user_id, caption) VALUES ('{0}', '{1}', '{2}' )".format(photo_data,uid, caption))
		conn.commit()
		pid = getUserPhotoID(photo_data)
		cursor.execute("INSERT INTO Tags (tag, picture_id) VALUES ('{0}', '{1}')".format(tag, pid))
		conn.commit()
		return render_template('hello.html', name=flask_login.current_user.id, message='Photo uploaded!', photos=getUsersPhotos(uid))
	#The method is GET so we return a  HTML form to upload the a photo.
	else:
		return render_template('upload.html')

@app.route('/changeProfile', methods=['GET', 'POST'])
@flask_login.login_required
def changeProfilePicture():
	if request.method == 'POST':
		uid = getUserIdFromEmail(flask_login.current_user.id)
		imgfile = request.files['photo']
		photo_data = base64.standard_b64encode(imgfile.read())
		cursor = conn.cursor()
		cursor.execute("UPDATE Users SET imgdata = '{0}' WHERE user_id = '{1}'".format(photo_data, uid))
		conn.commit()
		return render_template('hello.html', name=flask_login.current_user.id, message="Here's your profile", Picturephoto=getUserProfile(uid), homeTown=getHomeTown(uid), birthday=getDob(uid))
	else:
		return render_template('changeProfile.html')

#end photo uploading code
@app.route('/albums', methods=['GET', 'POST'])
@flask_login.login_required
def createAlbum():
	if request.method == 'POST':
		print "HELLOOOOOOOOOOOOOOOOO"
		albumCreate = request.form.get('createAlbum')
		dateNow = datetime.datetime.now().date()
		print dateNow
		uid = getUserIdFromEmail(flask_login.current_user.id)
		cursor = conn.cursor()
		cursor.execute("Insert INTO Album (user_id, dateAlbum, nameAlbum) VALUES ('{0}', '{1}', '{2}')".format(uid, dateNow, albumCreate))
		conn.commit()
		return render_template('hello.html', name=flask_login.current_user.id, message="Here's your profile", Picturephoto=getUserProfile(uid), homeTown=getHomeTown(uid), birthday=getDob(uid))
	else:
		return render_template('albums.html')



# CHANGE THE AREA WHERE IT RENDERS TEMPLATE SO IT DOESNT REFRESH!!!!
# Create a helper function which grabs the album id that matches the album id in photos and display it.
@app.route('/viewAlbums', methods=['GET', 'POST'])
@flask_login.login_required
def chooseAlbum():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	if request.method == 'POST':
		print "it must of posted"
		print "Album Selected is:"
		albumNameSelect = request.form.get('albumName')
		print albumNameSelect
		print "The photo Selected is:"
		pictureSelected = request.form.get('photoAlbum')
		print pictureSelected
		cursor = conn.cursor()
		cursor.execute("UPDATE Pictures SET aid ='{0}' WHERE picture_id= '{1}'".format(albumNameSelect, pictureSelected))
		conn.commit()
		print "The photo belongs to this albumid"
		photoBelong = getAidFromPhoto(pictureSelected)
		print photoBelong
		return render_template('finishedAlbums.html', albums=getAllAlbums(uid), photoExist=getUsersPhotosUpdated(uid))
	else:
		print "else statement"
		return render_template("viewAlbums.html", albums=getAllAlbums(uid), photoExist=getUsersPhotos(uid))

#EDIT THIS!!!!!!
@app.route('/searchResults', methods=['GET', 'POST'])
def index():
	photoArray = []
	test = []
	if request.method == 'GET': #if request is get (user navigated to the URL)
		return render_template('search.html')
	else: #if request is post (user posted some information)
		query = request.form['QUERY'] #get information from the 'QUERY' row of the form
		print query #QUERY IS THE TAGGGG!!!
		next = query.split(",")
		# next = [x.strip() for x in query.split(',')]
		print next
		for x in next:
			print x
			try:
				data = extractData(x)
				cursor = conn.cursor()
				for x in data:
					test.append(x)
					test1 = list(set(test))
				for x in test1:
					cursor.execute("SELECT imgdata FROM Pictures WHERE picture_id = '{0}'".format(x[0]))
					pictures = cursor.fetchone()[0]
					photoArray.append(pictures)
				return render_template('searchResults.html', photos = photoArray)
			except Exception as e:
				return render_template('searchResults.html')

#defines a function for extracting the data from a query
#LATER ADD SEARCH FOR FRIENDS CAUSE RIGHT NOW ITS ONLY TAGS
def extractData(query):
	cursor = conn.cursor()
	cursor.execute("SELECT picture_id FROM Tags WHERE tag = '{0}'".format(query))
	data = cursor.fetchall() #fetches all rows of the query
	# cursor.close()
	# conn.close()
	return data

@app.route('/search', methods=['GET'])
def search():
	return render_template('search.html')

#default page
@app.route("/", methods=['GET'])
def hello():
	return render_template('hello.html', message='Welcome to Photoshare')

@app.route("/comments", methods=['GET', 'POST'])
def commentsID():
	dateNow = datetime.datetime.now().date()
	picturesID = request.form.get('commentsPID')
	uid = getUserIdFromEmail(flask_login.current_user.id)
	comments = request.form.get('commentT')
	if request.method == 'POST':
		p = getAllPhotos2()
		#picturesID = request.form.get('commentsPID')
		print "HI 2"
		print picturesID
		# comment = request.form.get('commentT')
		print "jasdlkjadsflkjfsadlkjsdalkda"
		print comments
		cursor = conn.cursor()
		cursor.execute("INSERT INTO Comment(texts, picture_id, dateRN, user_id) VALUES ('{0}', '{1}', '{2}', '{3}')".format(comments, picturesID, dateNow, uid))
		conn.commit()
		cursor.execute("SELECT imgdata FROM Pictures WHERE picture_id = '{0}'".format(picturesID))
		picture = cursor.fetchone()[0]
		# print picture
		return render_template('commentResult.html', photos = picture, comment = comments)
	else:
	 	print "HIsss"
	 	p = getAllPhotos2()
	 	return render_template('comments.html', pictures = p)

def grabMultipleComments(pid):
	cursor = conn.cursor()
	commentStorage = []
	commentsTemp = []
	for id in pid:
		cursor.execute("SELECT texts, user_id FROM Comment WHERE picture_id = '{0}'".format(id))
		comments = cursor.fetchall()
		print comments
		for next in comments:
			print next
			if next[1] is None:
				replace = 0
			else:
				g = str(getNameFromID(int(next[1])))
				p = str(next[0])
				commentsTemp.append(g)
				commentsTemp.append(p)
		print "HIHIHIHI"
		print commentsTemp
	print "jsdflksdfjlksdfjlksdfjskldfjsdflkjsdflkdsjf"
 	commentStorage.append(commentsTemp)
	print commentStorage
	return commentStorage


@app.route('/LookAlbums', methods = ['GET', 'POST'])
def showAllAlbums():
	cursor = conn.cursor()
	cursor.execute("SELECT aid, nameAlbum FROM Album")
	returnAlbum = cursor.fetchall()
	cursor.execute("SELECT imgdata, caption, aid FROM Pictures")
	returnPictures = cursor.fetchall()
	return render_template('LookAlbums.html', albums = returnAlbum, photoExist = returnPictures)

@app.route('/makeFriends', methods =['GET', 'POST'])
def makeFriends():
	cursor = conn.cursor()
	cursor.execute("SELECT email, user_id FROM Users")
	userList = cursor.fetchall()
	uid = getUserIdFromEmail(flask_login.current_user.id)
	friend = request.form.get('friend')
	if request.method == 'POST':
		friendss = []
		cursor.execute("Insert Friends(user_id, user_id_friend) VALUES ('{0}', '{1}')".format(uid, friend))
		conn.commit()
		print friend
		cursor.execute("Select user_id_friend FROM Friends WHERE user_id = '{0}'".format(uid))
		listOfFriends = cursor.fetchall()
		print "sadfjdsaflkjdsfakljaslkfsjdlkdsfjlkdafsjklasdf"
		print listOfFriends
		friendsIds = [item[0] for item in listOfFriends]
		print friendsIds
		print "dsfajadsfkljdsalkjsdalk"
		for x in friendsIds:
			print x
			cursor.execute("Select DISTINCT email FROM Users WHERE user_id = '{0}'".format(x))
			friendss.append(cursor.fetchone())
		newListFr = [str(item[0]) for item in friendss]
		newListFr = set(newListFr)
		return render_template('makeFriends.html', message = "Friends Added", friends = newListFr)
	else:
		return render_template('makeFriends.html', userList = userList)

@app.route('/showAllPhotos', methods = ['GET', 'POST'])
def showAllPhotos():
	cursor = conn.cursor()
	cursor.execute("SELECT imgdata, caption, picture_id FROM Pictures")
	g = cursor.fetchall()
	cursor.execute("SELECT picture_id, texts, dateRN FROM Comment")
	h = cursor.fetchall()
	cursor.execute("SELECT picture_id, tag FROM Tags")
	p = cursor.fetchall()
	return render_template('showAllPhotos.html', photoExist = g, comments = h, tags = p)

@app.route('/addTag', methods=['GET', 'POST'])
@flask_login.login_required
def add_tag():
	cursor = conn.cursor()
	cursor.execute("SELECT imgdata, picture_id FROM Pictures")
	pictures = cursor.fetchall()
	if request.method == 'POST':
		p = request.values.get('addTag')
		print p
		picture_id = int(p)
		print picture_id
		word = request.form.get('tag')
		print word
		cursor.execute("INSERT INTO Tags (tag, picture_id) VALUES ('{0}', '{1}')".format(word, picture_id))
		conn.commit()
		cursor = conn.cursor()
		cursor.execute("SELECT imgdata, caption, picture_id FROM Pictures")
		g = cursor.fetchall()
		cursor.execute("SELECT picture_id, texts, dateRN FROM Comment")
		h = cursor.fetchall()
		cursor.execute("SELECT picture_id, tag FROM Tags")
		p = cursor.fetchall()
		return render_template('showAllPhotos.html', photoExist = g, comments = h, tags = p)
	else:
		return render_template('addTag.html', photoExist = pictures)

@app.route('/removeTags', methods = ['GET', 'POST'])
@flask_login.login_required
def removeTag():
	cursor = conn.cursor()
	cursor.execute("SELECT imgdata, picture_id FROM Pictures")
	pictures = cursor.fetchall()
	if request.method == 'POST':
		p = request.form.get('addTag')
		print p
		picture_id = int(p)
		print picture_id
		word = request.form.get('tag')
		print word
		cursor.execute("DELETE FROM Tags WHERE tag = '{0}'".format(word))
		conn.commit()
		cursor = conn.cursor()
		cursor.execute("SELECT imgdata, caption, picture_id FROM Pictures")
		g = cursor.fetchall()
		cursor.execute("SELECT picture_id, texts, dateRN FROM Comment")
		h = cursor.fetchall()
		cursor.execute("SELECT picture_id, tag FROM Tags")
		p = cursor.fetchall()
		return render_template('showAllPhotos.html', photoExist = g, comments = h, tags = p)
	else:
		return render_template('removeTags.html', photoExist = pictures)

def is_empty(any_structure):
    if any_structure:
        print('Structure is not empty.')
        return False
    else:
        print('Structure is empty.')
        return True

def UsersTags(word, uid):
	cursor = conn.cursor()
	cursor.execute("SELECT picture_id FROM Tags WHERE word = '{0}'".format(word))
	P = cursor.fetchall()
	pids = [(int(item[0])) for item in P]
	photos = []
	for id in pids:
		cursor.execute("SELECT imgdata FROM Pictures WHERE user_id = '{0}' AND picture_id = '{1}'".format(uid, id));
		C = cursor.fetchone()
		if C is not None:
			photos.append(C)
	return photos

@app.route('/seeTagU', methods = ['GET', 'POST'])
@flask_login.login_required
def seeTagU():
	# empty = []
	# cursor = conn.cursor()
	# uid = getUserIdFromEmail(flask_login.current_user.id)
	# cursor.execute("SELECT picture_id FROM Pictures WHERE user_id = '{0}'".format(uid))
	# h = cursor.fetchall()
	# print "jadfslkdafsjlkdsafj;lsfadjasdflk;jadsfl;kjafsdl;kjasdlkjksadl;jasdlf;jkkl;asdfj;ldksafjlkfjdsldsjfk;l"
	# if is_empty(h):
	# 	print "FIREFIREFIREFIRE"
	# 	return render_template("noTags.html")
	# else:
	# 	h = [item[0] for item in h]
	# 	print h[0]
	# 	h = h[0]
	# 	print h
	# 	h = int(h)
	# 	print "sdfajldsafjdsaklfjdlsfkajsadlkjslkjsalkjldasfkjdsafjafdslakdslkladsf;j;dsaflkjdsaflkjfdsa;ljdsfa;lklkjfsdal;kjdsfalk;jdfsakl;jdsfakl;jaflj;fsdaljsdaflkjldsfkajlkdsfja"
	# 	cursor.execute("SELECT tag FROM Tags WHERE picture_id = '{0}'".format(h))
	# 	print "ssfjklsjdflkjslkjfdlkjsdlkflkjsadflkd"
	# 	print cursor.fetchall()
	# 	empty.append(cursor.fetchone()[0])
	# 	print "HJHJHJHJHJH"
	# 	print empty
	# 	if request.method == 'POST':
	# 		emptypics = []
	# 		tag = request.form.get('tag')
	# 		cursor.execute("SELECT picture_id FROM Tags WHERE tag = '{0}'".format(tag))
	# 		l = cursor.fetchall()
	# 		for sc in l:
	# 			cursor.execute("SELECT imgdata FROM Pictures WHERE picture_id = '{0}'".format(sc))
	# 		p = cursor.fetchall()
	# 		return render_template('seeTagU.html', picture = p)
	# 	else:
	# 		return render_template('seeTagU.html', tags = empty)
	cursor = conn.cursor()
	cursor.execute("SELECT tag FROM Tags")
	tagAll = cursor.fetchall()
	test = [(str(item[0])) for item in tagAll]
	if request.method == 'POST':
		tagPhoto = request.form.get('tag')
		print tagPhoto
		allTagss = allTags(tagPhoto)
		print allTagss
		return render_template('tagPhotos.html', pictures = allTagss)
	else:
		return render_template('tagSelectP.html', tags = test)

@app.route('/likePhoto', methods = ['GET', 'POST'])
def likePhotos():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	cursor = conn.cursor()
	cursor.execute("SELECT imgdata, picture_id FROM Pictures")
	pictures = cursor.fetchall()
	like = request.form.get('likePhoto')
	if request.method == 'POST':
		print "adsfjlfkdsalskdfjdfslkjasdl;kjfsdlk;sadfjlk;adsfjkl;afdsjafdls;"
		# like = request.form.get('likePhoto')
		print like
		cursor.execute("INSERT INTO Likes(picture_id, user_id) VALUES ('{0}', '{1}')".format(like, uid))
		conn.commit()
		return render_template('hello.html')
	else:
		return render_template('likePhoto.html', pictures = pictures)

def getLike(pids):
	cursor = conn.cursor()
	listLike = []
	listUser = []
	for id in pids:
		cursor.execute("SELECT COUNT(*) FROM Likes WHERE picture_id = '{0}'".format(id))
		numberLikes = cursor.fetchone()
		numberLikes = int(numberLikes[0])
		listLike.append(numberLikes)
		cursor.execute("SELECT user_id FROM Likes WHERE picture_id = '{0}'".format(id))
		userLike = cursor.fetchall()
		userLike = [str(getUserNameID(int(item[0]))) for item in userLike]
		listUser.append(userLike)
	print(listUser)
	return listLike, listUser

def getUserNameID(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT firstName FROM Users WHERE user_id = '{0}'".format(uid))
	return cursor.fetchone()[0]

@app.route('/listLikes', methods = ['GET', 'POST'])
def listLikey():
	cursor = conn.cursor()
	uid = getUserIdFromEmail(flask_login.current_user.id)
	cursor.execute("SELECT imgdata, picture_id FROM Pictures")
	pictures = cursor.fetchall()
	cursor.execute("SELECT picture_id, user_id FROM Likes")
	likes = cursor.fetchall()
	likess = [int(item[1]) for item in likes]
	print likess
	h = getLike(likess)
	print "jsdflkjsdlksdlkjsdflk"
	print h
	return render_template('listLikes.html', pictures = pictures, likes = likes, likeness = h)

@app.route('/deletePicture', methods = ['GET', 'POST'])
@flask_login.login_required
def deletePicture():
	cursor = conn.cursor()
	uid = getUserIdFromEmail(flask_login.current_user.id)
	cursor.execute("SELECT imgdata, picture_id FROM Pictures WHERE user_id = '{0}'".format(uid))
	print "sdajdflksajadfslkjadsflk;lksadj;ldksajadl;sk"
	L = cursor.fetchall()
	print "adsfkjfdklsajadslkjl32jlk1jlkjlkjdsflkjdsflkjdfslk"
	pictureDelete = request.form.get('pictureID')
	if request.method == 'POST':
		print pictureDelete
		cursor.execute("DELETE FROM Pictures WHERE picture_id = '{0}'".format(pictureDelete))
		conn.commit()
		return render_template('showAllPhotos.html')
	else:
		return render_template('deletePicture.html', pictures = L)

def allTags(tag):
	cursor = conn.cursor()
	cursor.execute("SELECT picture_id FROM Tags WHERE tag = '{0}'".format(tag))
	pidTaggs = cursor.fetchall()
	pids = [(int(item[0])) for item in pidTaggs]
	print "jsdfalkasdfjlksfadjlksfajlks"
	print pids
	photos = []
	for id in pids:
		cursor.execute("SELECT imgdata FROM Pictures WHERE picture_id = '{0}'".format(id));
		H = cursor.fetchall()
		K = [item[0] for item in H]
		photos.append(K)
	return photos

@app.route('/tagSelectP', methods = ['GET', 'POST'])
def tagPhoto():
	cursor = conn.cursor()
	cursor.execute("SELECT tag FROM Tags")
	tagAll = cursor.fetchall()
	test = [(str(item[0])) for item in tagAll]
	if request.method == 'POST':
		tagPhoto = request.form.get('tag')
		print tagPhoto
		allTagss = allTags(tagPhoto)
		print allTagss
		return render_template('tagPhotos.html', pictures = allTagss)
	else:
		return render_template('tagSelectP.html', tags = test)


@app.route('/rest', methods = ['GET', 'POST'])
def rest():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	cursor = conn.cursor()
	cursor.execute("SELECT aid, nameAlbum FROM Album")
	returnAlbum = cursor.fetchall()
	cursor.execute("SELECT imgdata FROM Pictures")
	returnPictures = cursor.fetchall()
	pictures = [[item[0]] for item in returnPictures]
	return render_template('rest.html', nameFirst = getfName(uid), nameLast = getlName(uid),profilePhoto= getUserProfile(uid), pictures = pictures)




if __name__ == "__main__":
	#this is invoked when in the shell  you run
	#$ python app.py
	app.run(port=5000, debug=True)
