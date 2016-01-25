from subprocess import run, PIPE


class LinterNotFound(RuntimeError):
    pass


class Eslint:
    name = 'eslint'

    def run(self, f):
        out = run(["eslint", f],
                  stdout=PIPE).stdout.decode('utf-8').splitlines()
        return out[2:-3]

    def error_linenum(self, error):
        return int(error.split(':')[0])

    def format_error(self, error):
        fields = [f.strip() for f in error.split(':')]
        where, type = fields[:2]
        desc = " ".join(fields[2:-1])
        err = fields[-1]
        return "{:>8s} {:>7s} {:>50s} {:s}".format(where, type, desc, err)


class Flake8:
    name = 'flake8'

    def run(self, f):
        return run(["flake8", f],
                   stdout=PIPE).stdout.decode('utf-8').splitlines()

    def error_linenum(self, error):
        return int(error.split(':')[1])

    def format_error(self, error):
        fields = [f.strip() for f in error.split(':')]
        where = "{:s}:{:s}".format(fields[1], fields[2])
        err = fields[-1]
        return "{:>8s} {:s}".format(where, err)


class Rubocop:
    name = 'rubocop'

    def run(self, f):
        out = run(['rubocop', '-f', 's', f],
                   stdout=PIPE).stdout.decode('utf-8').splitlines()
        return out[1:-2] if len(out) > 3 else []

    def error_linenum(self, error):
        return int(error.split(':')[1])

    def format_error(self, error):
        fields = [f.strip() for f in error.split(':')]
        where = "{:s}:{:s}".format(fields[1], fields[2])
        type = fields[0]
        err = fields[-1]
        return "{:>8s} [{:s}] {:s}".format(where, type, err)


linters = [Eslint(), Flake8(), Rubocop()]


def find_linter(name):
    for linter in linters:
        if linter.name == name:
            return linter
    raise LinterNotFound
