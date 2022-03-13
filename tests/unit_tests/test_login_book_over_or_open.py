from tests.utils import mock_club, mock_competitions
import server
import flask


def flash_message(message):
    return str(flask.get_flashed_messages(message))


def test_response_open_or_over(client, mocker):

    data = {"email": mock_club[0]["email"]}

    mocker.patch.object(server, "clubs", mock_club)

    response = client.post("/showSummary", data=data)

    assert "Over" in response.data.decode("utf-8")
    assert "Open" in response.data.decode("utf-8")
    assert response.status_code == 200


def test_book_display_competition_open(client, mocker):

    data1 = mock_club[0]["name"]
    data2 = mock_competitions[0]["name"]

    mocker.patch.object(server, "clubs", mock_club)
    mocker.patch.object(server, "competitions", mock_competitions)

    response = client.get("/book/{}/{}".format(data2, data1))
    assert response.status_code == 200


def test_book_not_display_competition_open(client, mocker):

    data1 = mock_club[0]["name"]
    data2 = mock_competitions[2]["name"]

    mocker.patch.object(server, "clubs", mock_club)
    mocker.patch.object(server, "competitions", mock_competitions)

    response = client.get("/book/{}/{}".format(data2, data1))
    assert response.status_code == 400
