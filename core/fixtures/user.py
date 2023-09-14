import pytest
from core.user.models import User

data_user ={
    "username": "test_user",
    "email": "test@gmail.com",
    "first_name": "TEST",
    "last_name": "USER",
    'password':"test_password"
}

# 모든 테스트에 import 해서 테스트 유저로 사용 가능
@pytest.fixture
def user(db) -> User:
    return User.objects.create_user(**data_user)