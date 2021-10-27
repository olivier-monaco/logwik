from codecs import open
from os.path import abspath, dirname, join
from setuptools import setup, find_packages

ROOT_DIR = dirname(abspath(__file__))

__version__ = None
exec(open(join(ROOT_DIR, 'src', 'logwik', 'version.py')).read())

with open(join(ROOT_DIR, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='logwik',
    version=__version__,
    description='',
    long_description=long_description,
    author='Olivier Monaco',
    author_email='olivier@yowik.com',
    license='BSD',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'mariadb',
        'ua-parser',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'logwik=logwik.tool:main',
            'logwik-rslg=logwik.rsyslog:main',
        ],
    },
)
