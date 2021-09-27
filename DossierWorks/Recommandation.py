"""

Brief Projet Simplon : Application recommandation

- Luca Pelliccioli
- Anthony Marais
- Julien Bosse


27/06/2021

"""

import pandas as pd
import numpy as np

cos_sim = np.load("data/cos_sim.npy")
index_books = pd.read_csv("data/index_books.csv")
books = pd.read_csv("data/books.csv")
popularity_books = pd.read_csv("data/popularity_books.csv")

def get_book_id(title): 
    # Récupère l'ID du livre en fonction de son titre
    return books["goodreads_book_id"][books["title"]==title].item()

def get_book_title(goodreads_id):
    # Récupère le titre du livre en fonction de son id
    return books["title"][books["goodreads_book_id"]==goodreads_id].item()

def get_book_weighted_rating(goodreads_id):
    try:
        return popularity_books["weighted_rating"][popularity_books["goodreads_book_id"]==goodreads_id].item()
    except:
        return 0

class Recommandation:
    """ Classe qui nous permettra de faire différents types de recommandations """

    def __init__(self):

        self.user_bool = True
        print("##############################")
        print("#          WELCOME           #")
        print("#      TO  OUR  BOOKSHOP     #")
        print("##############################")

        while self.user_bool == True:
            print("\n_____ New recommandation _____")
            self.is_user_new = input("\nAre you a new user (Y/N) ? ")

            if self.is_user_new == "Y":
                self.last_book = input("\nWhat is the last book your read ? ")

                try:
                    print("\nWe recommand these bestsellers books :")
                    print(self.hybrid(self.last_book))
                    
                except Exception as e:
                    print(e)
                    print("\nWe couldnt find this book in our database, anyway : here are some bestseller books we recommand : ")
                    print(self.popularitybased())

            elif self.is_user_new == "N":
                self.user = int(input("\nUser ID please : "))

            elif self.is_user_new == "0":
                self.user_bool = False

            else: 
                print("\nPlease respond with 'Y' or 'N' ")


    def popularitybased(self):
        return list(popularity_books["title"][0:5])

    def contentbased(self, title, cos_sim = cos_sim):
        # Initialise la liste de livres recommandés
        rec_books_ids = []

        # ID du livre
        book_id = self.get_book_id(title)
        
        # Index du livre dans la matrice
        idx = index_books[index_books["book"]==book_id].index[0]

        # Création de la série qui comprend la similiraté de notre livre et tous les autres (correspond à sa colonne de la matrice cos_sim)
        score_series = pd.Series(cos_sim[idx]).sort_values(ascending = False)

        # On récupère les 10 premiers indices (plus grandes similarités)
        rec_books_indexes = list(score_series.iloc[1:31].index)

        rec_books_ids = list(map(lambda x: index_books["book"][x],rec_books_indexes))

        rec_books = list(map(get_book_title, rec_books_ids))

        return list(rec_books)


    def hybrid(self, title, cos_sim = cos_sim):
        """
        Fonction recommandation :
        Prend en entrée le title d'un livre et la matrice de similarité.
        Trouve l'id du livre
        Cherche dans la matrice les autres livres similaires
        """
        
        # Initialise la liste de livres recommandés
        rec_books_ids = []

        # ID du livre
        book_id = get_book_id(title)
        
        # Index du livre dans la matrice
        idx = index_books[index_books["book"]==book_id].index[0]

        # Création de la série qui comprend la similiraté de notre livre et tous les autres (correspond à sa colonne de la matrice cos_sim)
        score_series = pd.Series(cos_sim[idx]).sort_values(ascending = False)

        # On récupère les 10 premiers indices (plus grandes similarités)
        rec_books_indexes = list(score_series.iloc[1:31].index)
        
        rec_books_ids = list(map(lambda x: index_books["book"][x],rec_books_indexes))

        # Liste des weighted ratings associés aux livres
        rec_books_wr = list(map(get_book_weighted_rating,rec_books_ids))


        rec_books = pd.DataFrame(list(zip(rec_books_ids, rec_books_wr)),columns=['id','wr'])
        rec_books = rec_books.sort_values("wr",ascending=False)
        rec_books = list(map(get_book_title,list(rec_books["id"][0:5])))

        return rec_books
    

Recommandation()