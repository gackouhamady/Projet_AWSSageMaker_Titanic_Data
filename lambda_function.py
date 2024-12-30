import json
import boto3
import pandas as pd
from io import StringIO

# Initialize S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # 1. Récupérer le bucket et le key (chemin du fichier) depuis l'événement
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        # Vérifier que le fichier est dans le dossier "raw"
        if not key.startswith('raw/'):
            return {
                'statusCode': 400,
                'body': f"File {key} is not in 'raw/' folder. No action taken."
            }
        
        # 2. Télécharger le fichier depuis S3
        obj = s3.get_object(Bucket=bucket_name, Key=key)
        data = obj['Body'].read().decode('utf-8')
        
        # Charger les données dans un DataFrame
        df = pd.read_csv(StringIO(data))
        
        # 3. Traitement des données

        # - Imputer les valeurs manquantes avec la médiane pour les variables numériques
        df.fillna(df.median(numeric_only=True), inplace=True)

        # - Imputer les variables catégoriques avec la mode, sauf 'Cabin'
        for column in df.select_dtypes(include='object').columns:
            if column != 'Cabin':
                df[column].fillna(df[column].mode()[0], inplace=True)

        # - Transformer la colonne 'Cabin' en booléen : True si manquant, False sinon
        df["Cabin"] = df["Cabin"].isna()

        # 4. Extraction des variables

        # Exclure les attributs inutiles
        df.drop(["PassengerId", "Name", "Ticket"], axis="columns", inplace=True)

        # 5. Variables Encoding

        # Label Encoding pour 'Sex'
        df["Sex"] = df["Sex"].replace(["male", "female"], [0, 1])

        # One-Hot Encoding pour 'Embarked'
        df = pd.get_dummies(df, columns=['Embarked'], drop_first=True)

        # 6. Conversion des colonnes booléennes en int
        bool_columns = ['Cabin', 'Embarked_Q', 'Embarked_S']
        for column in bool_columns:
            if column in df.columns:
                df[column] = df[column].astype(int)
                
        df = pd.get_dummies(df)

        # 7. Afficher les statistiques descriptives
        stats = df.describe(include='all').to_dict()

        # 8. Sauvegarder le fichier traité dans un autre dossier (par exemple, "processed/")
        output_key = key.replace('raw/', 'processed/')
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        s3.put_object(Bucket=bucket_name, Key=output_key, Body=csv_buffer.getvalue())
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f"File {key} processed successfully.",
                'statistics': stats
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error processing file: {str(e)}"
        }

