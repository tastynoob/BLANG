import ply.yacc as yacc
import lang.astnode as ast
from lang.lexer import tokens
import copy

start = "program"


def p_program(p):
    """program : stat_list"""
    p[0] = ast.AstProgram(p[1])


def p_stat_list(p):
    """stat_list : stat
    | stat_list stat"""
    if type(p[1]) == ast.AstEnd:
        p[0] = ast.AstStatList()
    elif len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if type(p[2]) == ast.AstEnd:
            p[0] = p[1]
        else:
            p[0] = ast.AstStatList(p[1], p[2])


def p_stat(p):
    """stat : stat_expr
    | stat_ret
    | stat_if
    | stat_compound
    | func_decl
    | END"""
    p[0] = p[1]


def p_stat_compound(p):
    """stat_compound : LCURLY RCURLY
    | LCURLY stat_list RCURLY"""
    if len(p) == 3:
        p[0] = ast.AstNode()
    else:
        p[0] = p[2]


def p_stat_if(p):
    """stat_if : IF LPAREN expr RPAREN stat %prec LOWER_THAN_ELSE
    | IF LPAREN expr RPAREN stat ELSE stat"""
    if len(p) == 6:
        p[0] = ast.AstIf(p[3], p[5])
    else:
        p[0] = ast.AstIf(p[3], p[5], p[7])


def p_call_params_list(p):
    """call_params_list : expr
    | call_params_list COMMA expr"""
    if len(p) == 2:
        p[0] = ast.AstCallParamsList(p[1])
    else:
        p[0] = ast.AstCallParamsList(p[1], p[3])


def p_func_call(p):
    """func_call : FIELD LPAREN call_params_list RPAREN
    | FIELD LPAREN RPAREN"""
    if len(p) == 5:
        p[0] = ast.AstFuncCall(p[1].name, p[3])
    else:
        p[0] = ast.AstFuncCall(p[1].name)


def p_params_list(p):
    """params_list : FIELD
    | params_list COMMA FIELD"""
    if len(p) == 2:
        p[0] = ast.AstParamsList(p[1])
    else:
        p[0] = ast.AstParamsList(p[1], p[3])


def p_func_decl(p):
    """func_decl : DEF FIELD LPAREN params_list RPAREN stat_compound"""
    if len(p) == 7:
        p[0] = ast.AstFuncDecl(p[2].name, p[4].params, p[6])

def p_stat_ret(p):
    """stat_ret : RET stat_expr"""
    p[0] = ast.AstRet(p[2])

def p_stat_expr(p):
    """stat_expr : expr END"""
    p[0] = p[1]

def p_expr_oper(p):
    """expr : FIELD ASSIGN expr
    | expr OPERLV2 expr
    | expr OPERLV1 expr
    | expr OPERLV0 expr
    | LPAREN expr RPAREN
    | NUMBER
    | FIELD
    | STRING
    | func_call"""
    if p[1] == "(":
        p[0] = p[2]
    elif len(p) == 4:
        if p[2] == "=":
            p[0] = ast.AstAssign(p[1], p[3])
        else:
            p[0] = ast.AstBinaryOper(p[2], p[1], p[3])
    elif len(p) == 3:
        p[0] = ast.AstBinaryOper(p[1], ast.AstNumber(0), p[2])
    else:
        p[0] = p[1]


def p_error(p):
    print(p)
    raise Exception("Syntax error")


precedence = (
    ("nonassoc", "LOWER_THAN_ELSE"),
    ("nonassoc", "ELSE"),
    ("left", "ASSIGN"),
    ("left", "OPERLV2"),
    ("left", "OPERLV1"),
    ("left", "OPERLV0"),
    ("left", "LPAREN", "RPAREN"),
    ("left", "LCURLY", "RCURLY"),
    ("left", "COMMA"),
    ("left", "END"),
)


parser = yacc.yacc(outputdir="generated")
