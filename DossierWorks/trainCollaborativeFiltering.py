"""

Entraînement du modèle de recommandation basé sur le filtrage collaboratif

- Luca Pelliccioli
- Anthony Marais
- Julien Bosse

29/09/2021

"""

import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
from scipy.linalg import sqrtm
import pyarrow.feather as feather

books = pd.read_csv("data/books.csv")
ratings = pd.read_csv("data/ratings.csv")

# Création de la table user // book avec les notes déjà données
R_df = ratings.pivot(index="user_id",columns="book_id",values="rating").fillna(0)

# on récupère seulement les valeurs pour le svds
R = R_df.values

# Calcul la moyenne des notes mise par chaque user, pour la retirer (on la rajoutera à la fin)
user_ratings_mean = np.mean(R, axis=1)
user_ratings_mean = np.float16(user_ratings_mean)
R_demeaned = R - user_ratings_mean.reshape(-1, 1)

latent_dimension = 90 # Après une étude sur cette valeur (de 90 à 110) et sur l'erreur myenne et écart type prediction - note réelle, on a décidé de prendre 90 (rapport erreur/temps de calcul)

U, sigma, Vt = svds(R_demeaned, k=latent_dimension) 

sigma = np.diag(sigma)
s_root = sqrtm(sigma)

Usk = np.dot(U, s_root)
Usk = np.float16(Usk) # Passage float64 à float16

skV = np.dot(s_root, Vt)
skV = np.float16(skV) # Passage float64 à float16

predicted_rating = np.dot(Usk, skV) # Calcul des notes de chaque user pour chaque livre

predicted_rating = predicted_rating + user_ratings_mean.reshape(-1, 1) # On rajoute la moyenne

preds_df = pd.DataFrame(predicted_rating, columns=R_df.columns, index=R_df.index)

# Exporter les prédictions pour les usitliser dans Recommandation.py
feather.write_feather(preds_df,"data/predicted_ratings")