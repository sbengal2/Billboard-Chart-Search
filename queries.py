# imports
import os
from re import split

from pymongo import MongoClient
import re

# connecting to Mongo DataBase
client = MongoClient('localhost', 27017, unicode_decode_error_handler='ignore')
data_base = client['billboard']
collection = data_base['songs']


# method to get the input string in camel-case
def get_camel_case(input_phrase):
    words = []
    split_words = split('([^a-zA-Z0-9])', input_phrase)
    for x in split_words:
        if x.isalnum():
            words.append(x.capitalize())
    return " ".join(words)


def lyrics(song):
    print()
    print("ENTER 1 TO DOWNLOAD LYRICS FOR THE SONG")
    option = input("ENTER ANY NUMBER TO GO BACK: ")

    if int(option) == 1:
        os.system('clear')
        print(song['Lyrics'])
    else:
        os.system('clear')

# method to retrieve information of a song
def get_song_info():
    song_name = get_camel_case(input("ENTER THE TITLE OF THE SONG: "))
    count = collection.count_documents({'Song': song_name})
    if count == 0:
        print("SORRY, NO RECORD FOUND FOR: " + song_name.upper())
    elif count == 1:
        song = collection.find_one({'Song': song_name}, {'Song': 1, 'Performer': 1, 'Lyrics': 1, 'genre': 1,'active_year':1})
        os.system('clear')
        print('SONG: ' + song['Song'])
        print('ARTIST: ' + song['Performer'])
        if song.get('genre') is None:
            print("Not Found")
        else:
            print('GENRE: ' + ', '.join(map(str, song['genre'])))
        print('YEAR: '+str(song['active_year']))
        lyrics(song)

    else:
        artist_name = get_camel_case(input("ENTER THE NAME OF THE ARTIST: "))
        count = collection.count_documents({'Song': song_name, 'Performer': artist_name})
        os.system('clear')
        if count == 0:
            print("SORRY, NO RECORD FOUND FOR: " + song_name.upper() + " BY " + artist_name.upper())
        else:
            song = collection.find_one({'Song': song_name, 'Performer': artist_name},
                                       {'Song': 1, 'Performer': 1, 'Lyrics': 1, 'genre': 1, 'active_year': 1})
            print('SONG: ' + song['Song'])
            print('ARTIST: ' + song['Performer'])
            if song.get('genre') is None:
                print("Not Found")
            else:
                print('GENRE: ' + ', '.join(map(str, song['genre'])))
            print('YEAR: ' + str(song['active_year']))
            lyrics(song)


# method to get all the songs by an artist
def get_songs_by_performer():
    performer_name = get_camel_case(input("ENTER THE NAME OF THE ARTIST: "))
    look_up = collection.count_documents({'Performer': performer_name})
    if look_up == 0:
        print("SORRY, NO RECORD FOUND FOR: " + performer_name.upper() + "!")
    else:
        songs = collection.aggregate([
            {'$match': {'Performer': performer_name}},
            {'$group':
                {'_id': {
                    'Song': '$Song',
                    'artist': '$Performer',
                    'genre': '$genre',
                    'year': '$active_year'}}}
        ])
        os.system('clear')
        print(print("SHOWING " + str(look_up) + " RECORDS FOR " + "\"" + performer_name.upper() + "\""))
        for song in songs:
            # song = collection.find_one({'_id': x['_id']})
            print('SONG: ' + song['_id']['Song'])
            print('ARTIST: ' + song['_id']['artist'])
            if song['_id']['genre'] == "Not Found":
                print("Not Found")
            else:
                print('GENRE: ' + ', '.join(map(str, song['_id']['genre'])))
            print('YEAR: ' + str(song['_id']['year']))
            print()


# method to get the top-ten songs for each week in the input year
def get_top_songs_in_year():
    year = int(input("ENTER THE YEAR: "))
    no_of_records = collection.count_documents({'active_year': year})
    if no_of_records == 0:
        os.system('clear')
        print("SORRY, NO RECORDS FOUND!")
    else:
        year_list = collection.aggregate([{'$match': {'active_year': year, 'Peak Position': {'$gte': 1, '$lte': 10}}},
                                          {'$sort': {"Peak Position": 1, 'Weeks on Chart': 1}}])
        os.system('clear')
        print("THE MOST POPULAR SONGS FOR THE YEAR " + str(year) + " Are: ")
        for x in year_list:
            print('SONG: ' + x['Song'])
            print('ARTIST: ' + x['Performer'])
            if x['genre'] == "Not Found":
                print("Not Found")
            else:
                print('GENRE: ' + ', '.join(map(str, x['genre'])))
            print('YEAR: ' + str(x['active_year']))
            print()


