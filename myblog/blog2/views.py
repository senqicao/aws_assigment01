from django.shortcuts import render
import tweepy
import textblob
from gmaps import Geocoding
import folium
import random
from . import forms
from . import models






def index(request):
    consumer_key = "YAvBBJnUpgMOWIkBbzjjsCy1q"
    consumer_secret = "xPcvMjYjSicdIIcC57E9M8X51sarSiSi3syNjNZpNHn9wbz9gd"
    access_token = "841688184467705856-Sm1KiDoZomcOHgsXvJWj9ifXsHR5nc9"
    access_token_secret = "IhAGMDIfLn5eWvhUQVFvhqnYZ48q6c9VGZH735a43F3AZ"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    word = request.GET.get("word", None)

    public_tweets = api.search(str(word), retry_count = 3, count = 50)

    api1 = Geocoding()
    lat1 = dict(api1.geocode("new york")[0])['geometry']['location']['lat']
    lng1 = dict(api1.geocode("new york")[0])['geometry']['location']['lng']
    map_osm = folium.Map(location=[lat1, lng1], zoom_start=3)

    for tweet in public_tweets:

        analysis = textblob.TextBlob(tweet.text)
        a = tweet.user.location
        try:

            if a == '' or len(a) >= 12 or len(a) <= 3 or textblob.TextBlob(a).detect_language() != 'en' or a=='interwebs':
                lat = random.uniform(30, 60)
                lng = random.uniform(-135, -75)
            else:
                lat = dict(api1.geocode(a)[0])['geometry']['location']['lat']
                lng = dict(api1.geocode(a)[0])['geometry']['location']['lng']

            if analysis.sentiment[0] > 0:
                folium.Marker([lat, lng], popup=str(analysis.sentiment)+"location:"+str(a)+"latitude:"+str(round(lat,2))+"longitude:"+str(round(lng,2)), icon=folium.Icon(color='green')).add_to(map_osm)
            elif analysis.sentiment[0] == 0:
                folium.Marker([lat, lng], popup=str(analysis.sentiment)+"location:"+str(a)+"latitude:"+str(round(lat,2))+"longitude:"+str(round(lng,2)), icon=folium.Icon(color='blue')).add_to(map_osm)
            elif analysis.sentiment[0] < 0:
                folium.Marker([lat, lng], popup=str(analysis.sentiment)+"location:"+str(a)+"latitude:"+str(round(lat,2))+"longitude:"+str(round(lng,2)), icon=folium.Icon(color='red')).add_to(map_osm)
        except:
            pass
        map_osm.save('blog2/templates/blog2/osm.html')

    return render(request, "blog2/osm.html")

def index2(request):
    return render(request, "blog2/word.html")

