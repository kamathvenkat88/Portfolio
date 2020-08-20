from flask import Flask, render_template, request, redirect, url_for #flask is a module F is a class, from Module import Class
from pymongo import MongoClient #Pyongo, Module to connect to DB (MongoClient)
import ssl #imports empty certificate for MongoDb connection.
import requests #to get response for scraping
from bs4 import BeautifulSoup #Html parser for scraping
import random

app= Flask(__name__, template_folder="templates") #creates a Flask application which sets the template folder to templates

client = MongoClient('mongodb+srv://kamathVenkat:7N1eXZCat17dK9fE@cluster0.qd9tw.mongodb.net/kamathsBlog?retryWrites=true&w=majority&ssl=true', ssl_cert_reqs=ssl.CERT_NONE)
#connecting client to the MongoDB Cluster
db = client.get_database('kamathsBlog') #accessing database from cluster
 #accessing collection blogs from the Database

def getTravelBlogs():
	collection=db.travelBlog
	list_blogs = []
	for document in collection.find({},{"place":1, "year":1}):
		list_blogs.append(document['place']+'-'+document['year'])
	return list_blogs

def imgSize(url, data): #A function defined to get image size
	if url: #if URL is not none
		if url[0] == '/': #Check if the URL is relative to the current website
			url = data + url #If relative prepend current website
		if url[0:4] == 'data': #check if URL is the data URL 
			return '', 0 #hard to parse so. therefore return 0
		if url[0:4] != 'http': #check if the first 4 letter are Http
			url = 'https://'+url #prepent https:// if first three letters are not HTP
		return url, len(requests.get(url).content) #return URL and size  of image
	return '', 0 #return 0 if URL is none

def random_image(collection, index):
	cursor = collection.find({'key': index})
	count = cursor.count()
	skip_num = 0
	if count > 1:
		skip_num = random.randrange(count-1)
	
	for image in cursor.skip(skip_num).limit(1):
		return image['image']


def readTime(soup): #time required to read the article: Soup is parsed HTML data
	ps = soup.findAll('p') #searching for all P tags
	text = ' '.join([p.text for p in ps]) #collecting all the texts from P tags
	return str(round((len(text.split(' ')) * 300)/60000)) #reading words and appropriate tie to eachword

@app.route('/') #creating a route for the application which starts with "/"
def index(): #The function is run whenever the above route is encountered
	list_blogs = [] #creating an empty array
	collection = db.Blogs
	for document in collection.find({}, {'_id': 0}):#collection.find accesses document from database
		list_blogs.append(document) 
	list_blogs.reverse() #re-orders the blogs
	titles = getTravelBlogs()
	images = []
	collection = db.travelImages
	for title in titles:
		images.append(random_image(collection, title))
	return render_template('index.html', blogs = list_blogs, len_blogs = len(list_blogs), images = images, titles = titles, len_images = len(images)) #renders template index.html with the blogs

@app.route('/addBlog', methods=['POST']) #addBlog route on post request
def login_request():
	username = request.form['userName'];
	password = request.form['password'];
	if username == 'Venkat' and password == 'e0b0ef49a5d6a47abaa2c628718ed00b':
		travelBlogs = getTravelBlogs()
		return render_template('addBlog.html', travelBlogs = travelBlogs, len_travelBlogs = len(travelBlogs))
	else:
		return render_template('login.html')

@app.route('/addBlog') #addBlog route on get request 
def login():
	return render_template('login.html') #render the template login.html

@app.route('/scrapeBlog', methods=['POST'])
def scrapBlog():
	url = request.form['blogLink']
	blog = {'head':'', 'author':'', 'image':'', 'date':'', 'para':'', 'time':'', 'url':''}
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")

	#title
	title = soup.findAll("meta", {'property': 'og:title'})
	if title:
		if title[0]['content'].strip() != '':
			blog['head'] = title[0]['content']

	title = soup.findAll("title")
	if title:
		if title[0].text.strip() != '':
			blog['head'] = title[0].text.strip()

	title = soup.findAll("h1")
	if title:
		if title[0].text.strip() != '':
			blog['head'] = title[0].text.strip()

	#author
	author = soup.findAll("meta", {'name': "author"})
	if author:
		if author[0]['content'].strip() != '':
			blog['author'] = author[0]['content'].strip()

	#image
	img_tags = soup.findAll("img")
	img = ['', 0]
	for img_tag in img_tags:
		img_url, size = imgSize(img_tag.get('src'), url)
		if size > img[1]:
			img[1] = size
			img[0] = img_url
	blog['image'] = img[0]

	#time
	time = soup.findAll('time')
	month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	if time:
		print(time)
		if time[0].text.strip() != '':
			blog['date'] = time[0].text #month[int(date[1])-1] + ' ' + date[0]

	time = soup.findAll("meta", {'property': 'article:published_time'})
	if time:
		if time[0]['content'].strip() != '':
			date = time[0]['content'].split('-')
			blog['date'] = month[int(date[1])-1] + ' ' + date[0]



	#paragraph
	p_tags = soup.findAll("p")
	for p_tag in p_tags:
		if p_tag and len(p_tag.text.split(' ')) > 20:
			blog['para'] = ' '.join(p_tag.text.split(' ')[0:20]) + '...'
			break

	#read-time
	blog['time'] = readTime(soup)
	#url
	blog['url'] = url
	return render_template("scrapeBlog.html", blog=blog)

@app.route('/postBlog', methods=['POST'])
def postBlog():
	blog = {}
	collection = db.Blogs
	blog['url'] = request.form['url']
	blog['head'] = request.form['head']
	blog['image'] = request.form['image']
	blog['date'] = request.form['date']
	blog['para'] = request.form['para']
	blog['author'] = request.form['author']
	blog['time'] = request.form['time']
	status = collection.insert_one(blog)
	if status: 
		return redirect('/addBlog')
	return "failure"

@app.route('/postTravelBlog', methods=['POST'])
def postTravelBlog():
	blog = {}
	collection = db.travelBlog
	blog['place'] = request.form['place']
	blog['year'] = request.form['year']
	blog['head'] = request.form['head']
	blog['blog'] = request.form['blog']
	blog['foot'] = request.form['foot']
	status = collection.insert_one(blog)
	if status: 
		return redirect('/addBlog')
	return "failure"

@app.route('/postTravelImage', methods=['POST'])
def postTravelImage():
	blog = {}
	collection = db.travelImages
	blog['key'] = request.form['key']
	blog['image'] = request.form['image']
	status = collection.insert_one(blog)
	if status: 
		travelBlogs = getTravelBlogs()
		return redirect('/addBlog')
	return "failure"

@app.route('/getBlog')
def getBlog():
	list_docs = []
	for document in collection.find({}, {'_id': 0}):
		list_docs.append(document)
	return {'blogs': list_docs}

if __name__ == '__main__':
	app.run()

