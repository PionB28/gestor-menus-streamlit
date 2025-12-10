# app.py
import streamlit as st
from google import genai
import os # Para acceder a variables de entorno de forma segura

# --- CONFIGURACIÓN DE LA IA ---
try:
    # Intenta leer la clave API del panel de "Secrets" de Streamlit Cloud
    api_key = st.secrets["GEMINI_API_KEY"]
except (KeyError, FileNotFoundError):
    # Opción de respaldo si estás probando localmente o la clave no está configurada
    api_key = os.getenv("GEMINI_API_KEY") 
    
if not api_key:
    st.error("Error: La clave GEMINI_API_KEY no está configurada en Streamlit Secrets.")
    st.stop() # Detiene la ejecución si no hay clave.

client = genai.Client(api_key=api_key)
MODELO = "gemini-2.5-flash" # El modelo que usará la aplicación

# --- INTERFAZ Y PROMPT ---
st.title("🍽️ Gestor de Menús (Fase 1: Solo IA)")
st.caption("Aún falta conectar la Hoja de Google, ¡pero la IA ya funciona!")
st.markdown("---")

# 1. Definición del 'Rol' del modelo (System Prompt)
prompt_base = """
Actúa como un asistente de gestión de menús para un restaurante. Tu objetivo es procesar la solicitud del usuario 
y, si el menú actual estuviera disponible, sugerir la mejor acción. 
Responde de forma clara y profesional.
"""

user_input = st.text_area("✍️ Ingresa tu solicitud (ej: 'Sugiéreme un postre para verano')")

if st.button("Generar Respuesta"):
    if user_input:
        with st.spinner('Procesando solicitud con Gemini...'):
            full_prompt = prompt_base + "\nSolicitud del usuario: " + user_input
            
            # 2. Llamada a la API de Gemini
            try:
                response = client.models.generate_content(
                    model=MODELO,
                    contents=full_prompt
                )
                
                st.success("Respuesta de Gemini:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Ocurrió un error con la API: {e}")
            
    else:
        st.warning("Por favor, escribe una solicitud en el campo de texto.")