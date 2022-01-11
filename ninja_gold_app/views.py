from django.shortcuts import render, redirect
from datetime import datetime
from pytz import timezone
import random, pytz

# Create your views here.
def index(request):
    if 'gold' not in request.session or 'activities' not in request.session:
        request.session['gold'] = 0
        request.session['activities'] = []

    context = {
        "activities":request.session['activities']
    }
    return render(request, "index.html", context)

def process_money(request):
    if request.method == 'POST':
        #SETUP
        myGold = request.session['gold']
        activities = request.session['activities']
        location = request.POST['location']
        #MY LOCATION STUFF
        if location == 'farm':
            goldThisTurn = round(random.random() * 10 + 10)
        elif location == 'cave':
            goldThisTurn = round(random.random() * 5 + 10)
        elif location == 'house':
            goldThisTurn = round(random.random() * 3 + 2)
        else:
            #do casino stuff
            winOrLose = round(random.random())
            if winOrLose == 1:
                goldThisTurn = round(random.random() * 50)
            else:
                goldThisTurn = (round(random.random() * 50) * -1)
        
        #MY TURN STUFF
        date_format='%m/%d/%Y %H:%M:%S %Z'
        date = datetime.now(tz=pytz.utc)
        date = date.astimezone(timezone('US/Pacific'))
        myTime = date.strftime(date_format)

        myGold += goldThisTurn
        request.session['gold'] = myGold

        if goldThisTurn >= 0:
            str = f"Earned {goldThisTurn} from the {location}! Hooray!! {myTime}"            
        else:
            goldThisTurn *= -1
            str = f"Lost {goldThisTurn} from the {location}! Awh Sad :( {myTime}"
        
        activities.insert(0, str)
        request.session['activities'] = activities

    return redirect("/")
