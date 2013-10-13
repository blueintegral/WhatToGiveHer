#!/usr/bin/env python
import urllib2
import urllib
from bs4 import BeautifulSoup, SoupStrainer
import json
import unicodedata
import re
import collections
#from collections import Counteri
import os
import sys
from itertools import tee, izip
from flask import Flask, render_template, request
app = Flask(__name__)

reload(sys)
sys.setdefaultencoding("utf-8") #Because apparently Pinterest is in UTF-8?

''' To Do:
	-Actually fix this script so it works again. Stupid Pinterest, ruining my scripts by 
	changing the architecture of their website...
	-Grab the image from the pin as well as the link for whitelisted sites
	-Mock up and begin writing frontend
	-change pinterest scraping to happen on the client side by calling a YQL query
	from javascript.
	-either send the result back to the server or parse it in javascript on the client
	side. Scaling will actually work that way and I'll just have to worry 
	about caching the javascript really well.
'''

#Routing functions
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/get')
def get():
	#return request.args['user']
	if 'user' in request.args:
		username = request.args['user']
		links = main(username)
		return str(links)
		#return "done"



def pairwise(iterable):
	"s -> (s0,s1), (s1,s2), (s2, s3), ..."
	a, b = tee(iterable)
	next(b, None)
	return izip(a, b)

def get_name(username):
	opener = urllib2.build_opener(urllib2.HTTPHandler)
	req = urllib2.Request("http://pinterest.com/"+username)
	req.add_header('User-agent','Mozilla/5.0')
	try:
		result = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print "HTTP Error"
	except urllib2.URLError, e:
		print "HTTP Error"
	response = result.read()
	soup = BeautifulSoup(response)
	n = soup.title.string.find("(")
	#n = soup.title.string.find(" ",soup.title.string.find(" ")+1)
	return soup.title.string[0:n]

def scrape_pins(username):
	#Get each page and store it so we can find pins later
	opener = urllib2.build_opener(urllib2.HTTPHandler)
	page = 1
	soup = []
	output = []
	done = False
	#print "Scraping pins..."
	while not done:
		#print "http://pinterest.com/"+username+"/pins/?lazy=1&page="+str(page)
		req = urllib2.Request("http://pinterest.com/"+username+"/pins/?lazy=1&page="+str(page))
		req.add_header('User-agent','Mozilla/5.0')
		try:
			result = urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			#print e.code
			done = True
		except urllib2.URLError, e:
			print e.args
			done = True
		response = result.read()
		#See if this is the last page with Beautiful Soup
		response = response.decode('ascii','ignore')
		soup = BeautifulSoup(response)
		if soup.find(text=re.compile("The page you\'re looking for could not be found.")):
			done = True
			print "Got a 404 on pins, ending scrape."
		elif soup.find(text=re.compile("pinned anything yet")):
			done = True
			print "All pins scraped."
			
		else:
			#It's a valid page, save it
			#soup = soup + tempsoup	
			#f = open("soup.txt", "a")
			#unicodedata.normalize('NFKD', soup).encode('ascii','ignore')
			output.append(soup)
			#f.write(soup.prettify())
			#f.close()
			page = page + 1
			print "On page "+str(page)
	return output


def scrape_activity(username):
	print "Scraping activity..."
	page = 1
	soup =
	[]
	#output = []
	req = urllib2.Request("http://pinterest.com/"+username+"/activity/")
	req.add_header('User-agent','Mozilla/5.0')
	result = urllib2.urlopen(req)
	response = result.read()
	#This page doesn't have infinite scroll, so we can get it in one shot
	response = response.decode('ascii','ignore')
	soup = BeautifulSoup(response)
	if soup.find(text=re.compile("The page you\'re looking for could not be found.")):
		print "Got a 404 on activity."
	elif soup.find(text=re.compile("pinned anything yet")):
		print "No activity found."
	else:
		#It's a valid page, save it
		output = soup.prettify()
		#activity = soup.prettify()
		print "Got all activity."
	#Loop through the activity scrape and construct an array of ranked people similar to the original person
	
	friends = []
	lines = output.split('\n')
	for x, next in zip(lines, lines[1:]): #x
		m = re.search("via", x)
		if m:
			soup = BeautifulSoup(next)
			for a in soup.findAll('a',href=True):
				links = a['href']
				links = links[1:-1]
				friends.append(links)

	count = collections.Counter(friends)
	topfriends = count.most_common(3) #Get top 3 friends
	print "Her most similar friends appear to be: "
	print topfriends
	return topfriends

def get_links(links):
	#Ok, now let's run analysis on the original person
	#print links
	pinlinks = []
	#links is a list of beautiful soup's.
	for page in links:
		for line in page.findAll('a', href=True):
			string = line['href']
			if string and (string[0] == "h"):
				#print string
				for site in sitelist:
					if site in string:
						#print string
						pinlinks.append(string)
	#print pinlinks
	return pinlinks	
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################



#print "*************************************************************************************"
#print "WhatShouldIGetHer: Figure out what to get your girlfriend by cheating with Pinterest."
#print "*************************************************************************************"

#user = raw_input("What's the Pinterest username of your girlfriend? ")
#List of sites we know we can buy things from
sitelist = [
		"amazon.com",
		"etsy.com",
		"tobi.com",
		"polyvore.com",
		"wanelo.com",
		"boohoo.com",
		"ricketyrack.com",
		"crazydogtshirts.com",
		"revolveclothing.com",
		"net-a-porter.com",
		"ustrendy.com",
		"esther.com.au",
		"anthropologie.com",
		"pacsun.com",
		"nastygal.com",
		"modcloth.com",
		"joie.com",
		"rstyle.me",
		"thefancy.come",
		"thinkgeek.com",
		"zulily.com",
		"emersonfry.com",
		"lululemon.com",
		"shopbop.com",
		"asos.com",
		"dressinmoda.com"
	  ]

def main(user): 
	print get_name(user)
	root_pins = scrape_pins(user)
	if root_pins:
		topfriends = scrape_activity(user)
		if (topfriends):
			print "Scraping pins from top friends..."
			print "Scraping "+topfriends[0][0]+"..."
			friend1_pins = scrape_pins(topfriends[0][0])
			print "Scraping "+topfriends[1][0]+"..."
			friend2_pins = scrape_pins(topfriends[1][0])
			print "Scraping "+topfriends[2][0]+"..."
			friend3_pins = scrape_pins(topfriends[2][0])
			print "Analyzing "+user+"..."
			root_links = get_links(root_pins)
			print "Analyzing "+topfriends[0][0]+"..."
			friend1_links = get_links(friend1_pins)
			print "Analyzing "+topfriends[2][0]+"..."
			friend2_links = get_links(friend2_pins)
			print "Analyzing "+topfriends[2][0]+"..."
			friend3_links = get_links(friend3_pins)
			#print friend1_links
			#raw_input()
			#print friend2_links
			#raw_input()
			#print friend3_links
	return friend1_links+friend2_links+friend3_links

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 12000))
	app.debug = os.environ.get('DEBUG', True)
	app.logger.info("Debug is set to: %s" % app.debug)
	app.run(host='0.0.0.0', port=port)

