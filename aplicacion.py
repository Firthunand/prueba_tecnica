from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import pandas as pd
import openai

app = Flask(__name__)

# Configura tu clave de API de OpenAI
openai.api_key = ''

# Conexión a la base de datos
my_conn = mysql.connector.connect(
        host='',
        user='root',
        password='',
        database=''
    )
cursor = my_conn.cursor()
cursor.execute("SELECT * FROM encuesta")
row = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(row, columns=columns)
my_conn.close()


# Función para calcular el SNG
def calculoSng(satisfaccion_general):
    satisfaccion = satisfaccion_general[satisfaccion_general >= 6].count()
    neutros = satisfaccion_general[satisfaccion_general == 5].count()
    insatisfaccion = satisfaccion_general[(satisfaccion_general >= 1) & (satisfaccion_general <= 4)].count()
    total_encuestados = satisfaccion + neutros + insatisfaccion
    sng = round((satisfaccion - insatisfaccion) * 100 / total_encuestados)
    return sng

# Función para interactuar con GPT
def interaccion_Gpt(pregunta, respuestas):
    respuesta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un asistente útil."},
            {"role": "user", "content": f"Pregunta: {pregunta}\nRespuestas:\n{respuestas}\n¿Cómo puedo ayudarte?"}
        ],
        max_tokens=1024,
        temperature=0.5,
    )
    return respuesta.choices[0].message["content"]

## formulario preguntas
@app.route('/', methods=['POST','GET'])
def formulario():
    
    respuestas_abiertas = df['recomendacion_abierta'].dropna().tolist()
    respuestas_formateadas = "\n".join([f"- {resp}" for resp in respuestas_abiertas])
    
    respuesta=None
    if request.method == "POST":
        pregunta=request.form['pregunta']
        
        respuesta = interaccion_Gpt(pregunta,respuestas_formateadas)        
    
    return render_template('formulario.html', respuesta=respuesta)
    
    

