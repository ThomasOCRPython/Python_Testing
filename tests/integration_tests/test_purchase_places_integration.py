from tests.utils import mock_club, mock_competitions
import server
import flask


def flash_message(message):
    return str(flask.get_flashed_messages(message))


def test_show_remaining_places(client, mocker):
    data1 = mock_club[0]["name"]
    data2 = mock_competitions[0]["name"]
    number_of_places = mock_competitions[0]["numberOfPlaces"]
    places = "2"

    mocker.patch.object(server, "clubs", mock_club)
    mocker.patch.object(server, "competitions", mock_competitions)

    response = client.post(
        "/purchasePlaces", data={"club": data1, "competition": data2, "places": places}
    )

    new_number_of_places = mock_competitions[0]["numberOfPlaces"]

    assert new_number_of_places == int(number_of_places) - int(places)
    assert flash_message("") == "['Great-booking complete!']"
    assert "Number of Places: 23" in response.data.decode("utf-8")
    assert response.status_code == 200

    index = client.get("/book/{}/{}".format(data2, data1))
    assert "Places available: 23" in index.data.decode("utf-8")


def test_show_not_remaining_places_because_exeeded_quota(client, mocker):

    data1 = mock_club[0]["name"]
    data2 = mock_competitions[0]["name"]
    number_of_places = mock_competitions[0]["numberOfPlaces"]
    mock_club[0]["points"] = 13
    places = "13"

    mocker.patch.object(server, "clubs", mock_club)
    mocker.patch.object(server, "competitions", mock_competitions)

    response = client.post(
        "/purchasePlaces", data={"club": data1, "competition": data2, "places": places}
    )

    new_number_of_places = mock_competitions[0]["numberOfPlaces"]

    assert new_number_of_places != int(number_of_places) - int(places)

    assert (
        flash_message("") == "['Sorry, you have exceeded your points quota available.']"
    )

    assert response.status_code == 200

    index = client.get("/book/{}/{}".format(data2, data1))
    assert "Places available: 23" in index.data.decode("utf-8")


# test past
def test_not_show_past_competition(client, mocker):
    data1 = mock_club[0]["name"]
    data2 = mock_competitions[2]["name"]

    # number_of_places = mock_competitions[1]["numberOfPlaces"]
    places = "13"

    mocker.patch.object(server, "clubs", mock_club)
    mocker.patch.object(server, "competitions", mock_competitions)

    response = client.post(
        "/purchasePlaces", data={"club": data1, "competition": data2, "places": places}
    )
    assert response.status_code == 200
    index = client.get("/book/{}/{}".format(data2, data1))

    assert index.status_code == 400


def test_show_remaining_points(client, mocker):
    data1 = mock_club[0]["name"]
    data2 = mock_competitions[0]["name"]
    places = "3"

    mocker.patch.object(server, "clubs", mock_club)
    mocker.patch.object(server, "competitions", mock_competitions)

    response = client.post(
        "/purchasePlaces", data={"club": data1, "competition": data2, "places": places}
    )

    assert mock_club[0]["points"] == 10

    assert response.status_code == 200

    index = client.get("/book/{}/{}".format(data2, data1))
    assert index.status_code == 200
    assert "Points available: 10" in response.data.decode("utf-8")
    board = client.get("/pointsBoard")
    assert board.status_code == 200
    assert mock_club[0]["points"] == 10
