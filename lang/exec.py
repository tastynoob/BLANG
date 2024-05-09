import lang.visitor as vis
import lang.astnode as ast
import lang.typeclass as tc
import time
import os


def print_(val):
    if type(val) == tc.TypeString:
        val = val.replace("\\n", "\n")
    print(val, end="")


def println_(val):
    print_(val)
    print()


def cls():
    os.system("clear")


def float_(val):
    return tc.TypeFloat(val)


def int_(val):
    return tc.TypeInt(val)


def time_():
    return tc.TypeInt(time.time_ns())


def list_(x: tc.TypeString):
    # x: "1,2,3,4,5"
    x = x.split(",")
    return [int(i) for i in x]


build_in_func = {
    "print": print_,
    "println": println_,
    "input": input,
    "float": float_,
    "int": int_,
    "cls": cls,
    "time": time_,
    "list": list_,
}


class Interpreter(vis.NodeVisitor):
    varlist = {}
    funclist = {}
    classlist = {}

    def __init__(self):
        self.varlist = {}
        self.funclist = build_in_func
        self.classlist = {}

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
            if self.varlist.get(node.varname):
                if type(self.varlist[node.varname]) != typeclass:
                    raise SyntaxError(f"Variable '{node.varname}' already exists")
            self.varlist[node.varname] = typeclass(self.visit(node.expr))
        else:
            # auto type
            var = self.visit(node.expr)
            node.varType = type(var).__name__.lower().replace("type", "")
            self.varlist[node.varname] = var

    def visit_AstAssign(self, node: ast.AstAssign):
        rvalue = self.visit(node.expr)
        if type(node.lvalue) == ast.AstField:
            if self.varlist.get(node.lvalue.name) is not None:
                self.varlist[node.lvalue.name] = rvalue
            else:
                raise SyntaxError(f"Variable '{node.lvalue.name}' not found")
        elif type(node.lvalue) == ast.AstIndex:
            arr = self.visit(node.lvalue.point)
            index = self.visit(node.lvalue.index)
            arr[index] = rvalue
        elif type(node.lvalue) == ast.AstMbrSel:
            obj = self.visit(node.lvalue.object)
            assert type(node.lvalue.member) == ast.AstField
            memberName = node.lvalue.member.name
            obj.varlist[memberName] = rvalue
        else:
            raise SyntaxError(f"Unsupport lvalue type {type(node.lvalue)}")
        return rvalue

    def visit_AstUnaryOper(self, node: ast.AstUnaryOper):
        expr = self.visit(node.expr)
        if node.operator == "+":
            return expr
        elif node.operator == "-":
            return -expr
        elif node.operator == "!":
            return not expr
        elif node.operator == "~":
            return ~expr
        else:
            raise SyntaxError(f"Unknown operator {node.operator}")

    def visit_AstBinaryOper(self, node: ast.AstBinaryOper):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.operator == "+":
            return left + right
        elif node.operator == "-":
            return left - right
        elif node.operator == "*":
            return left * right
        elif node.operator == "/":
            return left / right
        elif node.operator == "%":
            return left % right
        elif node.operator == "<":
            return left < right
        elif node.operator == ">":
            return left > right
        elif node.operator == "<=":
            return left <= right
        elif node.operator == ">=":
            return left >= right
        elif node.operator == "==":
            return left == right
        elif node.operator == "!=":
            return left != right
        elif node.operator == "&&":
            return left and right
        elif node.operator == "||":
            return left or right
        else:
            raise Exception(f"Unknown operator {node.operator}")

    def visit_AstConst(self, node: ast.AstConst):
        return node.value

    def visit_AstIndex(self, node: ast.AstIndex):
        point = self.visit(node.point)
        index = self.visit(node.index)
        return point[index]

    def visit_AstField(self, node: ast.AstField):
        field = node.name
        return self.varlist[field]

    def visit_AstClassDecl(self, node: ast.AstClassDecl):
        self.classlist[node.name] = node

    def visit_AstMbrSel(self, node: ast.AstMbrSel):
        obj = self.visit(node.object)
        assert type(obj) == ClassDefiner
        if type(node.member) == ast.AstFuncCall:
            callee = node.member
            additonalVarlist = {
                'this': obj,
            }
            memberFuncDecl = obj.funclist.get(callee.name)
            if memberFuncDecl:
                funcExecutor = FuncCaller(
                    self, callee, memberFuncDecl, additonalVarlist
                )
                return funcExecutor.retVal
            else:
                raise SyntaxError(
                    f"Function '{callee.name}' not found in class '{obj.name}'"
                )
        elif type(node.member) == ast.AstField:
            return obj.varlist[node.member.name]

    def visit_AstFuncDecl(self, node: ast.AstFuncDecl):
        self.funclist[node.name] = node

    def visit_AstFuncCall(self, node: ast.AstFuncCall):
        calleeName = node.name
        # search in function list
        funcDecl = self.funclist.get(calleeName)
        classDecl = self.classlist.get(calleeName)
        if funcDecl:
            funcExecutor = FuncCaller(self, node, funcDecl)
            return funcExecutor.retVal
        # search in class list
        elif classDecl:
            newInstance = ClassDefiner(classDecl)
            return newInstance
        else:
            raise SyntaxError(f"Function '{calleeName}' not found")

    def visit_AstRet(self, node: ast.AstRet):
        raise Exception("Return statement not in function")


