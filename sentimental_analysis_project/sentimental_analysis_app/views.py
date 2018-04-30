from django.shortcuts import render,HttpResponse
import json
from django.shortcuts import redirect
from django.conf import settings
from sentimental_analysis_app.models import DemonitisationTweets
from sentimental_analysis_app.utils.data_writer import dump_csv_data_to_db
from django.db.models import Count
from django.core import serializers
from django.db import connection
from contextlib import closing

 
def profile(request):
    if not request.user.is_authenticated:
        return redirect('/')
    return render(request,'home.html')

def process_data(request):
    try:
        dump_csv_data_to_db()
        message="Successfully processed CSV data...!!!"
        print("Successfully processed CSV data...!!!")
    except IOError:
        message="Failed to dump csv to data base...!!!"
    return HttpResponse(content=json.dumps({'message':message}),content_type="application/json")

# Q1. Get percentage of different type of sentiment (Positive, Negative, Neutral)
def get_percentages_of_different_sentiments(request):
    chartData = []
    sql = "SELECT sentiment_type, count(*) as total FROM sentimental_analysis_app_demonitisationtweets GROUP BY sentiment_type;"
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            chartData.append([row[0],row[1]])
    return HttpResponse(content=json.dumps({'chartData':chartData, 'chartTitle': "<center><h2>Percentage of Tweets Positive, Negative or Netural.</h2></center>"}), content_type="application/json")


def get_most_popular_users_chart_data(request):
    return HttpResponse(content=json.dumps({"Users":[
    	{"id": 11,
         "ScreenName": "Ram",
         "ReTweets": "123",
         "Tweets": "3"
    	  },
    	  {"id": 12,
         "ScreenName": "Rahul",
         "ReTweets": "122",
         "Tweets": "3"
    	  },
    	  {"id": 10,
         "ScreenName": "Ishar",
         "ReTweets": "120",
         "Tweets": "3"
    	  },

    	]}), content_type="application/json")


