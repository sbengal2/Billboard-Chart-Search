# imports
import lyricsgenius
from pymongo import MongoClient
from textblob import TextBlob

# connecting to Mongo DataBase
client = MongoClient('localhost', 27017, unicode_decode_error_handler='ignore')
data_base = client['billboard']
collection = data_base['songs']
genius = lyricsgenius.Genius('7IYwBZhL1rXVpdZ8qrz4ZMFSdYboWnv1yJIzpvBU29bOa1bq8YKWddl_r2bIugkR')


# method to get the lyrics for each song
def get_lyrics(title, artist):
    try:
        return genius.search_song(title, artist).lyrics
    except:
        return 'not found'


# method to update lyrics for each song
def update_lyrics():
    for x in collection.find({}):
        lyrics = get_lyrics(x['Song'], x['Performer'])
        if lyrics:
            collection.update_one({'_id': x['_id']}, {'$set': {'lyrics': lyrics}})


# method to get the lyrics polarity for each song using textblob
def get_polarity(lyrics):
    analysis = TextBlob(lyrics)
    return analysis.sentiment.polarity


# method to update polarity for each song
def update_polarity():
    print('hi')
    count = 0
    for song in collection.find({}):
        collection.update_one({'_id': song['_id']}, {'$set': {'Sentiment': get_polarity(song['Lyrics'])}})
        print(count)
        count += 1
