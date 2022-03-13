from tests.utils import mock_club, mock_competitions
import server
import flask


def flash_message(message):
    return str(flask.get_flashed_messages(message))


# test  assez de point
def test_purchase_places_enough_point(client, mocker):

    data1 = mock_club[1]["name"]
    data2 = mock_competitions[0]["name"]

    places = "2"
    mocker.patch.object(server, "clubs", mock_club)
    mocker.patch.object(server, "competitions", mock_competitions)

    response = client.post(
        "/purchasePlaces", data={"club": data1, "competition": data2, "places": places}
    )
    assert response.status_code == 200


# test pas assez de point
def test_purchase_places_not_enough_point(client, mocker):

    data1 = mock_club[1]["name"]
    data2 = mock_competitions[1]["name"]

    places = 5
    mocker.patch.object(server, "clubs", mock_club)
    mocker.patch.object(server, "competitions", mock_competitions)

    response = client.post(
        "/purchasePlaces", data={"club": data1, "competition": data2, "places": places}
    )
    assert flash_message("") == '["Sorry, you don\'t have enough points."]'
    assert response.status_code == 200


# test + 12
def test_purchase_places_over_12_point(client, mocker):

    data1 = mock_club[0]["name"]
    data2 = mock_competitions[1]["name"]
    mock_club[0]["points"] = 13
    places = 13

    mocker.patch.object(server, "clubs", mock_club)
    mocker.patch.object(server, "competitions", mock_competitions)

    response = client.post(
        "/purchasePlaces", data={"club": data1, "competition": data2, "places": places}
    )

    assert (
        flash_message("") == "['Sorry, you have exceeded your points quota available.']"
    )
    assert response.status_code == 200


# vérifie point retiré
def test_purchase_places_remaining_point(client, mocker):
    data1 = mock_club[0]["name"]
    data2 = mock_competitions[1]["name"]
    places = 3

    mocker.patch.object(server, "clubs", mock_club)
    mocker.patch.object(server, "competitions", mock_competitions)

    response = client.post(
        "/purchasePlaces", data={"club": data1, "competition": data2, "places": places}
    )
    assert mock_club[0]["points"] == 10
    assert "Points available: 10" in response.data.decode("utf-8")
