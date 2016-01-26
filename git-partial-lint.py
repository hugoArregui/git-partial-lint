#!/usr/bin/env python3

import argparse
from glob import iglob
from itertools import chain

from lib.git import GitCmdInterface
from lib.rules import find_linter, LinterNotFound
from lib.partial_lint import PartialLint


def main():
    argparser = argparse.ArgumentParser(
        description='run linter only on the repo current changes')
    argparser.add_argument('--format', action='store', help='format')
    argparser.add_argument('rule', action='store', help='rule name')
    argparser.add_argument('files', action='store', metavar='file', nargs='+',
                           help='file or wildcard')
    args = argparser.parse_args()
    try:
        linter = find_linter(args.rule)
        git = GitCmdInterface()
        files = set(chain(*[iglob(f) for f in args.files]))
        out = PartialLint(git, linter).run(files, fmt=args.format)
        for l in out:
            print(l)
    except IOError:
        print('file not found')
    except LinterNotFound:
        print("No linter found")

if __name__ == '__main__':
    main()
