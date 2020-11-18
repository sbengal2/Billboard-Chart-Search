# imports
from datetime import datetime

import spotipy
from pymongo import MongoClient
from spotipy.oauth2 import SpotifyClientCredentials

# Mongo DataBase connection
client = MongoClient('localhost', 27017, unicode_decode_error_handler='ignore')
data_base = client['billboard']
collection = data_base['songs']

# authenticating and connecting to spotify API
client_id = '3aef940809f64b08b1bbc12dda91d750'
client_secret = 'f89e23cf5c914da88e08e52e7401b77c'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)  # spotify object to access API


# method to obtain genre for each song using spotify API
def get_genre(q):
    try:
        return sp.search(q, limit=1, offset=0, type='artist')  # search query
    except:
        return 'not found'


# method to update genre for each song
def update_genre():
    count = 0
    for x in collection.find({'genre': {'$exists': False}}):
        result = get_genre(x['Performer'])
        if result["artists"]['items']:
            genre = result['artists']['items'][0]['genres']
            if genre:
                collection.update_one({'_id': x['_id']},
                                      {'$set': {'genre': genre}})
        else:
            collection.update_one({'_id': x['_id']},
                                  {'$set': {'genre': 'Not Found'}})
        print(count)
        count += 1


# method to convert WeekID from string format to date format
def get_date_in_string():
    return collection.aggregate([{
        "$project": {
            "date": {
                "$dateFromString": {
                    "dateString": '$WeekID',
                    "format": "%Y-%m-%d"
                }
            }
        }
    }])


# method to update the date field for each song
def update_date_from_string():
    date_from_string = get_date_in_string()
    for x in date_from_string:
        collection.update_one({"_id": x["_id"]}, {"$set": {"date": x["date"]}})


# method to get year from date
def get_year(date_in):
    dt = datetime.strptime(date_in, '%m/%d/%y')
    if dt.year > 2020:
        dt = dt.replace(year=dt.year - 100)
    return dt


# method to update the date field for each song
def update_date():
    count = 1
    documents = collection.aggregate([{
        "$project": {
            "date": {
                "$dateFromString": {
                    "dateString": '$WeekID',
                    "format": "%m/%d/%Y"
                }
            }
        }
    }])
    for x in collection.find({}):
        collection.update_one({'_id': x['_id']}, {"$set": {"date": get_year(x['WeekID'])}})


# method to convert peak position to integer format
def update_peak_position():
    doc = collection.find({})
    for x in doc:
        collection.update_one({'_id': x['_id']}, {'$set': {'Peak Position': int(x['Peak Position'])}})


# method to remove any unwanted field from the data-set
def remove_any_field():
    collection.update_many({}, {'$unset': {'active_year': 1}})


# method to update any field in the data-set
def update_any_field():
    year_list = collection.aggregate([{"$project": {"year": {"$year": "$date"},
                                                    "week": {"$week": "$date"}}}])
    for x in year_list:
        collection.update_one({'_id': x['_id']}, {'$set': {'active_year': x['year']}})


# method to create active year for each song using its WeekID
def update_active_year():
    count = 0
    for x in collection.find({}):
        y = collection.find_one({'SongID': x['SongID']})
        collection.update_one({'SongID': y['SongID']}, {'$set': {'active_year': y['active_year']}})
        print(count)
        count += 10


# method to create week for each song using its WeekID
def update_week():
    for x in collection.aggregate([{'$project': {'week': {'$week': '$WeekID'}}}]):
        collection.update_one({'_id': x['_id']}, {'$set': {'week': x['week']}})
