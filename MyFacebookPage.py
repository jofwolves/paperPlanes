#! /bin/python

import os
import cgi

form = cgi.FieldStorage()

uname = form.getfirst('uname')
action = form.getfirst('action')

def get_name (username): # fully functional
	with open('members.csv','r') as users_file:
		for line in users_file:
			user_data = line.split()
			if (user_data[1] != username):
				continue
			if (len(user_data) < 3):
				continue
			return user_data[0]

def add_topic (topic): # fully functional
	with open('topic.csv','a') as topics_file:
		topic = "%s\n%s\n" % (uname,topic)
		topics_file.write(topic)
	return

def get_friends (): # seems functional
	friends = []
	with open('members.csv','r') as users_file:
		for line in users_file:
			user_data = line.split()
			if (user_data[1] != uname):
				continue
			if (len(user_data) < 3):
				continue
			friends = user_data[3:]
			break
	return friends

def add_friend (friend): # seems to work, finally!
	lines = []
	with open('members.csv','r+') as users_file:
		for line in users_file:
			user_data = line.split()
			if (len(user_data) < 3):
				continue
			if (user_data[1] != uname):
				lines.append(line);
				continue
			if (friend in user_data[3:]):
				return # no need to doubly add friend
			line = line.rstrip('\n')
			line += friend
			line += ' \n'
			lines.append(line);
	with open('members.csv','w') as users_file:
		for line in lines:
			users_file.write(line)
	return

if (action == "add_topic"):
	topic = form.getfirst('topic')
	add_topic(topic)
elif (action == "add_friend"):
	friend_name = form.getfirst('friend_name')
	add_friend(friend_name)

name = get_name(uname)

def print_topics (): # prints them backwards
	friends_list = get_friends()
	topics_content = []
	topics_authors = []
	with open('topic.csv','r') as topics_file:
		is_topic_line = 0 # username, or content?
		skip_entry = 0 # is user not on friends list?
		for line in topics_file:
			if (is_topic_line):
				is_topic_line = 0
				if (skip_entry):
					skip_entry = 0
					continue
				crt_topic = line.rstrip('\n')
				topics_content.append(crt_topic)
			else:
				is_topic_line = 1
				crt_uname = line.rstrip('\n')
				if (crt_uname not in friends_list):
					skip_entry = 1
					continue
				topics_authors.append(crt_uname)
	print "<br /> What your fellow paper airplane enthusiasts are up to: <br />"
	max_topic = len(topics_content)-1
	min_topic = max_topic-10 if (max_topic-10 > -1) else -1
	for i in range(max_topic,min_topic,-1):
		crt_uname = topics_authors[i]
		crt_name = get_name(crt_uname)
		crt_topic = topics_content[i]
		print "%s (%s) says: <br />" % (crt_name,crt_uname)
		print "%s <br /> <br />" % crt_topic
	return
	
def print_members ():
	print "<br /> Who else is a paper airplane enthusiast? <br />"
	with open('members.csv','r') as users_file:
		for line in users_file:
			user_data = line.split()
			if (len(user_data) < 3):
				break
			crt_name = user_data[0]
			crt_uname = user_data[1]
			print "%s (%s); &nbsp;" % (crt_name,crt_uname)
	print "<br /> <br />"
	return

print "Content-Type:text/html\n\n"
print "<html>"
print "<title> Home </title>"
print "<center>"
print "	<head>"
print "		<b> PaperPlanes </b> <br />"
print "		Come fly with us, %s! <br />" % name
print "	</head>"
print "	<body>"
print "		<a href=\"http://cs.mcgill.ca/~jwolf/welcome.html\">"
print "			Logout"
print "		</a> <br />"
print "		<form action=\"./mainPage.sh\" method=\"post\">"
print "			<input type=\"hidden\" name=\"action\" value=\"add_topic\">"
print "			<input type=\"hidden\" name=\"uname\" value=\"%s\">\n" % uname
print "			Write a topic: <input type=\"text\" name=\"topic\"> <br />"
print "			<input type=\"submit\" value=\"Post it.\"> <br />"
print "		</form>"
try:
	print_topics()
except Exception as e:
	print "	Something's not right. Topics will be back later. <br />"
	print "	Error: ",e," <br />"
try:
	print_members()
except:
	print "	Something's not right. User list will be back later <br />"
print "		<form action=\"./mainPage.sh\" method=\"post\">"
print "			<input type=\"hidden\" name=\"action\" value=\"add_friend\">"
print "			<input type=\"hidden\" name=\"uname\" value=\"%s\">\n" % uname
print "			Add someone to your list of friends (by username): <br />"
print "				<input type=\"text\" name=\"friend_name\"> <br />"
print "			<input type=\"submit\" value=\"Add friend!\"> <br />"
print "		</form>"
print "	</body>"
print "</center>"
print "</html>"

