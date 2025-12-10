# app.py
import streamlit as st
from google import genai
import os 
from io import BytesIO

# --- CONFIGURACIÓN DE LA IA (NECESARIA PARA EVITAR EL NAMEERROR) ---
try:
    # 1. Intenta leer la clave API del panel de "Secrets" de Streamlit Cloud
    api_key = st.secrets["GEMINI_API_KEY"]
except (KeyError, FileNotFoundError):
    # Opción de respaldo si la clave no está configurada
    api_key = os.getenv("GEMINI_API_KEY") 
    
if not api_key:
    st.error("Error: La clave GEMINI_API_KEY no está configurada en Streamlit Secrets.")
    st.stop() # Detiene la ejecución si no hay clave.

# Inicializa el cliente de Gemini
client = genai.Client(api_key=api_key)

# --- INTERFAZ MULTIMODAL ---
st.title("🍹 Gestor de Menús (OCR de Tragos)")
st.caption("Sube una foto del menú de tragos y la IA extraerá los datos.")
st.markdown("---")

# 1. Componente de carga de archivos
uploaded_file = st.file_uploader(
    "Sube una imagen del menú", 
    type=['png', 'jpg', 'jpeg'] # Tipos de archivo permitidos
)

# 2. Definición del 'Rol' del modelo (Tu System Prompt)
prompt_base = """
[AQUÍ VA TU TEXTO EXACTO DE LAS INSTRUCCIONES DE AI STUDIO]. 
Tu tarea es leer la imagen adjunta, identificar el nombre del trago, 
y todos sus ingredientes. Devuelve los datos en el siguiente formato:
NOMBRE_TRAGO | INGREDIENTES | PRECIO (si está visible)
"""

if uploaded_file is not None:
    # Muestra la imagen cargada
    st.image(uploaded_file, caption='Imagen cargada.', use_column_width=True)

    if st.button("Extraer Datos del Menú"):
        with st.spinner('Analizando la imagen con OCR y Gemini...'):
            
            # Convierte el archivo cargado a bytes para enviarlo a la API
            image_bytes = uploaded_file.read()
            
            # 3. LLAMADA A LA API CON IMAGEN
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[
                    {"role": "system", "parts": [{"text": prompt_base}]},
                    {"role": "user", "parts": [{"inline_data": {
                        "mime_type": uploaded_file.type,
                        "data": image_bytes
                    }}]},
                ]
            )
            
            # 4. Mostrar Resultados
            st.success("Extracción completada:")
            st.text_area("Datos Extraídos (Listos para la BD):", value=response.text, height=300)

# app.py
# ... (Todo el código anterior de configuración y Streamlit) ...

# Este código se añade AL FINAL de tu app.py, DENTRO del bloque 'if uploaded_file is not None:'

            # 4. Mostrar Resultados
            data_extraida = response.text # Guardamos el texto extraído en una variable
            st.success("Extracción completada:")
            st.text_area("Datos Extraídos (Listos para la BD):", value=data_extraida, height=300)

            # --- NUEVA SECCIÓN: FUNCIÓN PARA GUARDAR EN GOOGLE SHEETS ---

            if st.button("Guardar Datos en Google Sheets"):
                
                # LLAMA A LA FUNCIÓN DE GUARDADO
                if guardar_en_sheets(data_extraida):
                    st.balloons() # Celebración visual
                    st.success("🎉 Datos guardados exitosamente en la Hoja de Google!")
                else:
                    st.error("❌ Error al guardar datos. Revisa la configuración de la Hoja/Credenciales.")
