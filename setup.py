import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='otus-search',
    version='1.0',
    packages=['otus_search'],
    include_package_data=True,
    license='GNU General Public License v3.0',
    description='Utility for crawling internet sites and searching/saving URLs',
    long_description='README.md',
    url='https://github.com/antonklyukin/otus-search',
    author='Anton Klyukin',
    author_email='antonklyukin@gmail.com',
    keywords=['url', 'crawler', 'otus', 'parser', 'console'],
    classifiers=[],
    entry_points={},
)