class FuncCaller(Interpreter):
    retVal = None
    retFlag = False

    def __init__(
        self,
        passing: Interpreter,
        funcCall: ast.AstFuncCall,
        funcDecl: ast.AstFuncDecl,
        additonalVarlist: dict = None,
    ):
        super().__init__()
        self.retVal = None
        self.retFlag = False
        self.funclist = passing.funclist
        self.classlist = passing.classlist

        if additonalVarlist:
            self.varlist = additonalVarlist

        if type(funcDecl) != ast.AstFuncDecl:
            # built-in function
            if funcCall.params:
                self.retVal = funcDecl(*[passing.visit(arg) for arg in funcCall.params])
            else:
                self.retVal = funcDecl()
        else:
            # user-defined function
            if funcDecl.params:
                for i in range(len(funcDecl.params)):
                    self.varlist[funcDecl.params[i].name] = passing.visit(
                        funcCall.params[i]
                    )
            self.visit(funcDecl.body)

    def visit_AstStatList(self, node: ast.AstStatList):
        for i in range(len(node.body)):
            self.visit(node.body[i])
            if self.retFlag:
                return

    def visit_AstRet(self, node: ast.AstRet):
        if node.expr:
            self.retVal = self.visit(node.expr)
        else:
            self.retVal = None
        self.retFlag = True


class ClassDefiner(Interpreter):
    name = ""
    memberlist = {}

    def __init__(self, node: Interpreter):
        self.name = node.name
        self.memberlist = node.memberlist
        self.varlist = node.varlist
        self.funclist = node.funclist

    def __init__(self, node: ast.AstClassDecl, params=None):
        # create class definition
        super().__init__()
        self.name = node.name
        self.memberlist = {}
        self.visit(node.body)

    def visit_AstFuncCall(self, callee: ast.AstFuncCall):
        calleeName = callee.name
        additonalVarlist = {
            'this': self,
        }
        # search in function list
        funcDecl = self.funclist.get(calleeName)
        classDecl = self.classlist.get(calleeName)
        if funcDecl:
            funcExecutor = FuncCaller(self, callee, funcDecl, additonalVarlist)
            return funcExecutor.retVal
        # search in class list
        elif classDecl:
            if classDecl.name == self.name:
                raise SyntaxError(f"Cannot create instance by it self '{self.name}'")
            newInstance = ClassDefiner(classDecl)
            return newInstance

    def visit_AstVarDecl(self, node: ast.AstVarDecl):
        varType = node.varType
        if varType:
            # explicit type
            typeclass = getattr(tc, "Type" + varType.capitalize(), None)
            if not typeclass:
                raise SyntaxError(f"Unknown type '{varType}'")
            if self.varlist.get(node.varname):
                if type(self.varlist[node.varname]) != typeclass:
                    raise SyntaxError(f"Member '{node.varname}' already exists")
            self.varlist[node.varname] = typeclass(self.visit(node.expr))
        else:
            # auto type
            var = self.visit(node.expr)
            node.varType = type(var).__name__.lower().replace("type", "")
            self.varlist[node.varname] = var
        self.memberlist[node.varname] = "var"

    def visit_AstFuncDecl(self, node: ast.AstFuncDecl):
        self.funclist[node.name] = node
        self.memberlist[node.name] = "func"

    def __str__(self) -> str:
        return f"class({self.name}, {self.memberlist})"
