import firebase_admin
from firebase_admin import credentials, firestore
import csv

# Inicializar la aplicación de Firebase con las credenciales
cred = credentials.Certificate('incaf-reto-firebase-adminsdk-1ax5o-db4938a50f.json')
firebase_admin.initialize_app(cred)

# Obtener una referencia a la base de datos Firestore
db = firestore.client()

# Ruta al archivo CSV
csv_file_path = '0.v5mm3ynen1a0.dp1qil2qhvhmovies.csv'

# Leer el archivo CSV y agregar cada fila a la colección 'movies'
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)  # Leer el CSV como un diccionario
    for row in reader:
        # Agregar cada fila como un documento en la colección 'movies'
        db.collection('movies').add(row)
        print(f'Document added: {row}')  # Confirmar que el documento fue agregado

print('CSV file successfully processed')  # Mensaje final al completar el proceso