#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

int opc = 0;
int dc = 0;
char stack[256][256] = {};
char *mode;

int main( int argc, char *argv[] ) {
    FILE *file;
    int data;
    char stack[256][256];
    char datas[256][256] = {};
    char command[16] = "python3 main.py ";
    char new_command[256];
    sprintf(new_command, "%s%s", command, argv[1]);
    /*command power ON/OFF*/
    //system(new_command);
    char file_name[256];
    file = fopen(strtok(argv[1], "."), "rb");    // ファイルを読み込み用にオープン(開く)
    while ( (data=fgetc(file)) != EOF){
        switch (data) {
            case 0x3b: {
                char *line_data; //TODO : 一行ずつのデータ、ここから切り出して処理
                char *opcode;
                for ( int deel = 0; deel < sizeof(datas[dc]); deel++ ) {
                    if ( datas[dc][deel] != 0x00 ) {
                        line_data = &datas[dc][deel];
                        switch (line_data[0]) {
                            case 0x21: {
                                //TODO : mov
                                if ( strcmp(mode,"i") == 0) {
                                    //TODO : もし代入の値が整数型であれば
                                    int op1 = atoi(strtok(&line_data[2], "/"));// &;
                                    int op2 = atoi(strtok(NULL, "/"));
                                    stack[op1][0] = op2;                        
                                }
                                else
                                if ( strcmp(mode,"r") == 0) {
                                    int op1 = atoi(strtok(&line_data[2], "/"));
                                    int op2 = atoi(&strtok(NULL, "/")[1]);
                                    stack[op1][0] = stack[op2][0];
                                }
                                else {
                                    int linesize = 0;
                                    for (;;) {
                                        if (line_data[linesize] != 0x00 ) { linesize++; }
                                        else { break; }
                                    }
                                    int op1;
                                    char *op2;
                                    char *tp;
                                    tp = strtok( line_data, "/" );
                                    int size = 0;
                                    op1 = atoi(&tp[2]);
                                    int c = 0;
                                    while ( 1 ) {
                                        tp = strtok( NULL,"/" );
                                        if ( tp != NULL ) {
                                            op2 = tp;
                                        }
                                        else { 
                                            break;
                                        }
                                        c++;
                                    }
                                    for ( size_t i = 0; i < linesize; i++ ) {
                                        stack[op1][i] = op2[i];
                                    }
                                    
                                }
                                break;
                            }

                            case 0x22: {
                                if (strcmp(mode,"s") == 0) {
                                    printf("%s\n", stack[atoi(&line_data[1])]);
                                }
                                else {
                                    printf("%d\n", stack[atoi(&line_data[1])][0]);
                                }
                                break;
                            }

                            case 0x2a: {
                                char *base = strtok(line_data, "*");
                                int op1 = atoi(strtok(base, "/"));
                                int op2 = atoi(strtok(NULL, "/"));
                                stack[op1][0] = stack[op1][0] * stack[op2][0];
                                break;
                            }

                            case 0x2d: {
                                char *base = strtok(line_data, "-");
                                int op1 = atoi(strtok(base, "/"));
                                int op2 = atoi(strtok(NULL, "/"));
                                stack[op1][0] = stack[op1][0] - stack[op2][0];
                                break;
                            }

                            case 0x2f: {
                                char *base = strtok(line_data, "/");
                                int op1 = atoi(strtok(base, "/"));
                                int op2 = atoi(strtok(NULL, "/"));
                                stack[op1][0] = stack[op1][0] / stack[op2][0];
                                break;
                            }

                            case 0x2b: {
                                char *base = strtok(line_data, "+");
                                int op1 = atoi(strtok(base, "/"));
                                int op2 = atoi(strtok(NULL, "/"));
                                stack[op1][0] = stack[op1][0] + stack[op2][0];
                                break;
                            }

                            case 0x3e: {
                                char *now_mode = &line_data[1];
                                mode = now_mode;
                                break;
                            }
                            
                            default:
                                break;
                        }
                        
                        break;
                    }
                }
                
                dc++;
                break;
            }
            
            default: {
                if ( data != 0x00 ) {
                    datas[dc][opc] = data;
                    opc++;
                }
                break;
            }
        }
        
    }
    fclose(file);
}