#!/usr/bin/env python3

import argparse

from lib.git import GitCmdInterface
from lib.rules import find_linter, LinterNotFound
from lib.partial_lint import run_partial_lint


def main():
    argparser = argparse.ArgumentParser(
        description='run linter only on the repo current changes')
    argparser.add_argument('--format', action='store', help='format')
    argparser.add_argument('rule', action='store', help='rule name')
    argparser.add_argument('filename', action='store', help='filename')
    args = argparser.parse_args()
    try:
        linter = find_linter(args.rule)
        git = GitCmdInterface()
        out = run_partial_lint(git, linter, args.filename, fmt=args.format)
        for l in out:
            print(l)
    except IOError:
        print('file not found')
    except LinterNotFound:
        print("No linter found")

if __name__ == '__main__':
    main()
