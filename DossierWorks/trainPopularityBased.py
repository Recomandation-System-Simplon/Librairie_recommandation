"""

Entraînement du modèle de recommandation basé sur la popularté des livres

- Luca Pelliccioli
- Anthony Marais
- Julien Bosse

29/09/2021

"""

import pandas as pd
import pyarrow.feather as feather

books = pd.read_csv("data/books.csv")
books2=books[["book_id","goodreads_book_id","title","authors","average_rating","ratings_count"]].sort_values(["average_rating","ratings_count"],ascending=False)

# Calcul de C, à partir des moyennes de notes
C = books2["average_rating"].mean()

# Calcul de m, à partir du 50ème quantile
m = books2["ratings_count"].quantile(0.50)

# On ne garde que les livres au dessus de m
books3 = books2[books2["ratings_count"]>=m].copy()

# Calcul du weighted_rating de chaque livre
v = books3["ratings_count"]
R = books3["average_rating"]

books3["weighted_rating"] = ( v/(v+m) * R )+( m/(v+m) * C )

books3 = books3.sort_values("weighted_rating",ascending=False)
feather.write_feather(books3[["book_id","goodreads_book_id","title","weighted_rating"]],"data/popularity_books")