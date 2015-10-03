from setuptools import setup, find_packages
import os

ROOT = os.path.dirname(os.path.realpath(__file__))


setup(
    name = 'weblib',
    version = '0.1.20',
    description = 'Set of tools for web scraping projects',
    author = 'Gregory Petukhov',
    author_email = 'lorien@lorien.name',
    install_requires = ['pytils', 'six', 'lxml', 'user_agent'],
    packages = find_packages(exclude=['test']),
    license = "MIT",
    classifiers = (
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
)
