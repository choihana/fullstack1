import pytest
from rest_framework.test import APIClient

@pytest.fixture
def client():
    # 다양한 HTTP 메서드를 처리하고 테스트에서 인증과 같은 기능을 처리하는 클래스
    return APIClient()
