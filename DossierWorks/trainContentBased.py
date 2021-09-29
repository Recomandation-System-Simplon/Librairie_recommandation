"""

Entrainement du modèle de recommandation basé sur le contenu.

- Luca Pelliccioli
- Anthony Marais
- Julien Bosse

29/09/2021

"""

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pyarrow.feather as feather

books = pd.read_csv("data/books.csv")
tags = pd.read_csv("data/tags.csv")
book_tags = pd.read_csv("data/book_tags.csv")

def get_tag_id(x):
    # Fonction qui trouve le tag_id en fonction du tag_name

    tag_id = tags.query('tag_name == "'+x+'"')['tag_id'].item()

    return tag_id

def get_tag_name(x):
    # Fonction qui trouve le tag_name en fonction du tag_id

    tag_name = tags.query('tag_id == '+str(x))['tag_name'].item()

    return tag_name

# On garde seulement les tags que plus de 110 personnes ont mis à un livre
book_tags_trimmed = book_tags[book_tags["count"]>=110]

# On crée la liste des tags à supprimer car inutile pour Content-Based Filtering, mais on les gardera pour le Popularity Based
tag_names_supp = [
    "to-read",
    "currently-reading",
    "favorites",
    "favorite",
    "books-i-own",
    "owned",
    "owned-books",
    "to-buy",
    "favourites",
    "my-books",
    "i-own",
    "re-read",
    "all-time-favorites",
    "favorite-books",
    "read-in-2008",
    "read-in-2009",
    "read-in-2010",
    "read-in-2011",
    "read-in-2012",
    "read-in-2013",
    "read-in-2014",
    "read-in-2015",
    "read-in-2016",
    "read-in-2017",
    "read-2009",
    "read-2010",
    "read-2011",
    "read-2012",
    "read-2013",
    "read-2014",
    "read-2015",
    "read-2016",
    "read-2017",
    "read-2009",
    "read-2010",
    "read-2011",
    "read-2012",
    "read-2013",
    "read-2014",
    "read-2015",
    "read-2016",
    "read-2017",
    "books-read-in-2012",
    "books-read-in-2014",
    "books-read-in-2015",
    "books-read-in-2016",
    "2012-reads",
    "2013-reads",
    "2014-reads",
    "2015-reads",
    "2016-reads",
    "2017-reads",
    ]

# On récupère les ids des tags à supprimer
tag_ids_supp=[]
 
for tag in tag_names_supp:
    tag_ids_supp.append(get_tag_id(tag))

# Boucle qui retire des book_tags les tags_ids
for tag_id in tag_ids_supp:
    book_tags_trimmed = book_tags_trimmed[book_tags_trimmed["tag_id"]!=int(tag_id)]

# Création d'un dataframe dans lequel une ligne correspond à un livre grâce à .unique
df = pd.DataFrame(list(book_tags_trimmed["goodreads_book_id"].unique()),columns=["book"])
df["bag_of_tags"]=" "

def create_bag(book_id):
    # Fonction qui, pour un certain livre, crée une string qui contient les ids de tous ses tags

    bag = map(str,book_tags_trimmed["tag_id"][book_tags_trimmed["goodreads_book_id"]==book_id].to_list())
    bag = " ".join(bag)

    return bag

df["bag_of_tags"] = df["book"].apply(create_bag)

# Exporter le tableau qui fait coller l'index du livre dans la matrice sim cos à son ID
feather.write_feather(df["book"].to_frame(),"data/index_books")

# A partir du bag of tags on peut utiliser countvectorizer pour créer la matrice qui nous servira a calculcer la similarité entre chaque livre
count = CountVectorizer()
count_matrice = count.fit_transform(df['bag_of_tags'])

# Création de la matrice de similarité cosinus (score entre 0 et 1) entre chaque livre
cos_sim = cosine_similarity(count_matrice, count_matrice)
np.save("data/cos_sim.npy",cos_sim)