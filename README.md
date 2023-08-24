# Documentation ENT Z0 actualisation MDP

## Utilisation du Code

### 1️⃣ `main.py`

**Description :**
`main.py` est utilisé pour extraire toutes les JDDs (Jeux de Données) de l'ENT Z0.

**Instructions :**
- Exécutez `main.py`.
- Laissez le code s'exécuter pendant environ 20 minutes afin de garantir la récupération de tous les JDDs.

### 2️⃣ `mdp_activate.py`

**Description :**
Ce script est à exécuter après avoir obtenu tous les JDDs avec `main.py`. Il a pour but d'actualiser les mots de mots de passes des personnes n'ayant pas encore activé leur compte.

**Instructions :**
- Après avoir attendu que `main.py` ait fini de s'exécuter, lancez `mdp_activate.py`.

### 2️⃣ `mdp_changer.py`

**Description :**
Ce script est à exécuter après avoir obtenu tous les JDDs avec `mdp_activate.py`. Il a pour but de changer les mots 

**Instructions :**
- Après avoir attendu que `main.py` et `mdp_activate.py` aient fini de s'exécuter, lancez `mdp_changer.py`.

## ⚠️ Notes importantes

- Veillez à ce que les dépendances nécessaires soient bien installées avant d'exécuter les scripts.
- Assurez-vous de vérifier les JDDs extraits avant de procéder à des modifications ultérieures avec `mdp_activate.py`.
- Assurez-vous aussi que le code `mdp_activate.py` soit bien terminé avant de lancer `mdp_changer.py`.
