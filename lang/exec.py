import lang.visitor as vis
import lang.astnode as ast
import lang.typeclass as tc
import time
import os

def print_(val):
    if type(val) == tc.TypeString:
        val = val.replace('\\n', '\n')
    print(val, end='')

def println_(val):
    print_(val)
    print()

def cls():
    os.system('clear')


def float_(val):
    return tc.TypeFloat(val)


def int_(val):
    return tc.TypeInt(val)


def time_():
    return tc.TypeInt(time.time_ns())

build_in_func = {
    'print': print_,
    'println': println_,
    'input': input,
    'float': float_,
    'int': int_,
    'cls': cls,
    'time': time_
}


class Interpreter(vis.NodeVisitor):
    parentvarlist = {}
    varlist = {}
    funclist = {}

    def __init__(self):
        self.parentvarlist = {}
        self.varlist = {}
        self.funclist = build_in_func
        pass

    def visit_AstProgram(self, node: ast.AstProgram):
        self.visit(node.body)

    def visit_AstStatList(self, node: ast.AstStatList):
        for i in range(len(node.body)):
            self.visit(node.body[i])

    def visit_AstIf(self, node: ast.AstIf):
        if self.visit(node.condition):
            self.visit(node.then)
        elif node.else_:
            self.visit(node.else_)

    def visit_AstWhile(self, node: ast.AstWhile):
        while self.visit(node.condition):
            self.visit(node.body)

    def visit_AstVarDecl(self, node: ast.AstVarDecl):
        varType = node.varType
        if varType:
            # explicit type
            typeclass = getattr(tc, "Type" + varType.capitalize(), None)
            if not typeclass:
                raise SyntaxError(f"Unknown type '{varType}'")
            self.varlist[node.varname] = typeclass(self.visit(node.expr))
        else:
            # auto type
            var = self.visit(node.expr)
            node.varType = type(var).__name__.lower().replace('type', '')
            self.varlist[node.varname] = var

    def visit_AstAssign(self, node: ast.AstAssign):
        if self.varlist.get(node.field.name) is not None:
            rvalue = self.visit(node.expr)
            self.varlist[node.field.name] = rvalue
        else:
            raise SyntaxError(f"Variable '{node.field.name}' not found")
        return rvalue

    def visit_AstUnaryOper(self, node: ast.AstUnaryOper):
        expr = self.visit(node.expr)
        if node.operator == '+':
            return expr
        elif node.operator == '-':
            return -expr
        elif node.operator == '!':
            return not expr
        elif node.operator == '~':
            return ~expr
        else:
            raise SyntaxError(f"Unknown operator {node.operator}")


    def visit_AstBinaryOper(self, node: ast.AstBinaryOper):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.operator == '+':
            return left + right
        elif node.operator == '-':
            return left - right
        elif node.operator == '*':
            return left * right
        elif node.operator == '/':
            return left / right
        elif node.operator == '%':
            return left % right
        elif node.operator == '<':
            return left < right
        elif node.operator == '>':
            return left > right
        elif node.operator == '<=':
            return left <= right
        elif node.operator == '>=':
            return left >= right
        elif node.operator == '==':
            return left == right
        elif node.operator == '!=':
            return left != right
        else:
            raise Exception(f"Unknown operator {node.operator}")

    def visit_AstConst(self, node: ast.AstConst):
        return node.value

    def visit_AstField(self, node: ast.AstField):
        field = node.name
        return self.varlist[field]

    def visit_AstFuncDecl(self, node: ast.AstFuncDecl):
        self.funclist[node.name] = node

    def visit_AstFuncCall(self, node: ast.AstFuncCall):
        funcExecutor = FuncExecutor(self, node)
        return funcExecutor.retVal

    def visit_AstRet(self, node: ast.AstRet):
        raise Exception("Return statement not in function")


class FuncExecutor(Interpreter):
    retVal = None
    retFlag = False

    def __init__(self, parent: Interpreter, funcCall: ast.AstFuncCall):
        super().__init__()
        self.retVal = None
        self.retFlag = False
        self.funclist = parent.funclist
        func = self.funclist.get(funcCall.name)
        if not func:
            raise Exception(f"Function {funcCall.name} not found")
        if type(func) != ast.AstFuncDecl:
            # built-in function
            if funcCall.params:
                self.retVal = func(*[parent.visit(arg) for arg in funcCall.params])
            else:
                self.retVal = func()
        else:
            # user-defined function
            if func.params:
                for i in range(len(func.params)):
                    self.varlist[func.params[i].name] = parent.visit(funcCall.params[i])
            self.visit(func.body)

    def visit_AstStatList(self, node: ast.AstStatList):
        for i in range(len(node.body)):
            self.visit(node.body[i])
            if self.retFlag:
                return

    def visit_AstRet(self, node: ast.AstRet):
        self.retVal = self.visit(node.expr)
        self.retFlag = True
