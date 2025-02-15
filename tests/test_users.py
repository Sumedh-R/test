import unittest
from services.users.implementations.sql_user_repository import SQLUserRepository
from services.users.implementations.mongo_user_repository import MongoUserRepository

class TestUsers(unittest.TestCase):
    def setUp(self):
        self.sql_repo = SQLUserRepository()
        self.mongo_repo = MongoUserRepository()

    def test_create_user(self):
        user_data = {"name": "Test User", "email": "test@example.com"}
        self.assertIsNotNone(self.sql_repo.create_user(user_data))
        self.assertIsNotNone(self.mongo_repo.create_user(user_data)) 