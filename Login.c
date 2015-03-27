#include <stdio.h>
#include <stdlib.h>

#define NULL_TERM '\0'

int main (void){
	int length = atoi(getenv("CONTENT_LENGTH"));
	char input[60];
	char c;
	int i = 0, j;
	while ((c = getchar()) != EOF && i < 60) {
		if (c == '+') input[i] = ' ';
		else input[i] = c;
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
}
