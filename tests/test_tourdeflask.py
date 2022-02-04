import pytest
from src.app import app


@pytest.fixture()
def client():
    return app.test_client()


def test_basic_call(client):
    response = client.get('/')
    assert b'Welcome to Tour de Flask!' in response.data
