#! /bin/python

import os
import cgi

form = cgi.FieldStorage()

uname = form.getfirst('uname')
action = form.getfirst('action')

def get_name (username):
	"""
	find the name associated with a given username
	"""
	with open('members.csv','r') as users_file:
		for line in users_file:
			user_data = line.split()
			if (len(user_data) < 3):	# shouldn't occur since
				continue				# Registration.pl checks
			if (user_data[1] != username):
				continue
			return user_data[0] # correct user has been reached
	return "unregistered user" # correct user was not found

def add_topic (topic):
	"""
	add a topic to the topics "database"
	(adds in the name of the active user)
	"""
	with open('topic.csv','a') as topics_file:
		topic = "%s\n%s\n" % (uname,topic)
		topics_file.write(topic)
	return

def get_friends ():
	"""
	get a list of friends of the active user
	(works pretty much the same way as get_name)
	"""
	friends = []
	with open('members.csv','r') as users_file:
		for line in users_file:
			user_data = line.split()
			if (len(user_data) < 3):
				continue
			if (user_data[1] != uname):
				continue
			friends = user_data[3:]
			break
	return friends

def add_friend (friend):
	"""
	add a friend to the active user's list
	needs to copy over all of members.csv, unfortunately
	"""
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
			line = line.rstrip('\n')	# there's probably a much
			line += friend				# cleaner way of doing this,
			line += ' \n'				# but i don't know what it is
			lines.append(line);
	with open('members.csv','w') as users_file:
		for line in lines:			# re-write all of members.csv
			users_file.write(line)	# with addition of new friend
	return

#
# respond to any forms sent by this page itself
#
if (action == "add_topic"):
	topic = form.getfirst('topic')
	add_topic(topic)
elif (action == "add_friend"):
	friend_name = form.getfirst('friend_name')
	add_friend(friend_name)

if (action == "more_topics"):
	n_topics = int(form.getfirst('n_topics')) + 10
else:
	n_topics = 10

#
# this is where things start to actually happen
#
name = get_name(uname)

def print_topics ():
	"""
	print most recent topics from topic.csv;
	defaults to 10 topics, but n_topics can
	be altered by the user using a form
	"""
	friends_list = get_friends()
	topics_content = []
	topics_authors = []
	with open('topic.csv','r') as topics_file:
		is_topic_line = 0 # username, or content?
		skip_entry = 0 # is user not on friends list?
		for line in topics_file:
			if (is_topic_line): # add to topics_content
				is_topic_line = 0 # next line won't be a topic line
				if (skip_entry):	# don't want to bother with
					skip_entry = 0	# entries from people who aren't
					continue		# on the user's list
				crt_topic = line.rstrip('\n')
				topics_content.append(crt_topic)
			else: # not a topic line: add to topics_authors
				is_topic_line = 1 # next line will be a topic line
				crt_uname = line.rstrip('\n')
				if (crt_uname not in friends_list):
					skip_entry = 1
					continue
				topics_authors.append(crt_uname)
	print "<br /> What your fellow paper airplane enthusiasts are up to: <br />"
	max_topic = len(topics_content)-1
	min_topic = max_topic-n_topics if (max_topic-n_topics > -1) else -1
	for i in range(max_topic,min_topic,-1): # print the topics in reverse order
		crt_uname = topics_authors[i]
		crt_name = get_name(crt_uname)
		crt_topic = topics_content[i]
		print "%s (%s) says: <br />" % (crt_name,crt_uname)
		print "%s <br /> <br />" % crt_topic
	return
	
def print_members ():
	"""
	print name and username from each line of members.csv
	"""
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
print "		<a href=\"http://cs.mcgill.ca/~rbelya/welcome.html\">" # EDIT THIS LINE
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
print "		<form action=\"./mainPage.sh\" method=\"post\">"
print "			<input type=\"hidden\" name=\"action\" value=\"more_topics\">"
print "			<input type=\"hidden\" name=\"uname\" value=\"%s\">\n" % uname
print "			<input type=\"hidden\" name=\"n_topics\" value=\"%d\">\n" % n_topics
print "			<input type=\"submit\" value=\"View more topics\"> <br />"
print "		</form>"
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

