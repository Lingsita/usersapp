from jinja2 import Template
from jinja2 import Environment, PackageLoader, select_autoescape
from . import settings

env = Environment(
    loader=PackageLoader('userapp', settings.TEMPLATE_FOLDER),
    autoescape=select_autoescape(['html', 'xml'])
)


def index(request):
    print(request)
    template = Template('Hello {{ name }}!')
    template.render(name='John Doe')
    return template


def register(request):
    template = Template('Hello {{ name }}!')
    template.render(name='John Doe')


def user_list(request):
    template = Template('Hello {{ name }}!')
    template.render(name='John Doe')
    return template


def logout(request):
    template = Template('Hello {{ name }}!')
    template.render(name='John Doe')