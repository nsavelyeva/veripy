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
    def __init__(self, path='.', options='--verbose --with-id', covgate=0):
        self.name = 'cov'
        self.description = 'runs unit tests with code coverage using [nose](https://nose.readthedocs.io/en/latest/)' + \
                           ' with [cover plugin](https://nose.readthedocs.io/en/latest/plugins/cover.html)' + \
                           ' and optionally asserts quality gate'
        self.command = f'nosetests {options} --with-coverage --cover-inclusive --cover-min-percentage={covgate} ' + \
                       f'--cover-package={path} --where {path}'  # nosetests --verbose --with-id --with-coverage --where lib/tests
        self.install('requirements.txt')
