import ply.lex as lex
import lang.typeclass as tc
import lang.astnode as ast

keywords = (
    'IF',
    'WHILE',
    'ELSE',
    'DEF',
    'RET',
)

keywords_map = {}
for keyword in keywords:
    keywords_map[keyword.lower()] = keyword

tokens = keywords + (
    'CONST',
    'FIELD',  # a, b, c, d ...
    'OPERLV0',  # */
    'OPERLV1',  # +-
    'OPERLV2',  # > < >= <= == !=
    'ASSIGN',  # =
    'LPAREN',  # (
    'RPAREN',  # )
    'LSQUARE',  # [
    'RSQUARE',  # ]
    'LCURLY',  # {
    'RCURLY',  # }
    'COMMA',  # ,
    'COLON',
    'END',
)

t_COLON = r':'
t_ASSIGN = r'='
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_COMMA = r','
t_ignore = ' \t'


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


def t_LCURLY(t):
    r'\{'
    return t


def t_RCURLY(t):
    r'\}'
    return t


def t_NumFloat(t):
    r'\d+\.\d+'
    t.type = 'CONST'
    t.value = ast.AstConst(tc.TypeFloat(t.value))
    return t


def t_NumInt(t):
    r'\d+'
    t.type = 'CONST'
    t.value = ast.AstConst(tc.TypeInt(t.value))
    return t


def t_STRING(t):
    r'"[^"]*"'
    t.type = 'CONST'
    t.value = ast.AstConst(tc.TypeString(t.value[1:-1]))
    return t


def t_Boolean(t):
    r'true|false'
    t.type = 'CONST'
    t.value = ast.AstConst(tc.TypeBool(t.value))
    return t


def t_FIELD(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in keywords_map:
        t.type = keywords_map[t.value]
    else:
        t.value = ast.AstField(t.value)
    return t


def t_NEWLINE(t):
    r'[ \n]+'
    t.lexer.lineno += t.value.count('\n')
    # ignore newline if we are in a paren
    if t.lexer.paren_level != 0:
        return
    t.type = 'END'
    t.value = ast.AstEnd()
    return t


def t_SEMI(t):
    r';'
    t.type = 'END'
    t.value = ast.AstEnd()
    return t


def t_COMMENT(t):
    r'\#.*'
    pass


def t_error(t):
    print('Illegal character %s' % t.value[0])
    raise SyntaxError


lexer = lex.lex()
lexer.paren_level = 0
