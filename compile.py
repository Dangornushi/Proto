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
        l.append(p[2])
        p[0] = l
    else:
        p[0] = p[1]


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

def p_sent_define(p):
    """
    sent : FN ID KAKKO shiki KOKKA COLON sents END SEMI
    """
    p[0] = ("fn", p[2], p[4], p[7])

def p_sent_call(p):
    """
    sent : ID KAKKO shiki KOKKA SEMI
    """
    p[0]= ("call", p[1], p[3])

def p_sent_mov(p):
    """
    sent : TYPE ID EQOL shiki  SEMI
    """
    p[0] = ("mov", p[1], p[2], p[4])


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
funcd = {}

valld["0_start"] = {}
regd["0_start"] = {}

wordslist = []

regcount = 0

class Tasks:
    def __init__(self):
        pass
    def t_mov(self, r, vall, type):
        walker.append(">"+type[0]+";!r"+str(r)+"/"+vall+";")
    
    def t_put(self, r, type):
        walker.append(">"+type[0]+";"+"\""+str(r)+";")

class Walker:
    def __init__(self):
        self.ts = Tasks()

    def file_write(self):
        global wordslist
        with open("data", "wb") as fout:
            for x in wordslist:
                for item in x:
                    fout.write(item.encode())
    
    def append(self, data):
        wordslist.append( data )

    def steps(self, ast):
        global valld, regd, funcname, nowvall, regcount, funcd
        if ast[0] == "mov":
            #TODO : mov 
            self.steps(ast[3])

            valld[funcname][ast[2]] = nowvall
            regd[funcname][ast[2]] = regcount
            self.ts.t_mov(regcount, nowvall, ast[1])
            regcount+=1
        
        elif ast[0] == "shiki":
            nowvall = ast[1]

        elif ast[0] == "put":
            self.steps(ast[1])
            self.ts.t_put( regd[funcname][nowvall],  ast[2])
        
        elif ast[0] == "fn":
            funcd[ast[1]] = ast

        elif ast[0] == "call":
            print(ast)
            #pass
        
        elif type(ast[0]) == list or type(ast[0]) == tuple:
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
