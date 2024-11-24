import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
from google.oauth2 import service_account
import json

# --- Configuración de Firebase ---
if not firebase_admin._apps:  # Verifica si Firebase ya está inicializado
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    
db = firestore.Client(credentials=creds, project="incaf-reto")

# --- Función para cargar datos desde Firestore ---
@st.cache_data  # Cache para mejorar rendimiento
def load_data():
    docs = db.collection('movies').stream()
    return pd.DataFrame([doc.to_dict() for doc in docs])

# Cargar datos
df = load_data()

# --- Título principal del Dashboard ---
st.title("Dashboard de Películas")

# --- Checkbox para mostrar todas las Películas ---
if st.sidebar.checkbox('Mostrar todas las Películas'):
    st.header("Lista de Películas")
    st.dataframe(df)

# --- Búsqueda por título ---
search_term = st.sidebar.text_input("Buscar por título:")
if st.sidebar.button("Buscar"):
    if search_term:
        results = df[df['name'].str.contains(search_term, case=False)]
        st.header(f"Resultados para: '{search_term}'")
        st.dataframe(results)
    else:
        st.warning("Por favor, ingresa un título para buscar.")

# --- Filtrado por director ---
director = st.sidebar.selectbox('Selecciona un director', df['director'].unique())
if st.sidebar.button("Filtrar por director"):
    filtered = df[df['director'] == director]
    st.header(f"Películas dirigidos por {director}")
    st.write(f"Total de Películas: {len(filtered)}")
    st.dataframe(filtered)

# --- Formulario para agregar un nueva Película ---
st.sidebar.header("Agregar una nueva Película")
with st.sidebar.form("form"):
    new_title = st.text_input("Título:")
    new_director = st.text_input("Director:")
    new_genre = st.text_input("Género:")
    new_company = st.text_input("Compañia:")
    submitted = st.form_submit_button("Agregar Película")
    if submitted:
        if new_title and new_director:
            db.collection('movies').add({'name': new_title, 'director': new_director, 'genre': new_genre, 'company': new_company})
            st.sidebar.success(f"Película '{new_title}' agregada con éxito.")
            st.cache_data.clear()  # Limpiar caché para forzar recarga
            st.rerun()  # Recargar la app para mostrar nuevos datos
        else:
            st.sidebar.error("Por favor, completa todos los campos.")

# --- Footer ---
st.markdown("---")
st.markdown("**Dashboard desarrollado con Streamlit y Firestore**")

