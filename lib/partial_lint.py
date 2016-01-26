from os import path


def run_partial_lint(git, linter, f, fmt=None):
    if not path.exists(f):
        raise IOError
    current_brach = git.current_brach()
    is_new_file = not git.is_in_git("{:s}:{:s}".format(current_brach, f))

    linter_output = linter.run(f)

    blame = git.blame_file(f) if not is_new_file else None
    out = []
    for error in linter_output:
        if is_new_file or (error['linenum'] in blame):
            s = linter.format_error(error, fmt=fmt)
            out.append(s)
    return out
