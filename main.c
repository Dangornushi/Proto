#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main( int argc, char **argv ) {
    char command[256] = "python3 proto.py ";
    strcat( command, argv[1]);
    system(command);
    return 0;    
}