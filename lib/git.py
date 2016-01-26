from subprocess import run, PIPE, CalledProcessError


class FileNotInGit(RuntimeError):
    pass


class GitCmdInterface:

    def current_brach(self):
        return self._r(['rev-parse', '--abbrev-ref', 'HEAD'])

    def rev_parse(self, o):
        return self._r(['rev-parse', o])

    def blame_file(self, f, only_new_lines=True):
        lines = self._r(['blame', '-s', '--show-name', f]).splitlines()
        return {
            int(line.split()[2][:-1]): line
            for line in lines
            if not only_new_lines or line.startswith('00000000')}

    def is_in_git(self, path):
        try:
            self.rev_parse(path)
            under_git = True
        except FileNotInGit:
            under_git = False
        return under_git

    def _r(self, cmd):
        try:
            x = run(['git'] + cmd, stdout=PIPE, stderr=PIPE, check=True)
            return x.stdout.decode('utf-8').strip()
        except CalledProcessError as e:
            err = e.stderr.decode('utf-8').strip()
            if 'exists on disk, but not in' in err:  # fragile!
                raise FileNotInGit
            else:
                raise e
