# -*- coding: utf-8 -*-
import sys, struct
import ply.yacc as yacc
from lex import tokens
from helps import Option_Commandlines


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
    """
    p[0] = ("shiki", p[1])

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

def p_shiki_input(p):
    """
    shiki : INPUT KAKKO shiki KOKKA 
    """
    p[0] = ("input", p[3])

def p_compa(p):
    """
    compa : shiki EQOLS shiki
          | shiki DAINARI shiki
          | shiki SYOUNARI shiki
    """
    p[0] = ("compa", p[1], p[2], p[3] ) 

def p_shiki_plusplus(p):
    """
    sent : shiki PLUS PLUS SEMI
    """
    p[0] = ("add", p[1], p[2], "1")

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

def p_sent_if_else(p):
    """
    sent : IF compa COLON sents ELSE COLON sents END SEMI
    """
    p[0] = ("IF-ELSE", p[2], p[4], p[7])

def p_sent_while(p):
    """
    sent : WHILE compa COLON sents END SEMI
    """
    p[0] = ( "WHILE", p[2], p[4] )

def p_sent_def(p):
    """
    sent :　ID EQOL shiki SEMI
    """
    p[0] = ("mov", p[1], p[3])

def p_sent_input(p):
    """
    sent : INPUT KAKKO shiki KOKKA SEMI
    """
    p[0] == ("input", p[3])

def p_sent_put(p):
    """
    sent : PUT KAKKO shiki KOKKA SEMI
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

reg_c = 0   #レジスタカウンタ / 変数宣言で+1される

funcname = "0_start"    #関数め / 初期値は0_start / 0_startは関数内ではない場合に宣言された仮の関数名
nowvall = ""

ifbool = False

datalis = []

valld = {}
regd = {}
funcd = {}

valld["0_start"] = {}
regd["0_start"] = {}

class Tasks:
    def __init__(self):
        pass
    def t_mov(self, type, r, vall):
        pass
    
    def t_put(self, type, r):
        pass

class Walker:
    def __init__(self):
        pass

    def append( self, data ):
        global datalis
        datalis.append(data)

    def ifb(self, l, r):
        global valld, funcname

        try:
            try:
                if int(valld[funcname][l]) > int(valld[funcname][r]):
                    return True
            
            except:
                try:
                    if int(valld[funcname][l]) > int(r):
                        return True
                except:
                    if int(l) > int(valld[funcname][r]):
                        return True
        except:
                try:
                    if int(l) > int(r):
                        return True
                except:
                    return False

    def file_write(self):
        global datalis
        with open("data", "wb") as fout:
            for x in datalis:
                for item in x:
                    fout.write(item.encode())
    
    def steps( self, ast ):
        global funcname, nowvall, valld, regd, funcd, reg_c, ifbool
        tasks = Tasks()

        if ast[0] == "defunc":
            funcd[ast[1]] = ast[3]
        
        elif ast[0] == "IF":
            self.steps(ast[1])
            if ifbool:
                self.steps(ast[2])

        elif ast[0] == "IF-ELSE":
            self.steps(ast[1])
            if ifbool:
                self.steps(ast[2])
            else:
                self.steps(ast[3])

        elif ast[0] == "WHILE":
            self.steps(ast[1])
            while ifbool:
                self.steps(ast[2])
        
        elif ast[0] == "compa":
            self.steps(ast[1])
            beforvall = nowvall
            self.steps(ast[3])
            if self.ifb(beforvall,nowvall) and ast[2] == ">":
                ifbool = True
            
            elif self.ifb(nowvall, beforvall) and ast[2] == "<":
                ifbool = True
            elif self.ifb(beforvall,nowvall) != True and self.ifb(nowvall, beforvall) != True and ast[2] == "==":
                ifbool = True
            
            else:
                ifbool = False
                
        elif ast[0] == "mov":
            self.steps(ast[2])

            valld[funcname][ast[1]] = nowvall   #変数名と保存する値を格納
            regd[funcname][ast[1]] = reg_c  #変数名とレジスタの名前を格納

            
            reg_c+=1    #レジスタカウンタ+1
        
        elif ast[0] == "add":
            self.steps(ast[1])
            if type( ast[3] )  == str:
                valld[funcname][nowvall] = int(valld[funcname][nowvall]) + 1
            else :
                beforvall = nowvall
                self.steps(ast[3])
                valld[funcname][beforvall] = int(valld[funcname][beforvall]) + int(valld[funcname][nowvall])
                nowvall = int(valld[funcname][beforvall])

        elif ast[0] == "sub":
            self.steps(ast[1])
            if type( ast[3] )  == str:
                valld[funcname][nowvall] = int(valld[funcname][nowvall]) - 1
            else :
                beforvall = nowvall
                self.steps(ast[3])
                valld[funcname][beforvall] = int(valld[funcname][beforvall]) - int(valld[funcname][nowvall])
                nowvall = int(valld[funcname][beforvall])
        
        elif ast[0] == "div":
            self.steps(ast[1])
            if type( ast[3] )  == str:
                valld[funcname][nowvall] = int(valld[funcname][nowvall]) * 1
            else :
                beforvall = nowvall
                self.steps(ast[3])
                valld[funcname][beforvall] = int(valld[funcname][beforvall]) * int(valld[funcname][nowvall])
                nowvall = int(valld[funcname][beforvall])
        
        elif ast[0] == "mul":
            self.steps(ast[1])
            if type( ast[3] )  == str:
                valld[funcname][nowvall] = int(valld[funcname][nowvall]) / 1
            else :
                beforvall = nowvall
                self.steps(ast[3])
                valld[funcname][beforvall] = int(valld[funcname][beforvall]) / int(valld[funcname][nowvall])
                nowvall = int(valld[funcname][beforvall])

        elif ast[0] == "input":
            beforvall= nowvall
            self.steps(ast[1])
            nowvall = input(nowvall)


        elif ast[0] == "put":
            self.steps(ast[1])
            try:
                print(valld[funcname][nowvall])
            except:
                print(nowvall)

        elif ast[0] == "call":
            func2 = funcname
            funcname = ast[1]
            valld[funcname] = {}
            regd[funcname] = {}

            if type(ast[2][0]) == str:
                self.steps(ast[2])
                valld[funcname][nowvall] = valld[func2][nowvall]
                regd[funcname][nowvall] = regd[func2][nowvall]
                
            else:
                for item in ast[2]:
                    self.steps(item)
            reg_c = 0
            self.steps(funcd[ast[1]])


        elif ast[0] == "shiki":
            nowvall = ast[1].replace("\"", "")

        elif type(ast[0]) == list or type(ast[0]) == tuple:
            for item in ast:
                self.steps(item) 

if __name__ == '__main__':
    walker = Walker()
    infunc = False
    result = ""

    OC = Option_Commandlines(sys.argv[1])
    if OC.options():
        open_file = open(sys.argv[1], "r", encoding="utf_8").readlines()

        for item in open_file:
            item = item.replace("\n", "")
            if item.startswith("fn ") or item.startswith("if ")  or item.startswith("while "):
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
