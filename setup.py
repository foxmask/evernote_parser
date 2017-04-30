from setuptools import setup, find_packages
from evernote_parser import __version__ as version

install_requires = [
    'lxml==3.7.3',
    'pypandoc==1.3.3'
]

setup(
    name='evernote_parser',
    version=version,
    description='Evernote enex parser file. Will create one file for each note',
    author='FoxMaSk',
    maintainer='FoxMaSk',
    author_email='foxmask@trigger-happy.eu',
    maintainer_email='foxmask@trigger-happy.eu',
    url='https://github.com/foxmask/evernote_parser',
    download_url="https://github.com/foxmask/evernote_parser/"
                 "archive/evernote_parser-" + version + ".zip",
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=install_requires,
    include_package_data=True,
)