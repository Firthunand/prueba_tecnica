import openai
import mysql.connector
import pandas as pd

# Configura tu clave de API de OpenAI
openai.api_key = ''

#Conexión a la base de datos
my_conn = mysql.connector.connect(
        host='',
        user='',
        password='',
        database=''
    )
cursor = my_conn.cursor()
cursor.execute("SELECT * FROM encuesta")
row = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(row, columns=columns)
my_conn.close()


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

respuestas_abiertas = df['recomendacion_abierta'].dropna().tolist()
respuestas_formateadas = "\n".join([f"- {resp}" for resp in respuestas_abiertas])    
respuesta=None
pregunta = input("¿Cual es tu pregunta? : ") 
respuesta = interaccion_Gpt(pregunta,respuestas_formateadas)
print(respuesta)


