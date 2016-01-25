#!/bin/python

import argparse

from lib.git import GitInterface
from lib.rules import find_linter, LinterNotFound

def run_linter(linter, f):
    git = GitInterface()
    current_brach = git.current_brach()
    is_new_file = not git.is_in_git("{:s}:{:s}".format(current_brach, f))

    linter_output = linter.run(f)

    blame = git.blame_file(f) if not is_new_file else None
    out = []
    for error in linter_output:
        if is_new_file or (linter.error_linenum(error) in blame):
            s = linter.format_error(error)
            out.append(s)
    return out

def main():
    argparser = argparse.ArgumentParser(
        description='run linter only on the repo current changes')
    argparser.add_argument('rule', action='store', help='rule name')
    argparser.add_argument('filename', action='store', help='filename')
    args = argparser.parse_args()
    try:
        linter = find_linter(args.rule)
        out = run_linter(linter, args.filename)
        for l in out:
            print(l)
    except LinterNotFound:
        print("No linter found")

if __name__ == '__main__':
    main()