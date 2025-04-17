# Machine Learning on AWS: Titanic Survivors Prediction

## Contexte du projet
Projet réalisé en trinôme dans le cadre du Master 1 "Machine Learning pour la Science des Données" à l'Université Paris Cité, pour le module **Introduction au Cloud AWS**.

**Membres de l'équipe** :
- Ouarda Boumansour
- Hamady Gackou
- Omar Namous

**Encadrante** :
- Meriem Ouaret


## Objectif du projet
Concevoir un pipeline complet de machine learning sur AWS pour prédire les survivants du Titanic en utilisant les services cloud suivants :
- **Amazon S3** pour le stockage des données,
- **AWS Lambda** pour le traitement automatisé,
- **Amazon SageMaker** pour l'entraînement, le déploiement et l'inférence du modèle.


## Compétences Clés Mises en Œuvre
- Configuration d'environnements sécurisés sur AWS avec IAM.
- Stockage de données structurées sur Amazon S3.
- Automatisation du pré-traitement de données avec AWS Lambda (Python + Pandas).
- Construction, entraînement et évaluation d'un modèle XGBoost sur Amazon SageMaker.
- Réalisation d'inférences par lot (« batch transform ») et calcul d'accuracy.
- Surveillance avancée avec Amazon CloudWatch (logs et métriques).


---

## Démarche Technique Détaillée

### 1. Configuration Initiale AWS
- Création d'utilisateurs IAM et de rôles personnalisés suivant le principe du moindre privilège.
- Attribution de permissions gérées : AmazonS3FullAccess, AmazonSageMakerFullAccess, AWSLambdaFullAccess, CloudWatchFullAccess.
- Gestion des politiques IAM sur mesure pour créer et attacher des rôles sécurisés.

### 2. Gestion du stockage avec S3
- Création d'un bucket S3 structurant les données en dossiers `raw/` et `processed/`.
- Importation des données Titanic CSV et organisation rigoureuse des fichiers.

### 3. Pré-traitement automatisé via AWS Lambda
- Fonction Lambda déclenchée automatiquement à chaque upload dans S3.
- Traitement avancé des données :
  - Imputation des valeurs manquantes (médiane / mode).
  - Suppression des colonnes non pertinentes.
  - Encodage des variables catégorielles (Label Encoding, One-Hot Encoding).
  - Calcul de statistiques descriptives : moyennes, écart-types, skewness, kurtosis.
- Enregistrement automatique du jeu de données préparé dans `processed/` sur S3.

### 4. Entraînement Machine Learning avec Amazon SageMaker
- Préparation d'une instance de notebook (ml.t3.medium, offre gratuite).
- Séparation des données en train/test (80/20) et sauvegarde dans S3.
- Configuration et entraînement d'un modèle **XGBoost** avec hyperparamètres personnalisés :
  - Objectif : Binary Logistic
  - Max depth = 5, Learning rate (eta) = 0.2
  - 100 époques d'entraînement.
- Suivi du training via CloudWatch (monitoring des jobs).

### 5. Inférence et Evaluation
- Déploiement de l'artifact du modèle XGBoost.
- Réalisation de prédictions en lot avec **Batch Transform**.
- Evaluation de la performance :
  - **Accuracy obtenue** : **83%**
  - Validation par vérification croissée des prédictions contre les étiquettes réelles.


---

## Points Forts du Projet
- **Expérience complète cloud AWS** : IAM, S3, Lambda, SageMaker, CloudWatch.
- **Approche Data Engineering + Machine Learning** : Préparation, entraînement, déploiement.
- **Sécurité avancée** : Gestion des permissions précises pour minimiser les risques.
- **Automatisation de bout en bout** : Traitement, Entraînement et Inférence sans intervention manuelle.
- **Optimisation coûts AWS** : Choix pertinent des instances et stratégies batch.


## Technologies Utilisées
- **AWS** : IAM, S3, Lambda, CloudWatch, SageMaker
- **Machine Learning** : XGBoost (AWS SageMaker)
- **Programmation** : Python (Pandas, Scikit-learn), Boto3
- **Cloud Automation** : Trigger S3 → Lambda


---

## Conclusion
Ce projet a démontré notre capacité à construire un système de machine learning scalable, sécurisé et automatisé sur le cloud AWS. Il illustre une maîtrise des bonnes pratiques DevOps & DataOps, et constitue une expérience très valorisante pour tout poste lié à la data science, au cloud engineering, ou au machine learning industriel.

