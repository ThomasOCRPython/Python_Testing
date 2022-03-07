from locust import HttpUser, task
# from tests.utils import mock_club, mock_competitions
# from server import loadClubs, loadCompetitions



class ProjectPerfTest(HttpUser):
    email = "john@simplylift.co"
    club = "Simply Lift"
    competition = "Spring Festival"
    

    # email = mock_club[0]['email']
    # club = mock_club[0]['name']
    # competition = mock_club[0]['name']

    # email = loadClubs()[0]["email"]
    # club = loadClubs()[0]["name"]
    # competition = loadCompetitions()[0]['name']


    @task
    def index(self):
        response = self.client.get("/")

    @task(3)
    def login(self):
        response = self.client.post("/showSummary", data={"email": self.email})

    @task
    def points_board(self):
        self.client.get("/pointsBoard")

    @task
    def purchase_places(self):

        response = self.client.post("/purchasePlaces", data={
            "club": self.club,
            "competition": self.competition,
            "places": 1,
        })

    @task
    def book(self):
        response = self.client.get("/book/" + self.competition
                        + "/" + self.club)

    @task
    def logout(self):
        response = self.client.get("/logout")