# method to get the top-ten artists for each week in the input year
def get_top_artists_in_year():
    year = int(input("ENTER THE YEAR "))
    no_of_records = collection.count_documents({'active_year': year})
    if no_of_records == 0:
        os.system('clear')
        print("SORRY, NO RECORDS FOUND!")
    else:
        year_list = collection.aggregate([{'$match': {'active_year': year, 'Peak Position': {'$gte': 1, '$lte': 10}}},
                                          {'$sort': {"Peak Position": 1, 'Weeks on Chart': 1}}])
        os.system('clear')
        print("THE MOST POPULAR ARTISTS FOR THE YEAR: " + str(year))
        for x in year_list:
            print('ARTIST: ' + x['Performer'])
            if x['genre'] == "Not Found":
                print("Not Found")
            else:
                print('GENRE: ' + ', '.join(map(str, x['genre'])))
            print()


# method to get the top-ten genres for each week in the input year
def get_top_genres_in_year():
    genres = []
    year = int(input("ENTER THE YEAR: "))
    no_of_records = collection.count_documents({'active_year': year, 'genre': {'$not': {'$regex': "Not Found"}}})
    if no_of_records == 0:
        os.system('clear')
        print("SORRY, NO RECORDS FOUND!")
    else:
        year_list = collection.aggregate([{'$match': {'active_year': year,
                                                      'genre': {'$not': {'$regex': "Not Found"}},
                                                      'Peak Position': {'$gte': 1, '$lte': 10}}},
                                          {'$sort': {'Peak Position': 1}}])
        os.system('clear')
        print("THE MOST POPULAR GENRES FOR THE YEAR " + str(year) + " ARE: ")
        for x in year_list:
            if x != 'Not Found':
                genres = genres + list(x['genre'])
    for genre in set(genres):
        print(genre)


# method to get all the hot charts in the database
def get_all_hot_charts_for_year():
    start = 1958
    end = 2019
    os.system('clear')
    while start <= end:
        no_of_records = collection.count_documents({'active_year': start})
        print(print("SHOWING " + str(no_of_records) + " RECORDS FOR THE YEAR " + str(start) + ": "))
        print()
        if no_of_records == 0:
            print("SORRY, NO RECORDS FOUND!")
        else:
            doc = collection.aggregate([{'$match': {'active_year': start}}, {'$group':
                                                                                 {'_id': {'Song': '$Song',
                                                                                          'Performer': '$Performer',
                                                                                          'genre': '$genre',
                                                                                          'year': '$active_year'}}}])
            for x in doc:
                print('SONG: ' + x['_id']['Song'])
                print('ARTIST: ' + x['_id']['Performer'])
                if x['_id']['genre'] == "Not Found":
                    print("Genre: Not Found")
                else:
                    print('GENRE: ' + ', '.join(map(str, x['_id']['genre'])))
                print('YEAR: ' + str(x['_id']['year']))
                print()
        start += 1


# method to get all the songs of a genre
def get_songs_by_genre():
    genre = (input("ENTER THE GENRE: ")).lower()
    regex = re.compile(".*"+genre+".*", re.IGNORECASE)
    look_up = collection.count_documents({'genre': {'$in': [regex]}})
    if look_up == 0:
        os.system('clear')
        print("SORRY, NO RECORDS FOUND FOR" + genre.upper() + "!")
    else:
        os.system('clear')
        print(print("SHOWING " + str(look_up) + " RECORDS FOR " + "\"" + genre.upper() + "\""))
        print()
        songs = collection.aggregate([
            {'$match': {'genre': {'$in': [regex]}}},
            {'$group':
                {'_id': {
                    'Song': '$Song',
                    'artist': '$Performer',
                    'year': '$active_year'}}}
        ])
        for song in songs:
            print('SONG: ' + song['_id']['Song'])
            print('ARTIST: ' + song['_id']['artist'])
            print('YEAR: ' + str(song['_id']['year']))
            print()
