from subprocess import run, PIPE


class LinterNotFound(RuntimeError):
    pass


class Eslint:
    name = 'eslint'

    def run(self, f):
        out = run(["eslint", f],
                  stdout=PIPE).stdout.decode('utf-8').splitlines()
        r = []
        if len(out) > 5:
            for line in out[2:-3]:
                fields = [f.strip() for f in line.split(':')]
                r.append({
                    'file': f,
                    'linenum': int(fields[0]),
                    'type': fields[1],
                    'err': fields[-1],
                    'where': "{:s}".format(fields[0]),
                    'desc': " ".join(fields[2:-1])
                })
        return r

    def format_error(self, error):
        return "{where:>8} {type:>7} {desc:>50} {err}".format(**error)


class Flake8:
    name = 'flake8'

    def run(self, f):
        out = run(["flake8", f],
                  stdout=PIPE).stdout.decode('utf-8').splitlines()
        r = []
        for line in out:
            fields = [f.strip() for f in line.split(':')]
            r.append({
                'file': f,
                'linenum': int(fields[1]),
                'colnum': int(fields[2]),
                'err': fields[-1],
                'where': "{:s}:{:s}".format(fields[1], fields[2])
            })
        return r

    def format_error(self, error):
        return "{where:>8} {err}".format(**error)


class Rubocop:
    name = 'rubocop'

    def run(self, f):
        out = run(['rubocop', '-f', 's', f],
                  stdout=PIPE).stdout.decode('utf-8').splitlines()
        r = []
        if len(out) > 3:
            for line in out[1:-2]:
                fields = [f.strip() for f in line.split(':')]
                r.append({
                    'file': f,
                    'type': fields[0],
                    'linenum': int(fields[1]),
                    'colnum': int(fields[2]),
                    'err': fields[-1],
                    'where': "{:s}:{:s}".format(fields[1], fields[2])
                })
        return r

    def format_error(self, error):
        return "{where:>8} [{type}] {err}".format(**error)


linters = [Eslint(), Flake8(), Rubocop()]


def find_linter(name):
    for linter in linters:
        if linter.name == name:
            return linter
    raise LinterNotFound
