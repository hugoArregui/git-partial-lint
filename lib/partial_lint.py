from os import path


class PartialLint:

    def __init__(self, git, linter):
        self.git = git
        self.linter = linter
        self.blames = {}
        self.current_brach = git.current_brach()

    def run(self, fs, fmt=None):
        out = []
        for f in set(fs) & self.git.modified_files():
            if not self._file_exists(f):
                raise IOError

            for error in self.linter.run(f):
                if self._is_relevant(error):
                    s = self.linter.format_error(error, fmt=fmt)
                    if len(fs) > 1:
                        s = f + ':' + s
                    out.append(s)
        return out

    def _is_relevant(self, error):
        f = error['file']
        if f not in self.blames:
            r = self.blames[f] = self._is_file_versioned(f) and self._blame(f)
        else:
            r = self.blames[f]
        return r is False or error['linenum'] in r

    def _is_file_versioned(self, f):
        return self.git.is_file_in_git(self.current_brach, f)

    def _blame(self, f):
        return self.git.blame_file(f)

    def _file_exists(self, f):
        return path.exists(f)
