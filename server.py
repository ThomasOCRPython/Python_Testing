import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime
from flask_api import status
from flask import Response

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    date_time_now = str(datetime.now())
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html',club=club,competitions=competitions,date=date_time_now, clubs=clubs)
    except IndexError:
        flash("Sorry, that email wasn't found.")
        return render_template('index.html',error_message="Sorry, that email wasn't found.",date=date_time_now)

@app.route('/book/<competition>/<club>')
def book(competition,club):
    
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    date_time = str(datetime.now())
    competition_date = foundCompetition['date']

    if date_time > competition_date:
        return Response("The response body goes here",status=400,)
        # return "Record not found", status.HTTP_400_BAD_REQUEST
        # flash("Sorry , this competitions is over.")
        # return render_template('welcome.html',club=club, competition=competition, date=date_time)
    
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition,date=date_time, clubs=clubs)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions, date=date_time, clubs=clubs)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    club_point = int(club['points'])
    date = str(datetime.now())
    
        
    if club_point < placesRequired :
        flash("Sorry, you don't have enough points.")
        return render_template('booking.html',club=club, competition=competition, date=date, clubs=clubs)
    
    elif placesRequired > 12:
        flash("Sorry, you have exceeded your points quota available.")
        return render_template('booking.html',club=club, competition=competition, date=date, clubs=clubs)
    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions, date=date, clubs=clubs)

@app.route('/pointsBoard')
def points_display():
    return render_template('board.html', clubs=clubs)

# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))