import lang.visitor as vis
import lang.astnode as ast
import lang.typeclass as tc
import os


def cls():
    os.system('clear')


def float_(val):
    return float(val)


build_in_func = {'print': print, 'input': input, 'float': float_, 'cls': cls}


class Interpreter(vis.NodeVisitor):
    parentvarlist = {}
    varlist = {}
    funclist = {}
    retVal = None
    retFlag = False

    def __init__(self):
        self.parentvarlist = {}
        self.varlist = {}
        self.funclist = build_in_func
        self.retVal = None
        self.retFlag = False
        pass

    def visit_AstProgram(self, node: ast.AstProgram):
        self.visit(node.body)

    def visit_AstStatList(self, node: ast.AstStatList):
        for i in range(len(node.body)):
            self.visit(node.body[i])
            if self.retFlag:
                return

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
        if self.varlist.get(node.field.name):
            rvalue = self.visit(node.expr)
            self.varlist[node.field.name] = rvalue
        else:
            raise SyntaxError(f"Variable '{node.field.name}' not found")

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
        return self.varlist[node.name]

    def visit_AstFuncDecl(self, node: ast.AstFuncDecl):
        self.funclist[node.name] = node

    def visit_AstRet(self, node: ast.AstRet):
        self.retVal = self.visit(node.expr)
        self.retFlag = True

    def visit_AstFuncCall(self, node: ast.AstFuncCall):
        func = self.funclist.get(node.name)
        if not func:
            raise Exception(f"Function {node.name} not found")
        if type(func) != ast.AstFuncDecl:
            # built-in function
            if node.params:  # has parameters
                return func(*[self.visit(arg) for arg in node.params])
            else:
                return func()
        # user-defined function
        initVarlist = {}
        if func.params:
            for i in range(len(func.params)):
                initVarlist[func.params[i].name] = self.visit(node.params[i])
        return FuncExecutor(self, func.body, initVarlist)


def FuncExecutor(parent: Interpreter, node: ast.AstFuncDecl, varlist={}):
    """
    node: ast.AstFuncDecl
    varlist: initial variable list
    """
    interpreter = Interpreter()
    interpreter.parentvarlist = parent.varlist
    interpreter.funclist = parent.funclist
    interpreter.varlist = varlist
    interpreter.visit(node)
    return interpreter.retVal
