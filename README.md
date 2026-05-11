# 🌍 FinScope East Africa — Inclusion Financière Numérique

Application d'analyse exploratoire (EDA) sur l'inclusion financière et numérique en Afrique de l'Est, développée avec Streamlit.

## 📊 À propos

Cette application explore les données de **10 086 répondants** répartis dans **4 pays** (Kenya, Rwanda, Tanzanie, Ouganda) pour analyser :
- Les dynamiques d'accès aux services financiers numériques
- Les inégalités socio-économiques et de genre
- Les leviers de développement de l'inclusion financière

## 🗂️ Structure de l'application

| Section | Contenu |
|---|---|
| 🏠 Dashboard | Vue d'ensemble des KPIs clés |
| 👥 Q1. Démographie | Répartition par pays, âge et genre |
| 📱 Q2. Inclusion Numérique | Accès au téléphone par pays, zone et genre |
| 💼 Q3. Socio-Économique | Croisement éducation × emploi |
| 👨‍👩‍👧 Q4. Ménages | Taille des ménages et taux de dépendance |
| 🔍 Q5. Comportements | Patterns et corrélations multivariées |
| 📋 Q6. Synthèse Exécutive | KPIs, profils de risque, recommandations |

## 📈 Principaux résultats

- **74,9 %** de l'échantillon a accès à un téléphone mobile
- **Rwanda** : meilleur taux d'accès (83,1 %) — **Tanzanie** : plus en retard (60,5 %)
- Écart de genre de **7,8 points** (hommes 79,5 % vs femmes 71,7 %)
- **318 personnes ultra-vulnérables** (femmes + sans éducation + emploi informel)
- Résultat contre-intuitif : les zones **rurales** ont un meilleur accès que les urbaines (77,5 % vs 71,0 %)

## 🚀 Lancer l'application localement

```bash
# Cloner le dépôt
git clone https://github.com/MLG-20/finscope-east-africa.git
cd finscope-east-africa

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'app
streamlit run application_streamlit.py
```

## 📦 Dépendances

- [Streamlit](https://streamlit.io/) 1.57
- [Plotly](https://plotly.com/) 6.7
- [Pandas](https://pandas.pydata.org/) 3.0
- [NumPy](https://numpy.org/) 2.4
- [SciPy](https://scipy.org/) 1.17

## 📁 Données

| Fichier | Description |
|---|---|
| `Test.csv` | Données principales — 10 086 répondants |
| `VariableDefinitions.csv` | Dictionnaire des variables |

Source : [FinScope East Africa — Kaggle](https://www.kaggle.com/)

## 👤 Auteur

**MLG-20** — [GitHub](https://github.com/MLG-20)
