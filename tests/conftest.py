import pytest
import server


@pytest.fixture
def client():
    new_app = server.app
    new_app.testing = True
    with new_app.test_client() as c:
        yield c
