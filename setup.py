from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


with open("requirements.txt") as f:
    required = list(f)

with open("README.md") as f:
    description = f.read()


setup(
    name="washr",
    packages=find_packages(exclude=["tests"]),
    test_require=["pytest"],
    install_requires=required,
    cmdclass={'test': PyTest},
    description=description
)
