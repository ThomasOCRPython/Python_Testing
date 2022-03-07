from tests.utils import mock_club
import server
import flask

def flash_message(message):
    return str(flask.get_flashed_messages(message)) 


def test_login_write_email(client,mocker):
    data = {'email': mock_club[0]['email']}
    
    mocker.patch.object(server, 'clubs', mock_club)


    response = client.post("/showSummary", data=data)
    assert response.status_code == 200


def test_login_wrong_email(client, mocker):
    data = {'email': 'invalid@invalid.com'}

    mocker.patch.object(server, 'clubs', mock_club)
    response = client.post("/showSummary", data=data)
    assert response.status_code == 200
    assert flash_message('')== '["Sorry, that email wasn\'t found."]'
      
    