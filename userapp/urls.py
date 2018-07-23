from server import Router
from userapp.views import index, register, user_list, logout

urls = [
    ('/', index),
    ('/register', register),
    ('/list', user_list),
    ('/logout', logout),
]