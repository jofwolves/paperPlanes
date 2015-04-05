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
already_friend = False
no_such_user = False
myself = False
if (action == "add_topic"):
	topic = form.getfirst('topic')
	add_topic(topic)
elif (action == "add_friend"):
	friend_name = form.getfirst('friend_name')
        if (get_name(friend_name) == "unregistered user"):
		no_such_user = True
	elif (friend_name == uname):
		myself = Truei
	elif (already_friend in get_friends()):
		already_friend = True
	else:
		no_such_user = False
		myself = False
		already_friend = False
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
	print "<br /><h4>What your fellow paper airplane enthusiasts are up to:</h4><br />"
	max_topic = len(topics_content)-1
	min_topic = max_topic-n_topics if (max_topic-n_topics > -1) else -1
	for i in range(max_topic,min_topic,-1): # print the topics in reverse order
		crt_uname = topics_authors[i]
		crt_name = get_name(crt_uname)
		crt_topic = topics_content[i]
		print "<em>%s (%s)</em> says: " % (crt_name,crt_uname)
		print "%s <br /> <br />" % crt_topic
	return

def print_friends():
	"""
	prints all friends of current user
	"""	
	my_friends = get_friends()
	print "<h4>My friends:</h4>\n"
	print "<em>Name (Username)</em><br /><br />\n"
	for friend in my_friends:
		print "%s (%s)<br />" % (get_name(friend),friend)
	print "<br /> <br />"
		
def print_members ():
	"""
	print name and username from each line of members.csv
	"""
	print "<h4>Who else is a paper airplane enthusiast?</h4>\n"
	print "<em>Name (Username)</em><br /><br />\n"
	with open('members.csv','r') as users_file:
		for line in users_file:
			user_data = line.split()
			if (len(user_data) < 3):
				break
			crt_name = user_data[0]
			crt_uname = user_data[1]
			print "%s (%s)<br />" % (crt_name,crt_uname)
	print "<br /> <br />"
	return

print "Content-Type:text/html\n\n"
print "<html>\n"
print "<head>\n"
print "<title> Home </title>\n"
print "</head>\n"
print "<body>\n"
print "<table height=100% width=100% cellspacing=\"5\" cellpadding=\"2\" border=\"1\" background=\"pictures/bg1.jpg\">\n"

#################TOP of page(header)############################
print "<td colspan=\"6\" align=\"center\">\n"
print "		<h1> PaperPlanes </h1>\n"
print "		<h4>Come fly with us, %s! </h4>\n" % name
print "		<marquee behavior=\"scroll\" direction=\"left\">\n"
print "		<img src=\"./pictures/pap1.png\" alt=\"Flying plane\" width=100>\n"
print "		</marquee>\n"

print "		<a href=\"http://cs.mcgill.ca/~rbelya/welcome.html\">" # EDIT THIS LINE
print "			Logout"
print "		</a>"
print "</td>\n"
###########################################################

####################LEFT COLUMN##############################
print "<tr>\n"
print "<td rowspan=\"4\" valign=\"top\">\n"
try:
	print_friends()
except Exception as e:
	print "	Something's not right. Topics will be back later. <br />"
	print "	Error: ",e," <br />"
print "		<form action=\"./mainPage.sh\" method=\"post\">"
print "			<input type=\"hidden\" name=\"action\" value=\"add_friend\">"
print "			<input type=\"hidden\" name=\"uname\" value=\"%s\">\n" % uname
print "			Add someone to your list of friends (by username): <br />"
print "				<input type=\"text\" name=\"friend_name\"> <br />"
print "			<input type=\"submit\" value=\"Add friend!\"> <br />"
print "		</form>"
if (no_such_user is True):
	print "<font color=\"red\">User %s does not exist</font>\n" %friend_name
elif (myself is True):
	print "<font color=\"red\">Cannot add yourself as a friend</font>\n"
elif (already_friend is True):
	print "<font color=\"red\">User %s is already your friend</font>\n" %friend_name
print "</td>\n"
print "</td>\n"
print "</td>\n"
#######################################3###############

###################CENTER COLUMN########################################
print "<td colspan=\"4\" rowspan=\"4\" align=\"center\" valign=\"top\">\n"
print "		<form action=\"./mainPage.sh\" method=\"post\">"
print "			<input type=\"hidden\" name=\"action\" value=\"add_topic\">"
print "			<input type=\"hidden\" name=\"uname\" value=\"%s\">\n" % uname
print "			Write a topic: <input type=\"text\" size=\"60\" name=\"topic\"> <br />"
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
print "</td>\n"
######################################################

########################RIGHT COLUMN####################
print "<td rowspan=\"4\" valign=\"top\">\n"
try:
	print_members()
except:
	print "	Something's not right. User list will be back later <br />"
print "</td>\n"
#################################################

print "</tr> <tr> </tr><tr> </tr><tr></tr>\n"


print "</table>\n"
print "</body>\n"
print "</html>"

