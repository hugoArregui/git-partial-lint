import unittest
from unittest.mock import MagicMock

from lib.partial_lint import PartialLint


class PartialLintTest(unittest.TestCase):

    def setUp(self):
        self.git = MagicMock()
        self.git.current_brach = MagicMock(return_value='master')

        self.linter = MagicMock()

    def test_file_not_found(self):
        pl = PartialLint(self.git, self.linter)
        pl._file_exists = MagicMock(return_value=False)
        self.assertRaises(IOError, pl.run, ['lakdsjlkaj23123.rb'])

    def test_error_on_unversioned_file(self):
        f = 'main.js'
        errors = [{
            'file': f,
            'linenum': 10
        }]

        self.linter.run = MagicMock(return_value=errors)
        self.git.is_file_in_git = MagicMock(return_value=False)

        pl = PartialLint(self.git, self.linter)
        pl._file_exists = MagicMock(return_value=True)
        out = pl.run([f])
        self.assertEqual(len(out), 1)

    def test_error_on_new_change_in_versioned_file(self):
        f = 'main.js'
        errors = [{
            'file': f,
            'linenum': 10
        }]

        self.linter.run = MagicMock(return_value=errors)
        self.git.is_file_in_git = MagicMock(return_value=True)
        self.git.blame_file = MagicMock(return_value={10: MagicMock()})

        pl = PartialLint(self.git, self.linter)
        pl._file_exists = MagicMock(return_value=True)
        out = pl.run([f])
        self.assertEqual(len(out), 1)

    def test_error_on_old_change_in_versioned_file(self):
        f = 'main.js'
        errors = [{
            'file': f,
            'linenum': 10
        }]

        self.linter.run = MagicMock(return_value=errors)
        self.git.is_file_in_git = MagicMock(return_value=True)
        self.git.blame_file = MagicMock(return_value={})

        pl = PartialLint(self.git, self.linter)
        pl._file_exists = MagicMock(return_value=True)
        out = pl.run([f])
        self.assertEqual(len(out), 0)

if __name__ == '__main__':
    unittest.main()
