#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>


int main() {
  FILE *fptr;

  // Create a file on your computer (filename.txt)
  fptr = fopen("output-random-file.txt", "w");

  srand(time(NULL));
  int random_number = rand() % 50 + 1;
  
  if (fptr) {
        fprintf(fptr, "%d", random_number);
        fclose(fptr);
    }

  return 0;
}