from subprocess import run, PIPE


class LinterNotFound(RuntimeError):
    pass


class Rule:

    def __init__(self, name, fmt):
        self.name = name
        self.fmt = fmt

    def run(self, f):
        raise NotImplementedError

    def _run(self, cmd):
        return run(cmd, stdout=PIPE).stdout.decode('utf-8').splitlines()

    def _make_error(self, f, linenum, *, colnum=None, type=None, err=None,
                    desc=None):
        where = str(linenum)
        if colnum:
            where += ':' + str(colnum)
        return {
            'file': f,
            'linenum': linenum,
            'colnum': colnum,
            'type': type,
            'err': err,
            'where': where,
            'desc': desc
        }

    def format_error(self, error, multiple_files, fmt=None):
        r = '{file}: ' if multiple_files else ''
        r += fmt or self.fmt
        return r.format(**error)


class Eslint(Rule):
    name = 'eslint'
    fmt = "{where:>8} {type:>7} {desc:>50} {err}"

    def __init__(self):
        Rule.__init__(self, Eslint.name, Eslint.fmt)

    def run(self, f):
        out = self._run(["eslint", f])
        r = []
        if len(out) > 0:  # TODO: revisar el output cuando no hay errores
            for line in out[1:-2]:
                fields = [f.strip() for f in line.split()]
                linenum, colnum = map(int, fields[0].split(':'))
                r.append(self._make_error(f, linenum,
                                          colnum=colnum,
                                          type=fields[1],
                                          err=fields[-1],
                                          desc=" ".join(fields[2:-1])))
        return r


class Flake8(Rule):
    name = 'flake8'
    fmt = '{where:>8} {err}'

    def __init__(self):
        Rule.__init__(self, Flake8.name, Flake8.fmt)

    def run(self, f):
        out = self._run(["flake8", f])
        r = []
        for line in out:
            fields = [f.strip() for f in line.split(':')]
            linenum, colnum = map(int, fields[1:3])
            r.append(self._make_error(f, linenum, colnum=colnum,
                                      err=fields[-1]))
        return r


class Rubocop(Rule):
    name = 'rubocop'
    fmt = "{where:>8} [{type}] {err}"

    def __init__(self):
        Rule.__init__(self, Rubocop.name, Rubocop.fmt)

    def run(self, f):
        out = self._run(['rubocop', '-f', 's', f])
        r = []
        if len(out) > 3:
            for line in out[1:-2]:
                fields = [f.strip() for f in line.split(':')]
                linenum, colnum = map(int, fields[1:3])
                r.append(self._make_error(f, linenum,
                                          type=fields[0],
                                          colnum=colnum,
                                          err=fields[-1]))
        return r


linters = [Eslint(), Flake8(), Rubocop()]


def find_linter(name, linters=linters):
    for linter in linters:
        if linter.name == name:
            return linter
    raise LinterNotFound
