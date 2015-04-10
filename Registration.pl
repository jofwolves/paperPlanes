#! /bin/perl

use strict;
use warnings;
use CGI ':standard';

my $name = param('name');
my $uname = param('uname');
my $pass = param('pass');

#
# add your name to this list (space separated)
# in order to automatically be added to peoples
# friend lists, MySpace Tom-style
#
my $admin_names = "jwolf";

my $members_file = "members.csv";
open(my $fh,'<',$members_file);
my @existing_users = <$fh>;
close($fh);

my $user_exists = 0;
foreach (@existing_users) {
	my @user_data = split(/ /,$_);
	last if (scalar(@user_data) < 3); # end of list
	if ($user_data[1] eq $uname) {
		$user_exists = 1; # username exists : (
		last;
	}
}

#
# prints standard header to html file
#
sub html_head {
	print "<html>\n";
	print "<head>\n";
	print "<title>PaperPlanes</title>\n";
	print "</head>\n";
	print "<body>\n";
	print "<table height=100\% width=100\% cellspacing=\"0\" cellpadding=\"0\" border=\"0\" background=\"pictures/bg1.jpg\">\n";
	print "<tr><td align=center>\n";
	print "<h1> PaperPlanes </h1>\n";
	print "<h4>Come fly with us</h4>\n";
	print "<marquee behavior=\"scroll\" direction=\"left\">\n";
	print "<img src=\"./pictures/pap1.png\" alt=\"Flying plane\" width=100>\n";
	print "</marquee>\n";
}

sub html_tail{
	print "</td></tr>\n";
	print "</table>\n";
	print "</body>\n";
	print "</html>\n";
}

print "Content-Type:text/html\n\n";
if ($user_exists) { # let the user try again with a different username
	&html_head;
	print "		The username $uname is already taken; sorry about that. <br />\n";
	print "		<a href=\"http://cs.mcgill.ca/~rbelya/register.html\">\n";
	print "			Try a different one?\n";
	print "		</a>\n";
	print "	</body>\n";
	&html_tail;
}
else {
	&html_head;
	if ($name =~ /\W/ ||	# don't let anyone use a
		$uname =~ /\W/ ||	# name, username, or password
		$pass =~ /\W/) {	# that contains non-word characters
		print " 	Only alphanumeric characters and underscores are allowed. <br />\n";
		print "		<a href=\"http://cs.mcgill.ca/~rbelya/register.html\">\n";
		print "			Try again?\n";
		print "		</a>\n";
	}
	elsif ($name !~ /\w/ ||	# make sure each field contains
		$uname !~ /\w/ ||	# at least one character
		$pass !~ /\w/) { 	# (otherwise the .csv gets ugly)
		print " 	Each field must contain at least one character. <br />\n";
		print "		<a href=\"http://cs.mcgill.ca/~rbelya/register.html\">\n";
		print "			Try again?\n";
		print "		</a>\n";
	}
	else { # everything was a success! add them to the "database"
		open(my $fh,'>>',$members_file);
		print $fh "$name $uname $pass $admin_names \n";
		close($fh);
		print "		Congratulations! Your account has been created. <br />\n";
		print "		<a href=\"http://cs.mcgill.ca/~rbelya/welcome.html\">\n";
		print "			Login now and get started!\n";
		print "		</a>\n";
	}
	&html_tail;
}

