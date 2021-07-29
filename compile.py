# -*- coding: utf-8 -*-
from io import open_code
import ply.yacc as yacc
from lex import tokens
import sys, struct
from typing import ValuesView
import ply.yacc as yacc
from lex import tokens
import sys


def p_sents(p):
    """
    sents : sent
          | sents sent
    """
    if (len(p) > 2):
        l = list([p[1]])
        l.append(p[2])
        p[0] = l
    else:
        p[0] = p[1]

def p_paramlist(p):
    """
    paramlist : shiki
              | paramlist CONMA shiki
    """
    # ! important point!
    if (len(p) == 2):
        l = list(p[1])
        p[0] = l
    else:
        p[0] = p[1], 
        if type(p[1][0]) == list:
            l = list(p[1])
        else:
            l = list([p[1]])
        l.append(p[3])
        p[0] = l

def p_sent_shiki(p):
    """
    shiki : ID
          | STR
          | NUMBER
          | shiki
    """
    p[0] = ("shiki", p[1])

def p_shiki_plusplus(p):
    """
    shiki : shiki PLUS PLUS
    """
    p[0] = ("add", p[1], p[2], "1")

def p_shiki_calc(p):
    """
    shiki : shiki PLUS shiki
          | shiki MINUS shiki
          | shiki KAKERU shiki
          | shiki WARU shiki
    """
    if p[2] == "+": 
        p[0] = ("add", p[1], p[2], p[3])
    elif p[2] == "-":
        p[0] = ("sub", p[1], p[2], p[3])
    elif p[2] == "/":
        p[0] = ("mul", p[1], p[2], p[3])
    elif p[2] == "*":
        p[0] = ("div", p[1], p[2], p[3])

def p_compa(p):
    """
    compa : shiki EQOLS shiki
          | shiki DAINARI shiki
          | shiki SYOUNARI shiki
    """
    p[0] = ("compa", p[1], p[2], p[3] ) 

def p_sent_defunc(p):
    """
    sent : FN ID KAKKO paramlist KOKKA COLON sents END SEMI
    """
    p[0] = ("defunc", p[2], p[4], p[7])

def p_sent_if(p):
    """
    sent : IF compa COLON sents END SEMI
    """
    p[0] =("IF", p[2], p[4])

def p_sent_while(p):
    """
    sent : WHILE compa COLON sents END SEMI
    """
    p[0] = ( "WHILE", p[2], p[4] )
def p_sent_def(p):
    """
    sent : TYPE ID EQOL shiki SEMI
    """
    p[0] = ("defvall", p[1], p[3], p[5])

def p_sent_put(p):
    """
    sent : PUT KAKKO shiki CONMA TYPE KOKKA SEMI
    """
    p[0] = ( "put", p[3])

def p_sent_call(p):
    """
    sent : ID KAKKO paramlist KOKKA SEMI
    """
    p[0] = ("call", p[1], p[3])

def p_error(p):
    print ('SyntaxErr : すみません、 %sに当てはまる文法作るのやめてもらっていいすか？' % p)

parser = yacc.yacc(debug=0, write_tables=0)

datalis = []

funcname = ""
nowvall = ""

valld = {}
regd = {}
funcd = {}

class Walker:
    def __init__(self):
        pass

    def append( self, data ):
        global datalis
        datalis.append(data+"\n")

    def file_write(self):
        global datalis
        with open("data", "wb") as fout:
            for x in datalis:
                for item in x:
                    fout.write(item.encode())
    
    def steps( self, ast ):
        
        global funcname, nowvall, valld, regd, funcd

        if ast[0] == "defunc":
            funcname = ast[1]
            funcd[ast[1]] = ast[3]

        elif ast[0] == "mov":
            print(ast)

        elif ast[0] == "put":
            print(ast)

        elif ast[0] == "call":
            for item in ast[2]:
                self.steps(item)

        elif ast[0] == "shiki":
            nowvall = ast[1]

        elif type(ast[0]) == list or type(ast[0]) == tuple:
            for item in ast:
                self.steps(item) 

if __name__ == '__main__':
    walker = Walker()
    infunc = False
    result = ""

    open_file = open(sys.argv[1], "r", encoding="utf_8").readlines()
    for item in open_file:
        item = item.replace("\n", "");
        if item.startswith("fn "):
            infunc = True
            result = ""
            result += item
        elif item.startswith("end;"):
            infunc = False
            result += item
            if result != None:
                walker.steps(parser.parse(result))
        elif infunc and item != "\n":
            result += item
        else:
            if item != None and item != "\n" and item != "":
                walker.steps(parser.parse(item))
    walker.file_write()
