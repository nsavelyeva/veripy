#!/usr/local/bin/python

import sys
from comment import Comment
from scanners import Lint, Sec, Cc, Mi, Hal, Raw, Cov


if __name__ == '__main__':
    errors = []

    try:
        scan, path, options, covgate, comment, update, token = sys.argv[1:]
    except IndexError:
        sys.exit('Error: insufficient number of arguments provided: %s, but need 7' % (len(sys.argv)-1))

    scanner = None
    if scan == "lint":
        scanner = Lint(path or '.', options or '')
    elif scan == "sec":
        scanner = Sec(path or '.', options or '--recursive')
    elif scan == "cc":
        scanner = Cc(path or '.', options or '-nc')
    elif scan == "mi":
        scanner = Mi(path or '.', options or '--min=B --show --sort')
    elif scan == "hal":
        scanner = Hal(path or '.', options or '')
    elif scan == "raw":
        scanner = Raw(path or '.', options or '--summary')
    elif scan == "cov":
        scanner = Cov(path or '.', options or '--verbose', int(covgate) if covgate else 0)

    command, code, output = scanner.scan()
    if code != 0:
        errors.append(f'Execution of "{command}" failed, captured output is:\n{output}')

    if comment:
        body = scanner.prepare_comment(code, output)  # always non-empty
        comm = Comment(token, scanner.name.upper())
        num = comm.find()

        if update and num != 0:
            ok, content = comm.update(body, num)
        else:
            ok, content = comm.create(body)
        if not ok:
            errors.append(content)

    sys.exit('\n'.join(errors) or None)
