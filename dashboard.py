# imports

from plotter import song_sentiment_plotter
from queries import *


def sub_menu():
    print("\nENTER 1 FOR MAIN-MENU")
    option = input("ENTER 0 TO EXIT: ")
    os.system('clear')
    if int(option) == 1:
        main_menu()
    elif int(option) == 0:
        print("THANK YOU FOR USING \"THE BILLBOARD DATABASE\"!")
        exit(0)
    else:
        print("INVALID INPUT. PLEASE TRY AGAIN")
        sub_menu()


# user-interface method to the Mongo DataBase
def main_menu():
    print("----------------------------------WELCOME TO THE BILLBOARD DATABASE-------------------------------------")
    print("                                     1. GET SONG INFORMATION                                            ")
    print("                                     2. GET SONGS OF ARTIST IN THE DATABASE                             ")
    print("                                     3. GET SONGS OF A GENRE IN THE DATABASE                            ")
    print("                                     4. GET THE HOT CHARTS FOR A PARTICULAR YEAR (1958 - 2019)          ")
    print("                                     5. GET ALL POPULAR SONGS IN A YEAR                                 ")
    print("                                     6. GET ALL POPULAR ARTISTS IN A YEAR                               ")
    print("                                     7. GET ALL POPULAR GENRES IN A YEAR                                ")
    print("                                     8. PLOT SENTIMENT FOR SONGS                                        ")
    print("                                     9. EXIT                                                            ")
    choice = int(input("ENTER THE CHOICE: "))
    os.system('clear')

    if choice == 1:
        get_song_info()
        sub_menu()
    elif choice == 2:
        get_songs_by_performer()
        sub_menu()
    elif choice == 3:
        get_songs_by_genre()
        sub_menu()
    elif choice == 4:
        get_all_hot_charts_for_year()
        sub_menu()
    elif choice == 5:
        get_top_songs_in_year()
        sub_menu()
    elif choice == 6:
        get_top_artists_in_year()
        sub_menu()
    elif choice == 7:
        get_top_genres_in_year()
        sub_menu()
    elif choice == 8:
        song_sentiment_plotter()
        sub_menu()
    elif choice == 9:
        print("THANK YOU FOR USING \"THE BILLBOARD DATABASE\"!")
        exit(0)
    else:
        print("INVALID SELECTION, PLEASE ENTER A VALID OPTION!")
        sub_menu()


os.system('clear')
main_menu()
