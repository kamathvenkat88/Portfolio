import requests
from bs4 import BeautifulSoup
from PIL import Image
import urllib3

urls = ["https://towardsdatascience.com/how-to-learn-data-science-when-life-does-not-give-you-a-break-a26a6ea328fd", 
"https://www.theverge.com/21368867/transcription-google-docs-live-transcribe-how-to-zoom",
"https://www.freecodecamp.org/news/here-is-the-most-popular-ways-to-make-an-http-request-in-javascript-954ce8c95aaa/"]

def imgSize(url, data):
	if url:
		if url[0] == '/':
			url = data + url
		if url[0:4] != 'http':
			url = 'https://'+url
		return url, len(requests.get(url).content)
	return '', 0

blog = {}

#title
title = soup.findAll("meta", {'property': 'og:title'})
if title:
	if title[0].text.strip() != '':
		blog['head'] = title.text

title = soup.findAll("title")
if title:
	if title[0].text.strip() != '':
		blog['head'] = title.text

title = soup.findAll("h1")
if title:
	if title[0].text.strip() != '':
		blog['head'] = title.text

#author
author = soup.findAll("meta", {'name': "author"})
	if author:
		print(author[0]['content'])

author = soup.findAll("meta", {'name': "author"})[0]
if title:
	if title.text.strip() != '':
		blog['head'] = title.text
for url in urls:
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	
	h1_tag = soup.findAll("h1")[0]
	print(len(response.content))
	print(h1_tag.text)

	title = soup.findAll("meta",  {'property': 'og:title'})
	print(title)

	title = soup.findAll("title")
	print(title)

	time = soup.findAll("time")
	print(time)

	author = soup.findAll("meta", {'name': "author"})
	if author:
		print(author[0]['content'])
	

	img_tags = soup.findAll("img")
	img = [img_tags[0], 0]
	for img_tag in img_tags:
		img_url, size = imgSize(img_tag.get('src'), url)
		if size > img[1]:
			img[1] = size
			img[0] = img_url
	print(img)

	p_tags = soup.findAll("p")
	for p_tag in p_tags:
		if p_tag and len(p_tag.text.split(' ')) > 20:
			print(p_tag.text)
			break
	print()