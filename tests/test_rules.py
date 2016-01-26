import unittest
from unittest.mock import MagicMock

from lib.rules import Flake8, Rubocop


class Flake8Test(unittest.TestCase):

    target = 'git.py'

    out = [
        "git.py:24:9: F841 local variable 'x' is assigned to but never used",
        "git.py:29:32: E202 whitespace before ')'"
    ]

    error24 = {
        'file': target,
        'linenum': 24,
        'colnum': 9,
        'err': "F841 local variable 'x' is assigned to but never used",
        'where': '24:9',
        'desc': None,
        'type': None,
    }

    error29 = {
        'file': target,
        'linenum': 29,
        'colnum': 32,
        'where': '29:32',
        'err': "E202 whitespace before ')'",
        'desc': None,
        'type': None,
    }

    def test_no_error(self):
        rule, r = self._run_with_output(Flake8(), self.target, [])
        self.assertEqual(r, [])

    def test_errors(self):
        rule, r = self._run_with_output(Flake8(), self.target, self.out)
        self.assertEqual(r[0], self.error24)
        self.assertEqual(r[1], self.error29)

    def _run_with_output(self, rule, f, output):
        rule._run = MagicMock(return_value=output)
        return rule, rule.run(f)


class RubocopTest(unittest.TestCase):

    target = 'buyer.rb'

    out = [
        "== buyer.rb ==",
        "C: 27:  7: Indent when as deep as case.",
        "C: 34: 13: Use the new Ruby 1.9 hash syntax.",
        "",
        "1 file inspected, 36 offenses detected"
    ]

    error27 = {
        'file': target,
        'linenum': 27,
        'colnum': 7,
        'err': "Indent when as deep as case.",
        'where': '27:7',
        'desc': None,
        'type': 'C'
    }

    error34 = {
        'file': target,
        'linenum': 34,
        'colnum': 13,
        'where': '34:13',
        'err': "Use the new Ruby 1.9 hash syntax.",
        'desc': None,
        'type': 'C'
    }

    def test_no_error(self):
        rule, r = self._run_with_output(Rubocop(), self.target, [])
        self.assertEqual(r, [])

    def test_errors(self):
        rule, r = self._run_with_output(Rubocop(), self.target, self.out)
        self.assertEqual(r[0], self.error27)
        self.assertEqual(r[1], self.error34)

    def _run_with_output(self, rule, f, output):
        rule._run = MagicMock(return_value=output)
        return rule, rule.run(f)

if __name__ == '__main__':
    unittest.main()
