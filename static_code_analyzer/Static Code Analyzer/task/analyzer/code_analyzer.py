import argparse
import os

import code_checker


def parse_cli_arguments():
    parser = argparse.ArgumentParser(description="This program performs static code analysis on a given set of files.")
    parser.add_argument("filepath")
    args = parser.parse_args()
    return args.filepath


def make_code_checkers():
    code_checkers = [
        code_checker.CharactersNumberChecker(),
        code_checker.IndentationChecker(),
        code_checker.SemicolonChecker(),
        code_checker.InlineCommentChecker(),
        code_checker.ToDoChecker(),
        code_checker.BlankLinesChecker(),
        code_checker.SpacesAfterConstructChecker(),
        code_checker.ClassNameChecker(),
        code_checker.FunctionNameChecker(),
        code_checker.FunctionArgumentNameChecker(),
        code_checker.FunctionVariableNameChecker(),
        code_checker.MutableDefaultArgumentChecker(),
    ]
    return code_checkers


def check_file(filepath):
    code_checkers = make_code_checkers()
    errors = []
    for checker in code_checkers:
        checker(filepath)
        errors.extend(checker.errors)
    return errors


def print_errors(errors):
    errors.sort(key=lambda x: x[0])
    for _, message in errors:
        print(message)


def main():
    path = parse_cli_arguments()
    if os.path.isfile(path):
        errors = check_file(path)
        print_errors(errors)
    else:
        for (root, dirs, files) in os.walk(path, topdown=True):
            files = sorted(files)
            for name in files:
                errors = check_file(filepath=os.path.join(root, name))
                print_errors(errors)


main()
