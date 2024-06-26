import lang.astnode as ast
from abc import ABC


class NodeVisitor(ABC):
    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        node = visitor(node)
        return node

    def generic_visit(self, node):
        child = node.getChild()
        for i in range(len(child)):
            self.visit(child[i])
        return node


class Optimizer(NodeVisitor):
    def visit_AstProgram(self, node: ast.AstProgram):
        node.body = self.visit(node.body)
        return node

    def visit_AstStatList(self, node: ast.AstStatList):
        for i in range(len(node.body)):
            node.body[i] = self.visit(node.body[i])
        return node

    def visit_AstAssign(self, node: ast.AstAssign):
        node.expr = self.visit(node.expr)
        return node

    def visit_AstIf(self, node: ast.AstIf):
        node.condition = self.visit(node.condition)
        node.then = self.visit(node.then)
        if node.else_:
            node.else_ = self.visit(node.else_)
        return node

    def visit_AstWhile(self, node: ast.AstWhile):
        node.condition = self.visit(node.condition)
        node.body = self.visit(node.body)
        return node

    def visit_AstVarDecl(self, node: ast.AstVarDecl):
        node.expr = self.visit(node.expr)
        return node

    def visit_AstAssign(self, node: ast.AstAssign):
        node.expr = self.visit(node.expr)
        return node

    def visit_AstBinaryOper(self, node: ast.AstBinaryOper):
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)
        if type(node.left) == ast.AstConst and type(node.right) == ast.AstConst:
            if node.operator == '+':
                node = ast.AstConst(node.left.value + node.right.value)
            elif node.operator == '-':
                node = ast.AstConst(node.left.value - node.right.value)
            elif node.operator == '*':
                node = ast.AstConst(node.left.value * node.right.value)
            elif node.operator == '/':
                node = ast.AstConst(node.left.value / node.right.value)
            elif node.operator == '<':
                node = ast.AstConst(node.left.value < node.right.value)
            elif node.operator == '>':
                node = ast.AstConst(node.left.value > node.right.value)
            elif node.operator == '<=':
                node = ast.AstConst(node.left.value <= node.right.value)
            elif node.operator == '>=':
                node = ast.AstConst(node.left.value >= node.right.value)
            elif node.operator == '==':
                node = ast.AstConst(node.left.value == node.right.value)
            elif node.operator == '!=':
                node = ast.AstConst(node.left.value != node.right.value)
            else:
                return node
        return node

    def visit_AstRet(self, node: ast.AstRet):
        if node.expr:
            node.expr = self.visit(node.expr)
        return node

    def visit_AstFuncCall(self, node: ast.AstFuncCall):
        for i in range(len(node.params)):
            node.params[i] = self.visit(node.params[i])
        return node
