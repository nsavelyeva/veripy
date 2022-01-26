import os
import sys
import subprocess


class Scanner:
    def __init__(self):
        self.name = ''
        self.description = ''
        self.command = ''

    def install(self, path):
        cmd, ret, pwd = self.execute('pwd', exit_on_failure=False)
        cmd, ret, ls = self.execute(f'ls -l .', exit_on_failure=False)
        print(f'Contents of current directory "{pwd}" is:\n{ls}')
        print('About to install Python dependencies')
        if os.path.isfile(path):
            print(f'Detected "{path}". Installing.')
            cmd, ret, out = self.execute(f'pip install --prefix=/usr/local --no-compile -r {path}', exit_on_failure=False)
            if ret:
                print(f'Command "{cmd}" exited with non-zero return code {ret} ' +
                      f'(unit tests may fail because of missing dependencies), captured output is:\n{out}')
            else:
                print('Successfully installed requirements.')
        else:
            print(f'Could not find "{path}" in the current directory "{pwd}", ' +
                  f'unit tests may fail because of missing dependencies.\nContents of current directory is:\n{ls}')
        return pwd

    def execute(self, cmd='', print_output=False, exit_on_failure=False, treat_non_empty_output_as_failure=False):
        if not cmd:
            cmd = self.command
        print(f'Running command:\n{cmd}')
        result = subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True)

        out = (result.stdout + result.stderr).strip()
        ret = 2 if result.stderr.strip() or (treat_non_empty_output_as_failure and out) else result.returncode
        if print_output:
            print(out)
        if ret != 0 and exit_on_failure:
            sys.exit(f'Execution of "{cmd}" failed, captured output is:\n{out}')
        return cmd, ret, out

    def scan(self):
        return self.execute()

    def format_output(self, status, emoji, content, wrap):
        result = f'## {emoji} Veripy check `{self.name.capitalize()}`: {status.upper()}\n\n' + \
                 f'_This check {self.description}._\n\n'
        if content:
            if wrap:
                content = f'\n```\n{content}\n```'
            if len(content) > 2048:
                content = 'Please expand "Details" below to see full information\n' + \
                          f"\n<details><summary><code>Details</code></summary>\n\n{content}\n\n</details>\n"
            result += f'\n\n{content}\n\n'
        return result

    def output_success(self, wrap=True):
        return self.format_output('PASS', ':white_check_mark:', '', wrap)

    def output_failure(self, content, wrap=True):
        return self.format_output('FAIL', ':warning:', content, wrap)

    def output_info(self, content, wrap=True):
        return self.format_output('INFO', ':information_source:', content, wrap)

    def prepare_comment(self, code, content, wrap=True):
        if code:
            return self.output_failure(content, wrap)
        if content:
            return self.output_info(content)
        return self.output_success()
