#include <stdio.h>
#include <stdlib.h>

#define NULL_TERM '\0'

int login (char *uname);
int bad_pass (char *uname);
int bad_uname (char *uname);

int main (void){
	int length = atoi(getenv("CONTENT_LENGTH"));
	char input[60]; // input fields are limited to 10, 10, and 20
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
	while (input[i-1] != '=') i++; // get to first value
	for (j = 0; input[i] != '&'; i++, j++) {
		uname[j] = input[i]; // go until second var name
	}
	uname[j] = NULL_TERM;
	while (input[i-1] != '=') i++; // get to second value
	for (j = 0; input[i] != NULL_TERM; i++, j++) {
		pass[j] = input[i]; // go until third var name
	}
	pass[j] = NULL_TERM;

	FILE *members = fopen("members.csv","rt");
	int is_last_entry = 0; // default to continuing through entries
	while ((c = fgetc(members)) != EOF && !is_last_entry) {
		while (fgetc(members) != ' '); // move forward to username
		char uname_existing[11];
		int i = 0;
		while ((c = fgetc(members)) != ' ' && i < 10) {
			uname_existing[i] = c; // get username from this line
			i++;
		}
		uname_existing[i] = NULL_TERM;
		if (!strcmp(uname,uname_existing)) {
			char pass_existing[21];
			int i = 0;
			while ((c = fgetc(members)) != ' ' && i < 20) {
				pass_existing[i] = c; // get password from this line
				i++;
			}
			pass_existing[i] = NULL_TERM;
			if (!strcmp(pass,pass_existing)) login(uname);
			else bad_pass(uname); // have them try again
			return 0;
		}
		while (c = fgetc(members)) {
			if (c == EOF) { // stop looping through users
				is_last_entry = 1;
				break;
			}
			if (c == '\n' || c == '\r') break; // try next user
		}
	}
	fclose(members);
	bad_uname(uname); // no existing usernames returned matches
	return 0;
}

/**
 * edit site_name to run from a separate home page!
 */
const char* site_name = "http://cs.mcgill.ca/~rbelya";

/**
 * prints header to html output
 */
int html_head(void) {
	printf("Content-Type:text/html\n\n");
	printf("<html>\n");
	return 0;
}

/**
 * prints start of html body;
 * <title> field should go between
 * html_head() output and this
 */
int html_body_start(void) {
	//printf("<center>\n");
	//printf("\t<head>\n");
	//printf("\t\t<b> PaperPlanes </b> <br />\n");
	//printf("\t\tCome fly with us. <br />\n");
	//printf("\t</head>\n");
	printf("<body>\n");
	printf("<table height=\"100\%\" width=\"100\%\" cellspacing=\"0\" cellpadding=\"0\" border=\"0\" background=\"pictures/bg1.jpg\">\n");
	printf("<tr><td align=center>\n");
	printf("<h1> PaperPlanes </h1>\n");
	printf("<h4>Come fly with us</h4>\n");
	printf("<marquee behavior=\"scroll\" direction=\"left\">\n");
	printf("<img src=\"./pictures/pap1.png\" alt=\"Flying plane\" width=100>\n");
	printf("</marquee>\n");

	return 0;
}

/**
 * prints tail of html output
 */
int html_tail(void) {
	printf("</td></tr>\n");
	printf("</table>\n");

	printf("\t</body>\n");
	printf("</center>\n");
	printf("</html>\n");
	return 0;
}

/**
 * goes to fail page with a given message;
 * used for bad_uname() and bad_pass()
 */
int fail_page(char *message) {
	html_head();
	printf("<title> Login </title>\n");
	html_body_start();
	printf("\t\t<font color=\"red\"> %s </font> <br />\n",message);
	printf("\t\t<a href=\"%s/welcome.html\"> Try again? </a> <br />\n",site_name);
	printf("\t\t<a href=\"%s/register.html\"> Create an account? </a> <br />\n",site_name);
	html_tail();
	return 0;
}

/**
 * gives the user access to the main page
 */
int login(char *uname) {
	html_head();
	printf("<title> Welcome </title>\n");
	html_body_start();	
	printf("\t\tSuccess! <br />\n");
	printf("\t\t<form action=\"./mainPage.sh\" method=\"post\">\n");
	printf("\t\t\t<input type=\"hidden\" name=\"uname\" value=\%s>\n",uname);

	printf("\t\t\t<input type=\"submit\" value=\"Continue to the site.\">\n");
	printf("\t\t</form>\n");
	html_tail();
	return 0;
}

/**
 * password was not correct
 */
int bad_pass(char *uname) {
	char *message = "Incorrect password.";
	fail_page(message);		
	return 0;
}

/**
 * username was not found in database
 */
int bad_uname(char *uname) {
	char *message = "Username not found.";
	fail_page(message);
	return 0;
}
