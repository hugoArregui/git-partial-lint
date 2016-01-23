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
        return error.split(':')[0]

    def format_error(self, error):
        fields = [f.strip() for f in error.split(':')]
        where, type = fields[:2]
        desc = " ".join(fields[2:-1])
        err = fields[-1]
        return "{:>8s} {:>7s} {:>50s} {:s}".format(where, type, desc, err)

linters = [Eslint()]

def find_linter(name):
    for linter in linters:
        if linter.name == name:
            return linter
    raise LinterNotFound
