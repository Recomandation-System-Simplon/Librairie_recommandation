# Librairie_recommandation
Projet de recommandation de livres pour un libraire



# Installation
```console
git clone https://github.com/Recomandation-System-Simplon/Librairie_recommandation.git
cd Librairie_recommandation
```

Si anaconda installer sur votre machine :
```console
conda deactivate
```
En suite création de l'environnement de travail :
```console

python -m venv venv
```
Sur Windows exécutez :
```console
venv/Scripts/activate
```
ou sur Linux :
```console
source venv/bin/activate
```
Ensuite finir par :
```console
pip install -r requirements.txt
```

# Entraînement modèles
(peut prendre quelques minutes)
```console
python trainCollaborativeFiltering.py
python trainContentBased.py
```

# Lancer la recommandation
```console
python Recommandation.py
```