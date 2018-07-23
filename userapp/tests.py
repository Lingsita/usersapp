import unittest

from userapp.models import User


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.users = User('The widget')

    def test_create(self):
        self.assertEqual(self.user.size(), (50,50),
                         'incorrect default size')

    def test_retrieve(self):
        self.user.resize(100,150)
        self.assertEqual(self.widget.size(), (100,150),
                         'wrong size after resize')

if __name__ == '__main__':
    unittest.main()