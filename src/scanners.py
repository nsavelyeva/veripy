import os
from engine import Scanner


class Lint(Scanner):
    def __init__(self, path='.', options=''):
        self.name = 'lint'
        self.description = 'performs code linting using [pylint](https://pylint.org)'
        self.command = f'pylint {options} {path}'  # pylint --rcfile=review/.pylintrc src'
        self.install('requirements.txt')


class Sec(Scanner):
    def __init__(self, path='.', options='--recursive'):
        self.name = 'sec'
        self.description = 'runs security scan using [bandit](https://bandit.readthedocs.io/en/latest/)'
        self.command = f'bandit {options} {path}'  # bandit --recursive --exclude=lib/tests lib


class Cc(Scanner):
    def __init__(self, path='.', options='-nc'):
        self.name = 'cc'
        self.description = 'measures [cyclomatic complexity](https://radon.readthedocs.io/en/latest/intro.html#cyclomatic-complexity) of code using `radon`'
        self.command = f'! radon cc {options} {path} | grep .'  # ! radon cc -nc lib | grep .


class Mi(Scanner):
    def __init__(self, path='.', options='--min=B --show --sort'):
        self.name = 'mi'
        self.description = 'measures [maintainability index](https://radon.readthedocs.io/en/latest/intro.html#maintainability-index) of code using `radon`'
        self.command = f'! radon mi {options} {path} | grep .'  # ! radon mi --min=B --show --sort --exclude="lib/tests/test_*.py" lib | grep .


class Hal(Scanner):
    def __init__(self, path='.', options=''):
        self.name = 'hal'
        self.description = 'calculates [Halstead metrics](https://radon.readthedocs.io/en/latest/intro.html#halstead-metrics) of code using `radon`'
        self.command = f'radon hal {options} {path}'  # radon hal lib


class Raw(Scanner):
    def __init__(self, path='.', options='--summary'):
        self.name = 'raw'
        self.description = 'collects [raw metrics](https://radon.readthedocs.io/en/latest/intro.html#raw-metrics) of code using `radon`'
        self.command = f'radon raw {options} {path}'  # radon raw --summary lib


class Cov(Scanner):
    def __init__(self, path='.', options='--verbose', covgate=0):
        self.name = 'cov'
        self.gate = covgate
        self.description = 'runs unit tests with code coverage using [nose2](https://docs.nose2.io/en/latest/)' + \
                           ' with [coverage plugin](https://docs.nose2.io/en/latest/plugins/coverage.html)' + \
                           ' and asserts the quality gate threshold (default is 0)'
        # nose2 --verbose --start-dir . --with-coverage --coverage-report=html --coverage=.
        # creates .coverage, coverage.xml and htmlcov folder
        self.command = f'nose2 {options} --start-dir {path} --with-coverage --coverage={path} ' + \
                       '--coverage-report=term --coverage-report=html --coverage-report=xml ' + \
                       '--coverage-config=/opt/veripy/coverage.conf'
        self.curdir = self.install('requirements.txt')
        self.make_htmlcov()

    # See release notes for versions 6.1, 6.2 and 6.3 about .gitignore file
    # at https://coverage.readthedocs.io/en/6.3/changes.html?highlight=gitignore#version-6-3-2022-01-25
    def make_htmlcov(self):
        name = 'htmlcov'
        if not os.path.isdir(name):
            os.mkdir(name)
        with open(os.path.join(name, '.gitignore'), 'w'):
            pass  # create an empty file


    def scan(self):
        cmd, ret, out = self.execute()
        msg = ''
        if 'FAILED (failures=' in out:
            msg = '### Unit tests execution failed.\n\n'
        elif '\n\nOK\n' in out:
            msg = '### Unit tests execution passed.\n\n'

        # The file coverage.xml is generated, its first two lines are as follows:
        # <?xml version="1.0" ?>
        # <coverage version="6.3" timestamp="1643190874644" lines-valid="831" lines-covered="0" line-rate="0" ...>
        path = os.path.join(self.curdir, 'coverage.xml')
        with open(path) as xml_file:
            stats = xml_file.readlines()[1]
        cov = 0
        for item in stats.split():
            if item.startswith('line-rate='):
                cov = float(item.split('=')[1].replace('"', '')) * 100.0
                break
        if cov < self.gate:
            ret = 1
            msg += '### Actual code coverage is %.2f%% - lower than %d%% (configured threshold)' % (cov, self.gate)
        else:
            msg += '### Actual code coverage is %.2f%% - meets the configured threshold of %d%%' % (cov, self.gate)
        self.description += f'._\n\n{msg}_'
        return cmd, ret, out
