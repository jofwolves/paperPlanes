#! /bin/python

import os
import cgi

"""
print "Content-Type:text/html\n\n"
print "<html>\n"
print "<title> Home </title>\n"
print "Logged in. <br />\n"
print "</html>\n"
"""

def get_name ():
	with open('members.csv','r') as users_file:
		for line in users_file:
			user_data = line.split()
			num_data = len(user_data)
			if (num_data < 3):
				break
			if (user_data[1] != uname):
				continue
			return user_data[0]

def add_topic (topic):
	with open('topic.csv','a') as topics_file:
		topic = "%s\n%s\n" % (uname,topic)
		topics_file.write(topic)

def get_friends ():
	friends = []
	with open('members.csv','r') as users_file:
		for line in users_file:
			user_data = line.split()
			num_data = len(user_data)
			if (num_data < 3):
				break
			if (user_data[1] != uname):
				continue
			friends = user_data[3:]
			break
	return friends

def add_friend (friend):
	lines = []
	with open('members.csv','r+') as users_file:
		for line in users_file:
			user_data = line.split()
			if (len(user_data) < 3):
				break
			if (user_data[1] != uname):
				lines.append(line);
				continue
			line = line.rstrip('\n')
			line += friend 
			line += ' \n'
			lines.append(line);
			break
	with open('members.csv','w') as users_file:
		for line in lines:
			users_file.write(line)

form = cgi.FieldStorage()

uname = form.getfirst('uname')
action = form.getfirst('action')

if (action == "add_topic"):
	topic = form.getfirst('topic')
	add_topic(topic)
elif (action == "add_friend"):
	friend_name = form.getfirst('friend_name')
	add_friend(friend_name)

name = get_name()

def print_topics ():
	print "topics here"
	return

def print_members ():
	print "member list here"
	return

print "Content-Type:text/html\n\n"
print "<html>\n"
print "<title> Home </title>\n"
print "<center>\n"
print "	<head>\n"
print "		<b> PaperPlanes </b> <br />\n"
print "		Come fly with us, %s! <br />\n" % name
print "	</head>\n"
print "	<body>\n"
print "		<a href=\"http://cs.mcgill.ca/~jwolf/welcome.html\">\n"
print "			Logout\n"
print "		</a> <br />\n"
print "		<form action=\"./mainPage.sh\" method=\"post\">\n"
print "			<input type=\"hidden\" name=\"action\" value=\"add_topic\">\n"
print "			<input type=\"hidden\" name=\"uname\" value=\"%s\">\n" % uname
print "			Write a topic: <input type=\"text\" name=\"topic\"> <br />\n"
print "			<input type=\"submit\" value=\"Post it.\"> <br />"
print "		</form>\n"
print_topics()
print_members()
print "		<form action=\"./mainPage.sh\" method=\"post\">\n"
print "			<input type=\"hidden\" name=\"action\" value=\"add_friend\">\n"
print "			<input type=\"hidden\" name=\"uname\" value=\"%s\">\n" % uname
print "			Add someone to your list of friends (by username): <br />\n"
print "				<input type=\"text\" name=\"friend_name\"> <br />\n"
print "			<input type=\"submit\" value=\"Add friend!\"> <br />"
print "		</form>\n"
print "	</body>\n"
print "</center>\n"
print "</html>\n"

