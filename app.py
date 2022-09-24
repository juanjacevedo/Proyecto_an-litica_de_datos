import pandas as pd
import numpy as np 
import matplotlib as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go 
import streamlit as st
from streamlit.components.v1 import html

##Datos
mat_ietdh = pd.read_csv('matricula_IETDH.csv')
mat_me = pd.read_csv('MEN_MATRICULA_ESTADISTICA_ES(1).csv')
men_es = pd.read_csv('MEN_INSTITUCIONES_EDUCACI_N_SUPERIOR.csv')
men_ietdh = pd.read_csv('MEN_INSTITUCIONES_EDUCACI_N_PARA_EL_TRABAJO_Y_EL_DESARROLLO_HUMANO.csv')
coord = pd.read_csv('co.csv')

#Se crea una función para eliminar las tildes
def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b)
    return s


st.markdown("<h1 style='text-align: center; color: #1D3557;'>Educación superior y educación para el trabajo y el desarrollo humano en Colombia </h1>", unsafe_allow_html=True)

#Se crea la bodega de datos para Matricula IETDH
x = ['Secretaría', 'Código Institución', 'Nombre Institución','Estado Institución', 'Departamento','Municipio', ' Total Matrícula 2010 ',' Total Matrícula 2011 ', ' Total Matrícula 2012 ',' Total Matrícula 2013 ', ' Total Matrícula 2014 ', ' Total Matrícula 2015 ', ' Total Matrícula 2016 ',' Total Matrícula 2017 ', ' Total Matrícula 2018 ',' Total Matrícula 2019 ', ' Total Matrícula 2020 ',' Total Matrícula 2021 ']
datos = []
for i in x:
  datos.append(mat_ietdh[i])
mat_ietdh2 = pd.DataFrame(datos).transpose()

mat_ietdh2.columns = map(str.upper, mat_ietdh2.columns)

#Se coloca en minuscula las variables de la bodega de datos
x = ['SECRETARÍA','NOMBRE INSTITUCIÓN', 'ESTADO INSTITUCIÓN','DEPARTAMENTO', 'MUNICIPIO']
for i in x:
  mat_ietdh2[i] = mat_ietdh2[i].str.lower().apply(normalize)
mat_ietdh2.head()

#Corregir el nombre de los 'MUNICIPIO'
municipio = ['mompos', 'bogota']

cambio = ['mompox', 'bogota d.c']

for i,j in zip(municipio,cambio):
    mat_ietdh2['MUNICIPIO'] = mat_ietdh2['MUNICIPIO'].replace(i,j)
mat_ietdh2['MUNICIPIO'].unique()

#Corregir el nombre de los 'DEPARTAMENTO'
departamentos = ['la guajira','archipielago de san andres, providencia y santa catalina','bogota d.c.']

cambio = ['guajira','san andres y providencia','bogota d.c']

for i,j in zip(departamentos,cambio):
    mat_ietdh2['DEPARTAMENTO'] = mat_ietdh2['DEPARTAMENTO'].replace(i,j)
mat_ietdh2['DEPARTAMENTO'].unique()

#Se convierten en enteros las variables númericas. 
x = ['CÓDIGO INSTITUCIÓN', ' TOTAL MATRÍCULA 2010 ',
' TOTAL MATRÍCULA 2011 ',
' TOTAL MATRÍCULA 2012 ',
' TOTAL MATRÍCULA 2013 ',
' TOTAL MATRÍCULA 2014 ',
' TOTAL MATRÍCULA 2015 ',
' TOTAL MATRÍCULA 2016 ',
' TOTAL MATRÍCULA 2017 ',
' TOTAL MATRÍCULA 2018 ',
' TOTAL MATRÍCULA 2019 ',
' TOTAL MATRÍCULA 2020 ',
' TOTAL MATRÍCULA 2021 ']
for i in x:
  mat_ietdh2[i] = mat_ietdh2[i].astype('int64')

# # Define your javascript
# my_js = """
# alert("Hola mundo");
# """

# # Wrapt the javascript as html code
# my_html = f"<script>{my_js}</script>"

# # Execute your app
# st.title("Javascript example")
# html(my_html)