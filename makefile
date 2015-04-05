
default : Login.o
	gcc -o Login.cgi Login.o
	chmod a+rx Login.cgi
Login.o : Login.c
	gcc -c Login.c
clean : 
	rm -f Login.o
chmod :
	chmod a+rx -R *
