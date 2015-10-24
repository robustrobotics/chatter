try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'chatter',
    'description': 'Chatterbot for Github',
    'author': 'Will Vega-Brown',
    'url': 'https://github.com/wrvb/chatter',
    'download_url': 'https://github.com/wrvb/chatter/archive/master.zip',
    'author_email': 'wrvb@mit.edu',
    'version': '0.0.1',
    'install_requires': ['nose'],
    'packages': ['chatter'],
    'scripts': ['bin/chatter', 'bin/server']
}

setup(**config)
