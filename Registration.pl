#! /bin/perl

use strict;
use warnings;
use CGI ':standard';

my $name = param('name');
my $uname = param('uname');
my $pass = param('pass');

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

print "Content-Type:text/html\n\n";
if ($user_exists) {
	print "<html>\n";
	print "<title> Become a Member </title>\n";
	print "<center>\n";
	print "	<head>\n";
	print "		<b> PaperPlanes </b> <br />\n";
	print "		Come fly with us. <br />\n";
	print "	</head>\n";
	print "	<body>\n";
	print "		The username $uname is already taken; sorry about that. <br />\n";
	print "		<a href=\"http://cs.mcgill.ca/~jwolf/register.html\">\n";
	print "			Try a different one?\n";
	print "		</a>\n";
	print "	</body>\n";
	print "</center>\n";
	print "</html>\n";
}
else {
	open(my $fh,'>>',$members_file);
	print $fh "$name $uname $pass \n";
	close($fh);
	
	print "<html>\n";
	print "<title> Become a Member </title>\n";
	print "<center>\n";
	print "	<head>\n";
	print "		<b> PaperPlanes </b> <br />\n";
	print "		Come fly with us. <br />\n";
	print "	</head>\n";
	print "	<body>\n";
	print "		Congratulations! Your account has been created. <br />\n";
	print "		<a href=\"http://cs.mcgill.ca/~jwolf/welcome.html\">\n";
	print "			Login now and get started!\n";
	print "		</a>\n";
	print "	</body>\n";
	print "</center>\n";
	print "</html>\n";
}

