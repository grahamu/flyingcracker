import os
import sys
from setuptools import setup

from flyingcracker import VERSION

def read(fname):
    f = open(os.path.join(os.path.dirname(__file__), fname))
    contents = f.read()
    f.close()
    return contents

setup(
    name='flyingcracker',
    version=".".join(map(str, VERSION)),
    description="flyingcracker is a community service web application",
    long_description=read('README.rst'),
    author='Graham Ullrich',
    author_email='graham@flyingcracker.com',
    url='https://github.com/grahamu/flyingcracker/',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Framework :: Django',
    ]
)