from flask import Flask, render_template, request #flask is a module F is a class, from Module import Class
from pymongo import MongoClient
import ssl
import requests
from bs4 import BeautifulSoup

app= Flask(__name__, template_folder="templates")

client = MongoClient('mongodb+srv://kamathVenkat:7N1eXZCat17dK9fE@cluster0.qd9tw.mongodb.net/kamathsBlog?retryWrites=true&w=majority&ssl=true', ssl_cert_reqs=ssl.CERT_NONE)
db = client.get_database('kamathsBlog')
collection = db.Blogs
def imgSize(url, data):
	if url:
		if url[0] == '/':
			url = data + url
		if url[0:4] == 'data':
			return '', 0
		if url[0:4] != 'http':
			url = 'https://'+url
		return url, len(requests.get(url).content)
	return '', 0

def readTime(soup):
	ps = soup.findAll('p')
	text = ' '.join([p.text for p in ps])
	return str(round((len(text.split(' ')) * 300)/60000))

@app.route('/')
def index():
	list_docs = []
	for document in collection.find({}, {'_id': 0}):
		list_docs.append(document)
	list_docs.reverse()
	return render_template('index.html', blogs = list_docs, len_blogs = len(list_docs))

@app.route('/addBlog', methods=['POST'])
def login_request():
	username = request.form['userName'];
	password = request.form['password'];
	if username == 'Venkat' and password == 'e0b0ef49a5d6a47abaa2c628718ed00b':
		return render_template('addBlog.html')
	else:
		return render_template('login.html')

@app.route('/addBlog')
def login():
	return render_template('login.html')

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
	img = [img_tags[0], 0]
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
		if time[0]['datetime'].strip() != '':
			date = time[0]['datetime'].split('-')
			blog['date'] = month[int(date[1])-1] + ' ' + date[0]

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
	blog['url'] = request.form['url']
	blog['head'] = request.form['head']
	blog['image'] = request.form['image']
	blog['date'] = request.form['date']
	blog['para'] = request.form['para']
	blog['author'] = request.form['author']
	blog['time'] = request.form['time']
	status = collection.insert_one(blog)
	if status: 
		return render_template('addBlog.html')
	return "failure"

@app.route('/getBlog')
def getBlog():
	list_docs = []
	for document in collection.find({}, {'_id': 0}):
		list_docs.append(document)
	return {'blogs': list_docs}

if __name__ == '__main__':
	app.run()

