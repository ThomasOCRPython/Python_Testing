from tests.conftest import client


def test_should_status_code_ok(client):
	response = client.get('/')
	assert response.status_code == 200



def test_should_status_code_ok(client):
	response = client.get('/pointsBoard')
	assert response.status_code == 200

