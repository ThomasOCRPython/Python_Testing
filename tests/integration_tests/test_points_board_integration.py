from tests.utils import mock_club
import server
import flask


def flash_message(message):
    return str(flask.get_flashed_messages(message))


def test_login_write_user_and_show_board(client, mocker):

    data = {"email": mock_club[0]["email"]}
    mocker.patch.object(server, "clubs", mock_club)

    login = client.get("/")
    assert "Welcome to the GUDLFT Registration Portal!" in login.data.decode("utf-8")

    response = client.post("/showSummary", data=data)
    assert login.status_code == 200
    assert "Welcome, john@simplylift.co " in response.data.decode("utf-8")
    assert response.status_code == 200

    board = client.get("/pointsBoard")
    assert board.status_code == 200
    assert "Points" in board.data.decode("utf-8")
