import ply.lex as lex
import lang.typeclass as tc
import lang.astnode as ast

keywords = (
    'IF',
    'WHILE',
    'ELSE',
    'DEF',
    'RET',
    'CLASS',
)

keywords_map = {}
for keyword in keywords:
    keywords_map[keyword.lower()] = keyword

tokens = keywords + (
    'CONST',
    'FIELD',  # a, b, c, d ...
    'UNARY',  # ! ~ (include OPERLV1)
    'OPERLV0',  # */
    'OPERLV1',  # +-
    'OPERLV2',  # > < >= <= == !=
    'OPERLV3',  # && ||
    'ASSIGN',  # =
    'LPAREN',  # (
    'RPAREN',  # )
    'LSQUARE',  # [
    'RSQUARE',  # ]
    'LCURLY',  # {
    'RCURLY',  # }
    'COMMA',  # ,
    'DOT',  # .
    'COLON',
    'END',
)

t_COLON = r':'
t_ASSIGN = r'='
t_COMMA = r','
t_ignore = ' \t'


def t_NumFloat(t):
    r'\d+\.\d+'
    set_last_token(t.lexer, 'const')
    t.type = 'CONST'
    t.value = ast.AstConst(tc.TypeFloat(t.value))
    return t


def t_NumInt(t):
    r'\d+'
    set_last_token(t.lexer, 'const')
    t.type = 'CONST'
    t.value = ast.AstConst(tc.TypeInt(t.value))
    return t


def t_STRING(t):
    r'"[^"]*"'
    set_last_token(t.lexer, 'const')
    t.type = 'CONST'
    t.value = ast.AstConst(tc.TypeString(t.value[1:-1]))
    return t


def t_Boolean(t):
    r'true|false'
    set_last_token(t.lexer, 'const')
    t.type = 'CONST'
    t.value = ast.AstConst(tc.TypeBool(t.value))
    return t


def t_DOT(t):
    r'\.'
    return t


def t_UNARY(t):
    r'!|~'
    set_last_token(t.lexer, 'oper')
    return t


def t_OPERLV0(t):
    r'\*|/|%'
    set_last_token(t.lexer, 'oper')
    return t


def t_OPERLV1(t):
    r'\+|-'
    set_last_token(t.lexer, 'oper')
    return t


def t_OPERLV2(t):
    r'>=|<=|==|!=|>|<'
    set_last_token(t.lexer, 'oper')
    return t


def t_OPERLV3(t):
    r'&&|\|\|'
    set_last_token(t.lexer, 'oper')
    return t


def t_LPAREN(t):
    r'\('
    t.lexer.paren_level += 1
    return t


def t_RPAREN(t):
    r'\)'
    t.lexer.paren_level -= 1
    return t


def t_LSQUARE(t):
    r'\['
    return t


def t_RSQUARE(t):
    r'\]'
    return t


def t_LCURLY(t):
    r'\{'
    set_last_token(t.lexer, 'lcurly')
    return t


def t_RCURLY(t):
    r'\}'
    # add a fake token to indicate the end of the block
    if t.lexer.rcurly_end:
        t.lexer.rcurly_end = False
        set_last_token(t.lexer, 'rcurly')
    else:
        t.lexer.rcurly_end = True
        t.type = 'END'
        t.value = ast.AstEnd()
        t.lexer.lexpos -= 1
    return t


def t_FIELD(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    set_last_token(t.lexer, t.value)
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
    if t.lexer.last_token == 'if':
        return
    if t.lexer.last_token == 'while':
        return
    if t.lexer.last_token == 'else':
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


def set_last_token(lexer, name):
    # only record the last token if we are not in a paren
    if lexer.paren_level == 0:
        lexer.last_token = name


lexer = lex.lex(optimize=True, outputdir='generated')
lexer.paren_level = 0
lexer.last_token = None
lexer.rcurly_end = False
