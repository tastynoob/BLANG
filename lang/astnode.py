import lang
from abc import ABC
import json


class AstNode(ABC):
    type = None

    def __str__(self):
        raise NotImplementedError("should not be called")

    def to_json(self):
        raise NotImplementedError("should not be called")

    def getChild(self):
        return []


class AstProgram(AstNode):
    type = "Program"
    body = None

    def __init__(self, body):
        self.body = body

    def __str__(self):
        return f"{self.type}({self.body})"

    def to_json(self):
        return json.dumps({"type": self.type, "body": self.body.to_json()}, indent=4)

    def getChild(self):
        return [self.body]


class AstStatList(AstNode):
    type = "StatList"
    body = []

    def __init__(self, body=None, next=None):
        self.body = []
        if body:
            if type(body) == AstStatList:
                self.body = body.body
            else:
                self.body = [body]
            if next:
                self.body.append(next)
        else:
            if next:
                self.body.append(next)

    def __str__(self):
        return f"{self.type}({[str(x) for x in self.body]})"

    def to_json(self):
        return {"type": self.type, "body": [x.to_json() for x in self.body]}

    def getChild(self):
        return self.body


class AstClassDecl(AstNode):
    type = "ClassDecl"
    name = None
    body = None

    def __init__(self, name, body):
        self.name = name
        self.body = body

    def __str__(self):
        return f"{self.type}({self.name}, {self.body})"

    def to_json(self):
        return {"type": self.type, "name": self.name, "body": self.body.to_json()}

    def getChild(self):
        return [self.body]


class AstMbrSel(AstNode):
    type = "MbrSel"
    object = None
    member = None

    def __init__(self, object, member):
        self.object = object
        self.member = member

    def __str__(self):
        return f"{self.type}({self.object}, {self.member})"

    def to_json(self):
        return {
            "type": self.type,
            "object": self.object.to_json(),
            "member": self.member.to_json(),
        }


class AstParamsList(AstNode):
    type = "ParamsList"
    params = []

    def __init__(self, params, next=None):
        if type(params) == AstParamsList:
            self.params = params.params
        else:
            self.params = [params]
        if next:
            self.params.append(next)

    def __str__(self):
        raise NotImplementedError("should not be called")

    def to_json(self):
        raise NotImplementedError("should not be called")


class AstFuncDecl(AstNode):
    type = "FuncDecl"
    name = None
    params = None
    body = None

    def __init__(self, name, body, params=None):
        self.name = name
        self.params = params
        self.body = body

    def __str__(self):
        if self.params:
            return f"{self.type}({self.name}, {[str(x) for x in self.params]}, {self.body})"
        else:
            return f"{self.type}({self.name}, {self.body})"

    def to_json(self):
        if self.params:
            return {
                "type": self.type,
                "name": self.name,
                "params": [param.to_json() for param in self.params],
                "body": self.body.to_json(),
            }
        else:
            return {
                "type": self.type,
                "name": self.name,
                "params": "no params",
                "body": self.body.to_json(),
            }

    def getChild(self):
        return [self.body]


class AstRet(AstNode):
    type = "Ret"
    expr = None

    def __init__(self, expr=None):
        self.expr = expr

    def __str__(self):
        return f"{self.type}({self.expr})"

    def to_json(self):
        if self.expr:
            return {"type": self.type, "expr": self.expr.to_json()}
        else:
            return {"type": self.type, "expr": "none"}

    def getChild(self):
        if self.expr:
            return [self.expr]
        else:
            return []


class AstVarDecl(AstNode):
    type = "VarDecl"
    varname = None
    expr = None
    varType = None

    def __init__(self, name, expr, varType=None):
        self.varname = name
        self.expr = expr
        self.varType = varType

    def __str__(self):
        return f"{self.type}({self.varname}, {self.expr})"

    def to_json(self):
        if self.varType:
            return {
                "type": self.type,
                "varname": self.varname,
                "varType": self.varType,
                "expr": self.expr.to_json(),
            }
        else:
            return {
                "type": self.type,
                "varname": self.varname,
                "varType": "auto type",
                "expr": self.expr.to_json(),
            }

    def getChild(self):
        return [self.expr]


