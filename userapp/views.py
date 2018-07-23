from . import settings

from userapp.models import User
from userapp import session_scope



def login(postvars=None, method='GET'):
    if method=='POST':
        username = postvars.get(b'username')[0].decode("utf-8")
        password = postvars.get(b'password')[0].decode("utf-8")

        with session_scope() as session:
            user = session.query(User).filter_by(username=username).first()
            session.commit()
            if user and user.password == password:
                return (301, '/list')
            else:
                template = settings.template_env.get_template('login.html')
                return (200, template.render(error_message=True))

    template = settings.template_env.get_template('login.html')
    return (200, template.render())


def register(postvars=None, method='GET'):
    if method=='POST':
        username = postvars.get(b'username')[0].decode("utf-8")
        email = postvars.get(b'email')[0].decode("utf-8")
        country = postvars.get(b'country')[0].decode("utf-8")
        password = postvars.get(b'password')[0].decode("utf-8")

        with session_scope() as session:
            q = session.query(User).filter_by(username=username).first()
            session.commit()
            if not q:
                user = User(username=username, email=email, password=password, country=country, active=True)
                session.add(user)
                session.commit()
        return (301, '/list')

    template = settings.template_env.get_template('register.html')
    return (200, template.render())


def user_list():
    with session_scope() as session:
        users = session.query(User).all()
        session.commit()
        template = settings.template_env.get_template('list.html')
        return (200, template.render(users=users))


def logout():
    return (301, '/')