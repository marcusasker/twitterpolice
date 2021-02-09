from flask import Flask, render_template, request, redirect, session, flash, url_for
import json

import requests
import tweepy

app = Flask(__name__)
app.config["DEBUG"] = True
@app.route('/')
def hello():

    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    brott = request.form['brott']

    response = requests.get("https://polisen.se/api/events?type=" + brott)
    print(response.headers['content-type'])
    # f=open(response)
    # data=json.load(f)
    res = response.json()
    # print(res)
    geolocations = []
    geodict = {
        "id" : "",
        "longitude" : "",
        "latitude" : ""
    }
    for stories in res:
        a_dict = stories["location"]
        a_id = stories["id"]
        for things in a_dict:
            a_list = a_dict["gps"].split(",")
            longitude = a_list[0]
            latitude = a_list[1]
            geodict["id"]=a_id
            geodict["longitude"]=longitude
            geodict["latitude"]=latitude
            geolocations.append(geodict)

    auth = tweepy.OAuthHandler("kLBuI2XrILD4qIJ3vZhJY7KTf", "CpCEWCmbWVMWWuTVSvTrNEA9KgESonp1NEozgDSEjqPscItt1N")
    auth.set_access_token("1338824296177786883-mzQQKoz1p6YUclAkQIMScBweIKnbWg", "bSeaoJs8OPSav7bvbcA3K86kjA0VhskAfDHgnuq8o6gF1")
    api = tweepy.API(auth)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    tweet_dict = {
        "username" : "",
        "text" : ""
    }
    
    tweeters = []
    for posts in api.search(q=brott, geocode=str(longitude + "," +  latitude + "," + "50km"), lang="sv", rpp=10):
        # print(f"{tweet.user.name}:{tweet.text}")
        tweet_dict["username"]=posts.user.name
        tweet_dict["text"]=posts.text
        tweeters.append(tweet_dict)

    

        
    return render_template('search.html', brott=brott, res=res, tweeters=tweeters)

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5000, debug=True)