class AstCallParamsList(AstNode):
    type = "CallParamsList"
    params = []

    def __init__(self, params, next=None):
        if type(params) == AstCallParamsList:
            self.params = params.params
        else:
            self.params = [params]
        if next:
            self.params.append(next)

    def __str__(self):
        raise NotImplementedError("should not be called")

    def to_json(self):
        raise NotImplementedError("should not be called")


class AstFuncCall(AstNode):
    type = "FuncCall"
    name = None
    params = []

    def __init__(self, name, params=None):
        self.name = name
        self.params = []
        if params:
            if type(params) == AstCallParamsList:
                self.params = params.params
            else:
                self.params = [params]

    def __str__(self):
        return f"{self.type}({self.name}, {[str(x) for x in self.params]})"

    def to_json(self):
        if self.params:
            return {
                "type": self.type,
                "name": self.name,
                "params": [x.to_json() for x in self.params],
            }
        else:
            return {"type": self.type, "name": self.name}

    def getChild(self):
        return self.params


class AstField(AstNode):
    type = "Field"
    name = None

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.type}({self.name})"

    def to_json(self):
        return {"type": self.type, "name": self.name}


class AstIf(AstNode):
    type = "If"
    condition = None
    then = None
    else_ = None

    def __init__(self, condition, then, else_=None):
        self.condition = condition
        self.then = then
        self.else_ = else_

    def __str__(self):
        return f"{self.type}({self.condition}, {self.then}, {self.else_})"

    def to_json(self):
        if self.else_:
            return {
                "type": self.type,
                "condition": self.condition.to_json(),
                "then": self.then.to_json(),
                "else": self.else_.to_json(),
            }
        else:
            return {
                "type": self.type,
                "condition": self.condition.to_json(),
                "then": self.then.to_json(),
            }

    def getChild(self):
        if self.else_:
            return [self.condition, self.then, self.else_]
        else:
            return [self.condition, self.then]


class AstWhile(AstNode):
    type = "While"
    condition = None
    body = None

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __str__(self):
        return f"{self.type}({self.condition}, {self.body})"

    def to_json(self):
        return {
            "type": self.type,
            "condition": self.condition.to_json(),
            "body": self.body.to_json(),
        }

    def getChild(self):
        return [self.condition, self.body]


class AstAssign(AstNode):
    type = "Assign"
    lvalue = None
    expr = None

    def __init__(self, lvalue, expr):
        self.lvalue = lvalue
        self.expr = expr

    def __str__(self):
        return f"{self.type}({self.lvalue}, {self.expr})"

    def to_json(self):
        return {
            "type": self.type,
            "lvalue": self.lvalue.to_json(),
            "expr": self.expr.to_json(),
        }

    def getChild(self):
        return [self.expr]


class AstIndex(AstNode):
    type = "Index"
    point = None
    index = None

    def __init__(self, point, index):
        self.point = point
        self.index = index

    def __str__(self):
        return f"{self.type}({self.point}, {self.index})"

    def to_json(self):
        return {
            "type": self.type,
            "point": self.point.to_json(),
            "index": self.index.to_json(),
        }


class AstUnaryOper(AstNode):
    type = "UnaryOper"
    operator = None
    expr = None

    def __init__(self, operator, expr):
        self.operator = operator
        self.expr = expr

    def __str__(self):
        return f"{self.type}({self.operator}, {self.expr})"

    def to_json(self):
        return {
            "type": self.type,
            "operator": self.operator,
            "expr": self.expr.to_json(),
        }

    def getChild(self):
        return [self.expr]


class AstBinaryOper(AstNode):
    type = "BinaryOper"
    operator = None
    left = None
    right = None

    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __str__(self):
        return f"{self.type}({self.operator}, {self.left}, {self.right})"

    def to_json(self):
        return {
            "type": self.type,
            "operator": self.operator,
            "left": self.left.to_json(),
            "right": self.right.to_json(),
        }

    def getChild(self):
        return [self.left, self.right]


class AstConst(AstNode):
    type = "Const"
    value = None

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.type}({self.value})"

    # to json
    def to_json(self):
        return {"type": self.type, "value": self.value.to_json()}


class AstEnd(AstNode):
    type = "End"
