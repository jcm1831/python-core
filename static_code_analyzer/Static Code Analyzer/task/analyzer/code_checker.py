import ast
import re
from abc import ABC, abstractmethod
from string import Template

import ast_visitors


def make_annotated_error(filepath: str, line_number: int, message: str) -> str:
    return f"{filepath}: Line {line_number}: {message}"


class CodeChecker(ABC):

    def __init__(self):
        self.errors = []

    @abstractmethod
    def __call__(self, filepath: str) -> None:
        raise NotImplementedError()

    def _add_error(self, line_number: int, message: str) -> None:
        self.errors.append((line_number, message))


class CharactersNumberChecker(CodeChecker):
    MESSAGE_TEMPLATE = 'S001 Line is too long'

    def __call__(self, filepath: str) -> None:
        with open(filepath, mode='r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.rstrip('\n')  # remove newline character
                if len(line) > 79:
                    error = make_annotated_error(filepath, line_number, self.MESSAGE_TEMPLATE)
                    self._add_error(line_number, error)


class IndentationChecker(CodeChecker):
    MESSAGE_TEMPLATE = 'S002 Indentation is not a multiple of four'

    def __call__(self, filepath: str) -> None:
        with open(filepath, mode='r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.rstrip('\n')  # remove newline character
                leading_whitespace = len(line) - len(line.lstrip())
                if leading_whitespace % 4 != 0:
                    error = make_annotated_error(filepath, line_number, self.MESSAGE_TEMPLATE)
                    self._add_error(line_number, error)


class SemicolonChecker(CodeChecker):
    MESSAGE_TEMPLATE = 'S003 Unnecessary semicolon after a statement'

    def __call__(self, filepath: str) -> None:
        with open(filepath, mode='r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.rstrip('\n')  # remove newline character
                self._check_line(line_number, line, filepath)

    def _check_line(self, line_number: int, line: str, filepath: str) -> None:
        if '#' not in line:
            line = line.rstrip()
            if len(line) > 0 and line[-1] == ';':
                error = make_annotated_error(filepath, line_number, self.MESSAGE_TEMPLATE)
                self._add_error(line_number, error)
        else:
            statement, comment = line.split(sep='#', maxsplit=1)
            return self._check_line(line_number, statement, filepath)


class InlineCommentChecker(CodeChecker):
    MESSAGE_TEMPLATE = 'S004 At least two spaces required before inline comments'

    def __call__(self, filepath: str) -> None:
        with open(filepath, mode='r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.rstrip('\n')  # remove newline character
                if '#' in line:
                    pattern = re.compile(r'.* {2}#.*')
                    match = re.search(pattern, line)
                    if not match and line[0] != '#':
                        error = make_annotated_error(filepath, line_number, self.MESSAGE_TEMPLATE)
                        self._add_error(line_number, error)


class ToDoChecker(CodeChecker):
    MESSAGE_TEMPLATE = 'S005 TODO found'
    PATTERN = re.compile(r'.*# .*todo.*', flags=re.IGNORECASE)

    def __call__(self, filepath: str) -> None:
        with open(filepath, mode='r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.rstrip('\n')  # remove newline character
                if re.search(self.PATTERN, line):
                    error = make_annotated_error(filepath, line_number, self.MESSAGE_TEMPLATE)
                    self._add_error(line_number, error)


class BlankLinesChecker(CodeChecker):
    MESSAGE_TEMPLATE = 'S006 More than two blank lines used before this line'
    line_counter = 0

    def __call__(self, filepath: str) -> None:
        with open(filepath, mode='r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.rstrip('\n')  # remove newline character
                if len(line) == 0:
                    BlankLinesChecker.line_counter += 1
                else:
                    if BlankLinesChecker.line_counter > 2:
                        error = make_annotated_error(filepath, line_number, self.MESSAGE_TEMPLATE)
                        self._add_error(line_number, error)
                    BlankLinesChecker.line_counter = 0


class SpacesAfterConstructChecker(CodeChecker):
    MESSAGE_TEMPLATE = Template('S007 Too many spaces after $construct_name')

    def __call__(self, filepath: str) -> None:
        with open(filepath, mode='r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.rstrip('\n')  # remove newline character
                if 'def' in line or 'class' in line:
                    pattern = re.compile(r'((class)|(def)) {2,}(.+):')
                    if match := re.search(pattern, line):
                        message = self.MESSAGE_TEMPLATE.substitute(construct_name=match.group(1))
                        error = make_annotated_error(filepath, line_number, message)
                        self._add_error(line_number, error)


class ClassNameChecker(CodeChecker):
    MESSAGE_TEMPLATE = Template("S008 Class name '$class_name' should be written in CamelCase")

    def __call__(self, filepath: str) -> None:
        with open(filepath, mode='r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.rstrip('\n')  # remove newline character
                if 'class' in line:
                    pattern = re.compile(r'class ([a-z]\w*)+(\(([a-z]\w*)+\))?:')
                    if match := re.search(pattern, line):
                        message = self.MESSAGE_TEMPLATE.substitute(class_name=match.group(1))
                        error = make_annotated_error(filepath, line_number, message)
                        self._add_error(line_number, error)


class FunctionNameChecker(CodeChecker):
    MESSAGE_TEMPLATE = Template("S009 Function name '$function_name' should be written in snake_case")

    def __call__(self, filepath: str) -> None:
        with open(filepath, mode='r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.rstrip('\n')  # remove newline character
                if 'def' in line:
                    pattern = re.compile(r'def ([A-Z]\w*)_*\(.*\):')
                    if match := re.search(pattern, line):
                        message = self.MESSAGE_TEMPLATE.substitute(function_name=match.group(1))
                        error = make_annotated_error(filepath, line_number, message)
                        self._add_error(line_number, error)


class FunctionArgumentNameChecker(CodeChecker):
    def __call__(self, filepath: str) -> None:
        with open(filepath, mode='r', encoding='utf-8') as file:
            checker = ast_visitors.FunctionArgumentNameChecker()
            checker.visit(node=ast.parse(file.read()))
            for line_number, error_message in checker.errors:
                error = make_annotated_error(filepath, line_number, error_message)
                self._add_error(line_number, error)


class FunctionVariableNameChecker(CodeChecker):
    def __call__(self, filepath: str) -> None:
        with open(filepath, mode='r', encoding='utf-8') as file:
            checker = ast_visitors.FunctionVariableNameChecker()
            checker.visit(node=ast.parse(file.read()))
            for line_number, error_message in checker.errors:
                error = make_annotated_error(filepath, line_number, error_message)
                self._add_error(line_number, error)


class MutableDefaultArgumentChecker(CodeChecker):
    def __call__(self, filepath: str) -> None:
        with open(filepath, mode='r', encoding='utf-8') as file:
            checker = ast_visitors.MutableDefaultArgumentChecker()
            checker.visit(node=ast.parse(file.read()))
            for line_number, error_message in checker.errors:
                error = make_annotated_error(filepath, line_number, error_message)
                self._add_error(line_number, error)
