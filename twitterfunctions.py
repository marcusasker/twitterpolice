import tweepy
import requests

'''En funktion som autentiserar användare och söker efter tweets med hjälp utav ett sökord i parametern,
det som returneras är en lista med lexikon på twitteranvändarens namn och själva tweet'''
def search_all_tweet(question):
    auth = tweepy.OAuthHandler("kLBuI2XrILD4qIJ3vZhJY7KTf", "CpCEWCmbWVMWWuTVSvTrNEA9KgESonp1NEozgDSEjqPscItt1N")
    auth.set_access_token("1338824296177786883-mzQQKoz1p6YUclAkQIMScBweIKnbWg", "bSeaoJs8OPSav7bvbcA3K86kjA0VhskAfDHgnuq8o6gF1")
    api = tweepy.API(auth)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    tweeters = []
    new_search = api.search(q=question, lang="sv", maxResults=10)
    for status in new_search:
        tweet_dict = {
        "username" : "",
        "text" : ""
        }
        tweet_dict["username"]=status.user.name
        tweet_dict["text"]=status.text
        tweeters.append(tweet_dict)
    
    return tweeters
    
'''Hämtar in data från polisens api och returnerar värdet.  '''
def get_police():
    response = requests.get("https://polisen.se/api/events")
    print(response.headers['content-type'])
    res = response.json()
    return res
    
''' konverterar månader från polisens api till integers för att kunna jämföra med kalendern. '''
def converter(month):
    if month == "januari":
        return "01"
    elif month == "februari":
        return "02"
    elif month == "mars":
        return "03"
    elif month == "april":
        return "04"
    elif month == "maj":
        return "05"
    elif month == "juni":
        return "06"
    elif month == "juli":
        return "07"
    elif month == "augusti":
        return "08"
    elif month == "september":
        return "09"
    elif month == "oktober":
        return "10"
    elif month == "november":
        return "11"
    else:
        return "12"

'''Söker efter polishändelser med hjälp utav ett sökord och ett datum i parametern, 
med hjälp av föregående funktion kollar den datum på händelserna och lägger till de 
händelserna som matchar med datumsökning i en lista som sedan returneras'''
def search_police(question, date):
    result = []
    response = requests.get("https://polisen.se/api/events?type=" + question)
    print(response.headers['content-type'])
    res = response.json()
    for story in res:
        x = story["name"].split(" ")
        a = x[1]
        y = "2021" + "-" + converter(a) + "-" + x[0]
        if y == date:
            result.append(story)
    return result

'''Söker efter polishändelser med hjälp utav ett sökord i parametern, till skillnad från den
föregående bortser denna funktionen från vilket datum händelsen skedde på. Resultatet returneras
som en lista med flera lexikon'''
def search_all_police(question):
    response = requests.get("http://polisen.se/api/events?type=" + question)
    print(response.headers['content-type'])
    res = response.json()
    return res

'''Får ut vilka geolocations ett specifikt lexikon har, denna funktionen är specifikt gjord
för den data man får ut från polisens API'''
def get_geo_locations(dict):
    geolocations = []
    for item in dict:
        geodict = {
        "id" : "",
        "longitude" : "",
        "latitude" : ""
        }
        a_dict = item["location"]
        a_id = item["id"]
        for item in a_dict:
            a_list = a_dict["gps"].split(",")
            longitude = a_list[0]
            latitude = a_list[1]
            geodict["id"] = a_id
            geodict["longitude"] = longitude
            geodict["latitude"] = latitude
            geolocations.append(geodict)
            
    return geolocations

'''Söker efter tweets med hjälp utav ett sökord samt longitude och latitude i parametern, 
funktionen autentiserar användare och söker efter tweets i en radius kring longitude och latitude med en radius om 50km.
funktionen returnerar en lista med lexikon med twitteranvändarens namn samt själva tweet'''
def search_tweet(question, longitude, latitude):
    auth = tweepy.OAuthHandler("kLBuI2XrILD4qIJ3vZhJY7KTf", "CpCEWCmbWVMWWuTVSvTrNEA9KgESonp1NEozgDSEjqPscItt1N")
    auth.set_access_token("1338824296177786883-mzQQKoz1p6YUclAkQIMScBweIKnbWg", "bSeaoJs8OPSav7bvbcA3K86kjA0VhskAfDHgnuq8o6gF1")
    api = tweepy.API(auth)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    tweeters = []
    new_search = api.search(q=question, geocode=str(longitude + "," +  latitude + "," + "50km"), lang="sv", maxResults=1)
    for status in new_search:
        tweet_dict = {
        "username" : "",
        "text" : ""
        }
        tweet_dict["username"]=status.user.name
        tweet_dict["text"]=status.text
        tweeters.append(tweet_dict)
    
    return tweeters
