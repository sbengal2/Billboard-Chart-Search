# imports
import re
import matplotlib.pyplot as plt
from pymongo import MongoClient

# connecting to Mongo DataBase
client = MongoClient('localhost', 27017, unicode_decode_error_handler='ignore')
data_base = client['billboard']
collection = data_base['songs']


# method to plot the average sentiment of songs against year
def song_sentiment_plotter():
    year_list = []
    avg_sentiment_list = []
    start_year = 1958
    end_year = 2019
    while start_year <= end_year:
        year_list.append(start_year)
        sentiment_sum = 0
        no_of_records = collection.count_documents({'active_year': start_year})
        for x in collection.find({'active_year': start_year}):
            sentiment_sum += x['Sentiment']
        avg_sentiment_list.append(sentiment_sum / no_of_records)
        start_year += 1

    plt.xlabel('Years From 1958 - 2019')
    plt.ylabel('Average Sentiment/Year')
    plt.title('Varying Sentiment Of Songs From 1958 -2019')
    plt.plot(year_list, avg_sentiment_list)
    plt.legend(loc='best')
    plt.show()


# method to plot the average sentiment of genre against year
def genre_sentiment_plotter():
    genre = {'rock':[],'metal':[],'country':[],'pop':[],'edm':[],'rap':[]}
    year_list = [1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974,
                 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991,
                 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
                 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
    for key in genre.keys():
        genre[key].append(get_genre_polairty_list(key))
    plt.xlabel('Average Genre Sentiment/Year')
    plt.ylabel('Years From 1958 - 2019')
    plt.title('Varying Sentiment Of Generic Music Genres From 1958 -2019')
    plt.barh(year_list, genre['rock'][0],color='yellow',label="Rock")
    plt.barh(year_list, genre['metal'][0],color='black',label="Metal")
    plt.barh(year_list, genre['country'][0],color='green',label="Country")
    plt.barh(year_list, genre['pop'][0],color='red',label="Pop")
    plt.barh(year_list, genre['rap'][0],color='blue',label="Rap")
    plt.barh(year_list, genre['edm'][0],color='orange',label="EDM")
    plt.legend(loc='lower right')
    plt.show()



# method to get the sentiment list for each genre
def get_genre_polairty_list(genre):
    print("Fetching results for "+ genre.upper()+"....",end='\r')
    regex = re.compile(".*"+genre+".*", re.IGNORECASE)
    avg_sentiment_list = []
    avg_sentiment_list.clear()
    start_year = 1958; end_year = 2019
    while start_year <= end_year:
        sentiment_sum = 0
        no_of_records = collection.count_documents({'active_year': start_year, 'genre': {'$in': [regex]}})
        for x in collection.find({'active_year': start_year, 'genre': {'$in': [regex]}}):
            sentiment_sum += x['Sentiment']
        if no_of_records == 0:
            avg_sentiment_list.append(0)
        else:
            avg_sentiment_list.append(sentiment_sum / no_of_records)
        start_year += 1
    return avg_sentiment_list
