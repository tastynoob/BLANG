import lang
from abc import ABC
import json


class AstNode:
    type = None

    def __str__(self):
        return f'{self.type}'

    def replace(self, node):
        self = node


class AstProgram(AstNode):
    type = 'Program'
    body = None

    def __init__(self, body):
        self.body = body

    def __str__(self):
        return f'{self.type}({self.body})'

    def to_json(self):
        return json.dumps({'type': self.type, 'body': self.body.to_json()}, indent=4)


class AstStatList(AstNode):
    type = 'StatList'
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
        return f'{self.type}({[str(x) for x in self.body]})'

    def to_json(self):
        return {'type': self.type, 'body': [x.to_json() for x in self.body]}


class AstParamsList(AstNode):
    type = 'ParamsList'
    params = []

    def __init__(self, params, next=None):
        if type(params) == AstParamsList:
            self.params = params.params
        else:
            self.params = [params]
        if next:
            self.params.append(next)

    def __str__(self):
        raise NotImplementedError

    def to_json(self):
        raise NotImplementedError


class AstFuncDecl(AstNode):
    type = 'FuncDecl'
    name = None
    params = None
    body = None

    def __init__(self, name, body, params=None):
        self.name = name
        self.params = params
        self.body = body

    def __str__(self):
        if self.params:
            return f'{self.type}({self.name}, {[str(x) for x in self.params]}, {self.body})'
        else:
            return f'{self.type}({self.name}, {self.body})'

    def to_json(self):
        if self.params:
            return {
                'type': self.type,
                'name': self.name,
                'params': [param.to_json() for param in self.params],
                'body': self.body.to_json(),
            }
        else:
            return {
                'type': self.type,
                'name': self.name,
                'params': 'no params',
                'body': self.body.to_json(),
            }


class AstRet(AstNode):
    type = 'Ret'
    expr = None

    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f'{self.type}({self.expr})'

    def to_json(self):
        return {'type': self.type, 'expr': self.expr.to_json()}


class AstVarDecl(AstNode):
    type = 'VarDecl'
    varname = None
    expr = None
    varType = None

    def __init__(self, name, expr, varType=None):
        self.varname = name
        self.expr = expr
        self.varType = varType

    def __str__(self):
        return f'{self.type}({self.name}, {self.expr})'

    def to_json(self):
        if self.varType:
            return {
                'type': self.type,
                'varname': self.varname,
                'varType': self.varType,
                'expr': self.expr.to_json(),
            }
        else:
            return {
                'type': self.type,
                'varname': self.varname,
                'varType': 'auto type',
                'expr': self.expr.to_json(),
            }


class AstCallParamsList(AstNode):
    type = 'CallParamsList'
    params = []

    def __init__(self, params, next=None):
        if type(params) == AstCallParamsList:
            self.params = params.params
        else:
            self.params = [params]
        if next:
            self.params.append(next)

    def __str__(self):
        raise NotImplementedError

    def to_json(self):
        raise NotImplementedError


class AstFuncCall(AstNode):
    type = 'FuncCall'
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
        return f'{self.type}({self.name}, {[str(x) for x in self.params]})'

    def to_json(self):
        if self.params:
            return {
                'type': self.type,
                'name': self.name,
                'params': [x.to_json() for x in self.params],
            }
        else:
            return {'type': self.type, 'name': self.name}


class AstField(AstNode):
    type = 'Field'
    name = None

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.type}({self.name})'

    def to_json(self):
        return {'type': self.type, 'name': self.name}


class AstIf(AstNode):
    type = 'If'
    condition = None
    then = None
    else_ = None

    def __init__(self, condition, then, else_=None):
        self.condition = condition
        self.then = then
        self.else_ = else_

    def __str__(self):
        return f'{self.type}({self.condition}, {self.then}, {self.else_})'

    def to_json(self):
        if self.else_:
            return {
                'type': self.type,
                'condition': self.condition.to_json(),
                'then': self.then.to_json(),
                'else': self.else_.to_json(),
            }
        else:
            return {
                'type': self.type,
                'condition': self.condition.to_json(),
                'then': self.then.to_json(),
            }


class AstWhile(AstNode):
    type = 'While'
    condition = None
    body = None

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __str__(self):
        return f'{self.type}({self.condition}, {self.body})'

    def to_json(self):
        return {
            'type': self.type,
            'condition': self.condition.to_json(),
            'body': self.body.to_json(),
        }


class AstAssign(AstNode):
    type = 'Assign'
    field = None
    expr = None

    def __init__(self, field, expr):
        self.field = field
        self.expr = expr

    def __str__(self):
        return f'{self.type}({self.field}, {self.expr})'

    def to_json(self):
        return {
            'type': self.type,
            'field': self.field.to_json(),
            'expr': self.expr.to_json(),
        }


class AstBinaryOper(AstNode):
    type = 'BinaryOper'
    operator = None
    left = None
    right = None

    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __str__(self):
        return f'{self.type}({self.operator}, {self.left}, {self.right})'

    def to_json(self):
        return {
            'type': self.type,
            'operator': self.operator,
            'left': self.left.to_json(),
            'right': self.right.to_json(),
        }


class AstConst(AstNode):
    type = 'Const'
    value = None

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.type}({self.value})'

    # to json
    def to_json(self):
        return {'type': self.type, 'value': self.value.to_json()}


class AstEnd(AstNode):
    type = 'End'

    def __str__(self):
        raise SyntaxError

    def to_json(self):
        raise SyntaxError
