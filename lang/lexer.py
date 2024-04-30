import ply.lex as lex
import lang.astnode as ast

keywords = (
    'IF',
    'ELSE',
    'DEF',
    'RET',
)

keywords_map = {}
for keyword in keywords:
    keywords_map[keyword.lower()] = keyword

tokens = keywords + (
    'NUMBER',
    'STRING',
    'FIELD', # a, b, c, d ...
    'OPERLV0', # */
    'OPERLV1', # +-
    'OPERLV2', # > < >= <= == !=
    'ASSIGN', # =
    'LPAREN', # (
    'RPAREN', # )
    'LSQUARE', # [
    'RSQUARE', # ]
    'LCURLY', # {
    'RCURLY', # }
    'COMMA', # ,

    'END',
)

t_ASSIGN = r'='
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_COMMA = r','
t_ignore = ' \t'
t_ignore_COMMENT=r'^\n'

def t_OPERLV0(t):
    r'\*|/'
    return t

def t_OPERLV1(t):
    r'\+|-'
    return t

def t_OPERLV2(t):
    r'>|<|>=|<=|==|!='
    return t

def t_LPAREN(t):
    r'\('
    t.lexer.paren_level += 1
    return t

def t_RPAREN(t):
    r'\)'
    t.lexer.paren_level -= 1
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = ast.AstNumber(t.value)
    return t

def t_FIELD(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in keywords_map:
        t.type = keywords_map[t.value]
    else:
        t.value = ast.AstField(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = ast.AstString(t.value[1:-1])
    return t

def t_END(t):
    r'[;\n]+'
    if t.value.endswith('\n'):
        # count '\n' in the line number
        t.lexer.lineno += t.value.count('\n')
    if ';' not in t.value and t.lexer.paren_level > 0:
        return
    t.type = 'END'
    t.value = ast.AstEnd()
    return t

def t_error(t):
    print('Illegal character %s' % t.value[0])
    raise SyntaxError

lexer = lex.lex()
lexer.paren_level = 0

