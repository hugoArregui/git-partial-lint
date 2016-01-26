from os import path


def run_partial_lint(git, linter, fs, fmt=None):
    current_brach = git.current_brach()
    blames = {}

    def is_relevant(f, error):
        if f not in blames:
            is_new_file = not git.is_file_git(current_brach, f)
            r = blames[f] = git.blame_file(f) if not is_new_file else None
        else:
            r = blames[f]
        print(r.keys())
        return r is None or error['linenum'] in r

    out = []
    for f in fs:
        if not path.exists(f):
            raise IOError

        for error in linter.run(f):
            print(error)
            if is_relevant(f, error):
                s = linter.format_error(error, fmt=fmt)
                if len(fs) > 1:
                    s = f + ':' + s
                out.append(s)
    return out
