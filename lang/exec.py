import lang.visitor as vis
import lang.astnode as ast

class Interpreter(vis.NodeVisitor):
    parentvarlist = {}
    varlist = {}
    funclist = {}
    retVal = None
    retFlag = False
    def __init__(self):
        self.funclist = {
            'print' : print
        }
        pass
    def visit_AstProgram(self, node : ast.AstProgram):
        self.visit(node.body)
    def visit_AstStatList(self, node : ast.AstStatList):
        for i in range(len(node.body)):
            self.visit(node.body[i])
            if self.retFlag:
                return
    def visit_AstAssign(self, node : ast.AstAssign):
        self.varlist[node.field.name] = self.visit(node.expr)
        return self.varlist[node.field.name]
    def visit_AstIf(self, node : ast.AstIf):
        if self.visit(node.condition):
            self.visit(node.then)
        elif node.else_:
            self.visit(node.else_)
    def visit_AstBinaryOper(self, node : ast.AstBinaryOper):
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
    def visit_AstNumber(self, node : ast.AstNumber):
        return node.value
    def visit_AstField(self, node : ast.AstField):
        return self.varlist[node.name]
    def visit_AstString(self, node : ast.AstString):
        return node.value
    def visit_AstFuncDecl(self, node : ast.AstFuncDecl):
        self.funclist[node.name] = node
    def visit_AstRet(self, node : ast.AstRet):
        self.retVal = self.visit(node.expr)
        self.retFlag = True
    def visit_AstFuncCall(self, node : ast.AstFuncCall):
        func = self.funclist.get(node.name)
        if not func:
            raise Exception(f"Function {node.name} not found")
        if type(func) != ast.AstFuncDecl:
            # built-in function
            return func(*[self.visit(arg) for arg in node.params])
        # user-defined function
        initVarlist = {}
        for i in range(len(func.params)):
            initVarlist[func.params[i].name] = self.visit(node.params[i])
        return FuncExecutor(self, func.body, initVarlist)



def FuncExecutor(parent: Interpreter, node:ast.AstFuncDecl, varlist={}):
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