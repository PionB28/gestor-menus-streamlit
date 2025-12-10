{\rtf1\ansi\ansicpg1252\cocoartf2759
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww44600\viewh22420\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # app.py\
import streamlit as st\
from google import genai\
import os # Para acceder a variables de entorno de forma segura\
\
# --- CONFIGURACI\'d3N DE LA IA ---\
try:\
    # Intenta leer la clave API del panel de "Secrets" de Streamlit Cloud\
    api_key = st.secrets["GEMINI_API_KEY"]\
except (KeyError, FileNotFoundError):\
    # Opci\'f3n de respaldo si est\'e1s probando localmente o la clave no est\'e1 configurada\
    api_key = os.getenv("GEMINI_API_KEY") \
    \
if not api_key:\
    st.error("Error: La clave GEMINI_API_KEY no est\'e1 configurada en Streamlit Secrets.")\
    st.stop() # Detiene la ejecuci\'f3n si no hay clave.\
\
client = genai.Client(api_key=api_key)\
MODELO = "gemini-2.5-flash" # El modelo que usar\'e1 la aplicaci\'f3n\
\
# --- INTERFAZ Y PROMPT ---\
st.title("\uc0\u55356 \u57213 \u65039  Gestor de Men\'fas (Fase 1: Solo IA)")\
st.caption("A\'fan falta conectar la Hoja de Google, \'a1pero la IA ya funciona!")\
st.markdown("---")\
\
# 1. Definici\'f3n del 'Rol' del modelo (System Prompt)\
prompt_base = """\
Act\'faa como un asistente de gesti\'f3n de men\'fas para un restaurante. Tu objetivo es procesar la solicitud del usuario \
y, si el men\'fa actual estuviera disponible, sugerir la mejor acci\'f3n. \
Responde de forma clara y profesional.\
"""\
\
user_input = st.text_area("\uc0\u9997 \u65039  Ingresa tu solicitud (ej: 'Sugi\'e9reme un postre para verano')")\
\
if st.button("Generar Respuesta"):\
    if user_input:\
        with st.spinner('Procesando solicitud con Gemini...'):\
            full_prompt = prompt_base + "\\nSolicitud del usuario: " + user_input\
            \
            # 2. Llamada a la API de Gemini\
            try:\
                response = client.models.generate_content(\
                    model=MODELO,\
                    contents=full_prompt\
                )\
                \
                st.success("Respuesta de Gemini:")\
                st.markdown(response.text)\
                \
            except Exception as e:\
                st.error(f"Ocurri\'f3 un error con la API: \{e\}")\
            \
    else:\
        st.warning("Por favor, escribe una solicitud en el campo de texto.")}