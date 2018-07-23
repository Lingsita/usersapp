from server import Router
from userapp.views import login, register, user_list, logout

urls = [
    ('/', login),
    ('/register', register),
    ('/list', user_list),
    ('/logout', logout),
]