import ast
import re
from string import Template

SNAKE_CASE = re.compile(r'([a-z0-9])+(_[a-z0-9]+)*')


class FunctionArgumentNameChecker(ast.NodeVisitor):
    MESSAGE_TEMPLATE = Template("S010 Argument name '$arg_name' should be written in snake_case")

    def __init__(self):
        self.errors = []

    def visit_FunctionDef(self, node):
        for arg in node.args.args:
            if not (re.match(SNAKE_CASE, arg.arg)):
                message = self.MESSAGE_TEMPLATE.substitute(arg_name=arg.arg)
                self.errors.append((node.lineno, message))
        self.generic_visit(node)


class FunctionVariableNameChecker(ast.NodeVisitor):

    def __init__(self):
        self.errors = []

    def visit_FunctionDef(self, node):
        checker = AssignmentChecker()
        for body_node in node.body:
            checker.visit(body_node)
        self.generic_visit(node)
        self.errors.extend(checker.errors)


class AssignmentChecker(ast.NodeVisitor):
    MESSAGE_TEMPLATE = Template("S011 Variable name '$var_name' should be written in snake_case")

    def __init__(self):
        self.errors = []

    def visit_Assign(self, node):
        for target in node.targets:
            if not (isinstance(target, ast.Attribute)) and not (re.match(SNAKE_CASE, target.id)):
                message = self.MESSAGE_TEMPLATE.substitute(var_name=target.id)
                self.errors.append((node.lineno, message))
        self.generic_visit(node)


class MutableDefaultArgumentChecker(ast.NodeVisitor):
    MESSAGE_TEMPLATE = "S012 The default argument value is mutable."

    def __init__(self):
        self.errors = []

    def visit_FunctionDef(self, node):
        if any(isinstance(default, ast.List) for default in node.args.defaults):
            self.errors.append((node.lineno, self.MESSAGE_TEMPLATE))
        self.generic_visit(node)
