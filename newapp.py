from flask import Flask, render_template, request, redirect, session, flash, url_for, flash
import json
from twitterfunctions import search_tweet, get_police, search_police, get_geo_locations, search_all_tweet, search_all_police
app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def hello():
    error = None
    res = get_police()
    x = "Polis"
    y = search_all_tweet(x)
    return render_template('index.html', res=res, tweeters=y, error=error)

@app.route('/search', methods=['GET', 'POST'])
def search():

    try:
        brott = request.form['brott']
        date = request.form['date']

        if date == "":
            res = search_all_police(brott)
            x = get_geo_locations(res)
            for cordinate in x:
                lon = cordinate["longitude"]
                lat = cordinate["latitude"]
            y = search_tweet(brott, lon, lat)
            return render_template('search.html', brott=brott, res=res, tweeters=y)

        else:
            rez = search_police(brott, date)
            if rez == []:
                error = 'Det datum du har valt är ogiltligt, vänligen välj något annat!'
                res = get_police()
                x = "Polis"
                y = search_all_tweet(x)
                return render_template("index.html", res=res, tweeters=y, error=error)
            else:
                x = get_geo_locations(rez)
                for cordinate in x:
                    lon = cordinate["longitude"]
                    lat = cordinate["latitude"]
                y = search_tweet(brott, lon, lat)
                return render_template('search.html', brott=brott, res=rez, tweeters=y)

    except UnboundLocalError:
        error = 'Något gick fel med din sökning, tryck på hjälp för att få information angående sökning!'
        res = get_police()
        x = "Polis"
        y = search_all_tweet(x)
        return render_template("index.html", res=res, tweeters=y, error=error)

    
@app.route('/api')
def api():
    return render_template('apidoc.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5000, debug=True)