default : Login.c
	gcc -o Login.cgi Login.c
	chmod 755 Login.cgi

chmod :
	chmod 700 *
	chmod 600 *.csv
	chmod 500 setURLusername # v. important
	chmod 755 *.sh *.cgi *.html
	chmod -R 755 pictures
