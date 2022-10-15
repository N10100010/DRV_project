import re
from setuptools import setup


def pip_to_requirements(s):
    """
    Change a PIP-style requirements.txt string into one suitable for setup.py
    """

    if s.startswith('#'):
        return ''
    m = re.match('(.*)([>=]=[.0-9]*).*', s)
    if m:
        return '%s (%s)' % (m.group(1), m.group(2))
    return s.strip()


setup(
    name='DRB_backend',
    version=open('VERSION', 'r').read().strip(),
    author='UNKNOWN',
    author_email='UNKNOWN',
    license='UNKNOWN',
    url='https://github.com/meejah/python-skeleton',

    install_requires=open('backend/requirements.txt').readlines(),
    extras_require=dict(
        dev=open('requirements-dev.txt').readlines()
    ),
    description='XXX Skeleton python project example.',
    long_description=open('README.rst', 'r').read(),
    keywords=['python', 'XXX'],
    classifiers=[
        'Development Status :: DEV ALPHA',
        'License :: OSI Approved :: UNKNOWN',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9',
    ],

    packages=["DRB_backend"],
    entry_points=dict(
        console_scripts=[
            'checkout=checkout.cli:cli'
        ]
    ))
