import ply.lex as lex

tokens = (
#    "STR",
    "NUMBER",
    "ID",
    "STR",
    "IF",
    "ELSE",
    "ELIF",
    "WHILE",
    "PLUS",
    "MINUS",
    "KAKERU",
    "WARU",
    "EQOL",
    "EQOLS",
    "DAINARI",
    "SYOUNARI",
    "CONMA",
    "PIRIOD",
    "KAKKO",
    "KOKKA",
    "LKAKKO",
    "LKOKKA",
    "TYPE",
    "PUT",
    "COLON",
    "SEMI",
    "END",
    "QOT",
    "FN",
    "RETURN",
    "INPUT",
    "OR",
    "AND",
)

t_CONMA = r","
t_PIRIOD = r"\."
t_PLUS = r"\+"
t_MINUS = r"\-"
t_KAKERU = r"\*"
t_WARU = r"\/"
t_EQOL = r"\="
t_EQOLS = r"\=\="
t_KAKKO = r"\("
t_KOKKA = r"\)"
t_NUMBER = r"\d+"
t_LKAKKO = r"\["
t_LKOKKA = r"\]"
t_ignore = r' \t'
t_COLON = r"\:"
t_SEMI = r"\;"
t_DAINARI = r"\>"
t_SYOUNARI = r"\<"
t_QOT = r"\""
t_OR = r"\|\|"
t_AND = "&&"

def t_STR (t):
    r"[\"'][_\<\>\.,\*+-/\!\?a-zA-Z0-9\"' ]*"
    return t

def t_ID (t):
    r"[a-zA-Z_][a-zA-Z0-9_|\&]*"
    if t.value == "int":
        t.type = "TYPE"
    elif t.value == "str":#t.value == "float" or 
        t.type = "TYPE"
    elif t.value == "void":
        t.type = "TYPE"
    elif t.value == "put":
        t.type = "PUT"
    elif t.value == "end":
        t.type = "END"
    elif t.value == "if":
        t.type = "IF"
    elif t.value == "else":
        t.type = "ELSE"
    elif t.value == "elif":
        t.type = "ELIF"
    elif t.value == "while":
        t.type = "WHILE"
    elif t.value == "fn":
        t.type = "FN"
    elif t.value == "return":
        t.type = "RETURN"
    elif t.value == ",":
        t.type = "CONMA"
    elif t.value == "input":
        t.type = "INPUT"
    elif t.value == "&&" or t.value == "and":
        t.type = "AND"
    elif t.value == "||" or t.value == "or":
        t.type = "OR"
    else:
        t.type == "ID"
    return t

def t_error(t):
    print("LexErr：%s, それ、あなたの感想ですよね？" % t.value[0])
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

lexer = lex.lex(debug=0)