# -*- coding: utf-8 -*-
from io import open_code
import ply.yacc as yacc
from lex import tokens
import sys, struct

def p_sents(p):
    """
    sents : sent
          | sents sent
    """
    if (len(p) > 2):
        l = list([p[1]])
        l.append([p[2]])
        p[0] = l
    else:
        p[0] = [p[1]]


def p_shiki(p):
    """
    shiki : ID
          | NUMBER
          | STR
    """
    p[0] = ("shiki", p[1])

def p_shiki_conma(p):
    """
    shiki : shiki CONMA
    """
    p[0] = p[1]

def p_sent_mov(p):
    """
    sent : ID EQOL shiki  SEMI
    """
    p[0] = ("mov", p[1], p[3])


def p_sent_put(p):
    """
    sent : PUT KAKKO shiki CONMA TYPE KOKKA SEMI
    """
    p[0] = ("put", p[3], p[5])

def p_error(p):
    print("SyntaxErr : すみません、 %sに当てはまる文法作るのやめてもらっていいすか？" % p)


funcname = "0_start"
nowvall = ""

valld = {}
regd = {}

valld["0_start"] = {}
regd["0_start"] = {}

wordslist = []

regcount = 0

class Walker(object):
    def __init__(self):
        pass

    def file_write(self):
        global wordslist
        with open("data", "wb") as fout:
            for x in wordslist:
                fout.write(x.encode())
    
    def append(self, data):
        wordslist.appen( data+"\n" )

    def steps(self, ast):
        global valld, regd, funcname, nowvall, regcount
        if ast[0] == "mov":
            self.steps(ast[2])
            valld[funcname][ast[1]] = nowvall
            regcount+=1
        
        elif ast[0] == "shiki":
            nowvall = ast[1]

        elif ast[0] == "put":
            print(ast)
        else:
            for item in ast:
                self.steps(item)

parser = yacc.yacc(debug=0, write_tables=0)

if __name__ == '__main__':
    walker = Walker()
    infunc = False
    result = ""

    open_file = open(sys.argv[1], "r", encoding="utf_8").readlines()
    
    for item in open_file:
        item = item.replace("\n", "");
        if item.startswith("fn "):
            infunc = True
            result += item
        elif item.startswith("end;"):
            infunc = False
            result += item
            walker.steps(parser.parse(result))
        elif infunc and item != "\n":
            result += item
        else:
            walker.steps(parser.parse(item))
