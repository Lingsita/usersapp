import os

from jinja2 import Environment, FileSystemLoader

TEMPLATE_FOLDER = 'templates'

CUSTOM_MODULES = [
    'userapp'
]

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# jinja2 environment.
template_env = Environment(loader=FileSystemLoader(os.path.join(ROOT_DIR, 'templates')),
                     trim_blocks=True)