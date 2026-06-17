import unittest
from app import create_app
from app.extensions import db
from app.models import User

class UserModelTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        user = User(username='test', email='test@example.com', password_hash='hash')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(User.query.count(), 1)