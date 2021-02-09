from flask import Flask, render_template, request, redirect, session, flash, url_for
import json

app = Flask(__name__)
app.config["DEBUG"] = True



    @route("/get")
    def twitterposts():

    auth = tweepy.OAuthHandler("kLBuI2XrILD4qIJ3vZhJY7KTf", "CpCEWCmbWVMWWuTVSvTrNEA9KgESonp1NEozgDSEjqPscItt1N")
    auth.set_access_token("1338824296177786883-mzQQKoz1p6YUclAkQIMScBweIKnbWg", "bSeaoJs8OPSav7bvbcA3K86kjA0VhskAfDHgnuq8o6gF1")
    api = tweepy.API(auth)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    tweet_dict = {
        "username" : "",
        "text" : ""
    }

    tweeters = []
    for posts in api.search(q="malmö universitet"):
        # print(f"{tweet.user.name}:{tweet.text}")
        tweet_dict["username"]=posts.user.name
        tweet_dict["text"]=posts.text
        tweeters.append(tweet_dict)

    tweeters.jsonify()

    print(tweeters)

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=8080, debug=True)