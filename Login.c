#include <stdio.h>
#include <stdlib.h>

#define NULL_TERM '\0'

int login (char *uname);
int bad_pass (char *uname);
int bad_uname (char *uname);

int users_looped = 0; //D-TODO remove line

int main (void){
	int length = atoi(getenv("CONTENT_LENGTH"));
	char input[60];
	char c;
	int i = 0, j;
	while ((c = getchar()) != EOF && i < 60) {
		input[i] = c;
		i++;
	}
	input[i] = NULL_TERM;

	char uname[11];
	char pass[21];
	i = 1;
	while (input[i-1] != '=') i++;
	for (j = 0; input[i] != '&'; i++, j++) {
		uname[j] = input[i];
	}
	uname[j] = NULL_TERM;
	while (input[i-1] != '=') i++;
	for (j = 0; input[i] != NULL_TERM; i++, j++) {
		pass[j] = input[i];
	}
	pass[j] = NULL_TERM;

	FILE *members = fopen("members.csv","rt");
	int is_last_entry = 0;
	while ((c = fgetc(members)) != EOF && !is_last_entry) {
		users_looped++;
		while (fgetc(members) != ' ');
		char uname_existing[11];
		int i = 0;
		while ((c = fgetc(members)) != ' ' && i < 10) {
			uname_existing[i] = c;
			i++;
		}
		uname_existing[i] = NULL_TERM;
		if (!strcmp(uname,uname_existing)) {
			char pass_existing[21];
			int i = 0;
			while ((c = fgetc(members)) != ' ' && i < 20) {
				pass_existing[i] = c;
				i++;
			}
			pass_existing[i] = NULL_TERM;
			if (!strcmp(pass,pass_existing)) login(uname);
			else bad_pass(uname);
			return 0;
		}
		while (c = fgetc(members)) {
			if (c == EOF) {
				is_last_entry = 1;
				break;
			}
			if (c == '\n' || c == '\r') break;
		}
	}
	fclose(members);
	bad_uname(uname);
	return 0;
}

const char* site_name = "http://cs.mcgill.ca/~jwolf";

int html_head(void) {
	printf("Content-Type:text/html\n\n");
	printf("<html>\n");
	return 0;
}

int html_body_start(void) {
	printf("<center>\n");
	printf("<head>\n");
	printf("<b> PaperPlanes </b> <br />\n");
	printf("Come fly with us. <br />\n");
	printf("</head>\n");
	printf("<body>\n");
	return 0;
}

int html_tail(void) {
	printf("</body>\n");
	printf("</center>\n");
	printf("</html>\n");
	return 0;
}

int fail_page(char *message) {
	html_head();
	printf("<title> Login </title>\n");
	html_body_start();
	printf("<color=\"red\"> %s </color> <br />\n",message);
	printf("<a href=\"%s/welcome.html\"> Try again? </a> <br />\n",site_name);
	printf("<a href=\"%s/register.html\"> Create an account? </a> <br />\n",site_name);
	printf("Number of users looped through: %d <br />\n",users_looped); //D-TODO remove line
	html_tail();
	return 0;
}

int login(char *uname) {
	html_head();
	printf("<title> Welcome </title>\n");
	html_body_start();	
	printf("Success! <br />\n");
	printf("<form action=\"./mainPage.sh\" method=\"post\">\n");
	printf("<input type=\"hidden\" name=\"action\" value=\"login\">\n");
	printf("<input type=\"hidden\" name=\"uname\" value=\"%s\">\n",uname);
	printf("<input type=\"submit\" value=\"Continue to the site.\">\n");
	printf("</form>\n");
	html_tail();
	return 0;
}

int bad_pass(char *uname) {
	char *message = "Incorrect password.";
	fail_page(message);		
	return 0;
}

int bad_uname(char *uname) {
	char *message = "Username not found.";
	fail_page(message);
	return 0;
}

