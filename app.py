import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st
from streamlit.components.v1 import html
import geojson as gj
import requests as rq
import pydeck as pdk
import math

# Datos
mat_ietdh = pd.read_csv('matricula_IETDH.csv')
mat_me = pd.read_csv('MEN_MATRICULA_ESTADISTICA_ES(1).csv')
men_es = pd.read_csv('MEN_INSTITUCIONES_EDUCACI_N_SUPERIOR.csv')
men_ietdh = pd.read_csv(
    'MEN_INSTITUCIONES_EDUCACI_N_PARA_EL_TRABAJO_Y_EL_DESARROLLO_HUMANO.csv')
coord = pd.read_csv('co.csv')

# Se crea una función para eliminar las tildes


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

# Coordenadas


# Se pone en mayuscula todas las columnas
coord.columns = map(str.upper, coord.columns)
coord['CITY'] = coord['CITY'].str.lower()
coord['CITY'] = coord['CITY'].str.lower().apply(normalize)
coord.rename(columns={'CITY': 'MUNICIPIO'}, inplace=True)
coorde = pd.DataFrame()
coorde['MUNICIPIO'] = coord['MUNICIPIO']
coorde['LAT'] = coord['LAT']
coorde['LNG'] = coord['LNG']


# Matricula IETDH

# Se crea la bodega de datos para Matricula IETDH
x = ['Secretaría', 'Código Institución', 'Nombre Institución', 'Estado Institución', 'Departamento', 'Municipio', ' Total Matrícula 2010 ', ' Total Matrícula 2011 ', ' Total Matrícula 2012 ', ' Total Matrícula 2013 ',
     ' Total Matrícula 2014 ', ' Total Matrícula 2015 ', ' Total Matrícula 2016 ', ' Total Matrícula 2017 ', ' Total Matrícula 2018 ', ' Total Matrícula 2019 ', ' Total Matrícula 2020 ', ' Total Matrícula 2021 ']
datos = []
for i in x:
    datos.append(mat_ietdh[i])
mat_ietdh2 = pd.DataFrame(datos).transpose()

mat_ietdh2.columns = map(str.upper, mat_ietdh2.columns)

# Se coloca en minuscula las variables de la bodega de datos
x = ['SECRETARÍA', 'NOMBRE INSTITUCIÓN',
     'ESTADO INSTITUCIÓN', 'DEPARTAMENTO', 'MUNICIPIO']
for i in x:
    mat_ietdh2[i] = mat_ietdh2[i].str.lower().apply(normalize)
mat_ietdh2.head()

# Corregir el nombre de los 'MUNICIPIO'
municipio = ['mompos', 'bogota']

cambio = ['mompox', 'bogota d.c']

for i, j in zip(municipio, cambio):
    mat_ietdh2['MUNICIPIO'] = mat_ietdh2['MUNICIPIO'].replace(i, j)
mat_ietdh2['MUNICIPIO'].unique()

# Corregir el nombre de los 'DEPARTAMENTO'
departamentos = [
    'la guajira', 'archipielago de san andres, providencia y santa catalina', 'bogota d.c.']

cambio = ['guajira', 'san andres y providencia', 'bogota d.c']

for i, j in zip(departamentos, cambio):
    mat_ietdh2['DEPARTAMENTO'] = mat_ietdh2['DEPARTAMENTO'].replace(i, j)
mat_ietdh2['DEPARTAMENTO'].unique()

# Se convierten en enteros las variables númericas.
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


# Matricula ES

# Se crea las bodegas de datos con las columnnas de interes
x = ['x|Código de la Institución', 'Institución de Educación Superior (IES)', 'Código del departamento(IES)', 'Departamento de domicilio de la IES',
     'Código del Municipio(IES)', 'Municipio dedomicilio de la IES', 'Año', 'Total Matriculados']
datos = []
for i in x:
    datos.append(mat_me[i])
mat_meta = pd.DataFrame(datos).transpose()

# Se pone en mayuscula todas las columnas
mat_meta.columns = map(str.upper, mat_meta.columns)

# Se renombran las columnas
mat_meta.rename(columns={'X|CÓDIGO DE LA INSTITUCIÓN': 'CODIGO INSTITUCION', 'INSTITUCIÓN DE EDUCACIÓN SUPERIOR (IES)': 'INSTITUCION DE EDUCACION SUPERIOR', 'CÓDIGO DEL DEPARTAMENTO(IES)': 'CODIGO DEPARTAMENTO',
                'DEPARTAMENTO DE DOMICILIO DE LA IES': 'DEPARTAMENTO DOMICILIO', 'CÓDIGO DEL MUNICIPIO(IES)': 'CODIGO MUNICIPIO', 'MUNICIPIO DEDOMICILIO DE LA IES': 'MUNICIPIO DOMICILIO'}, inplace=True)

# Se ponen las variables en minuscula y se le quitan tildes
x = ['INSTITUCION DE EDUCACION SUPERIOR', 'DEPARTAMENTO DOMICILIO',
     'MUNICIPIO DOMICILIO']
for i in x:
    mat_meta[i] = mat_meta[i].str.lower().apply(normalize)

    # Corregir el nombre de los MUNICIPIO DOMICILIO
municipio = ['bogota d.c.', 'aca?a', 'espinal (chicoral)', 'santa fe de antioqu', 'coveas (sucre)', 'el carmen de vibora', 'santafe de bogota',
             'oca?a', 'rcoveñas', 'santa fe de antioquia', 'guadalajara de buga', 'san jose de cucuta', 'villa de san diego']

cambio = ['bogota d.c', 'ocaña', 'espinal', 'santa fe de antioquia', 'rcoveñas', 'el carmen de viboral',
          'bogota d.c', 'ocaña', 'coveñas',  'santafe de antioquia', 'buga', 'cucuta', 'ubate']

for i, j in zip(municipio, cambio):
    mat_meta['MUNICIPIO DOMICILIO'] = mat_meta['MUNICIPIO DOMICILIO'].replace(
        i, j)

# Corregir el nombre de los DEPARTAMENTO DOMICILIO
departamentos = ['narino', 'la guajira', 'bogota d.c', 'bogota d.c.', 'san andres y provi', 'narinio', 'archipielago de sa',
                 'archipielago de san andres providencia y santa catalina']

cambio = ['nariño', 'guajira', 'bogota d.c', 'bogota d.c', 'san andres y providencia',
          'nariño', 'san andres y providencia', 'san andres y providencia']

for i, j in zip(departamentos, cambio):
    #  for j in cambio:
    mat_meta['DEPARTAMENTO DOMICILIO'] = mat_meta['DEPARTAMENTO DOMICILIO'].replace(
        i, j)
mat_meta['DEPARTAMENTO DOMICILIO'].unique()

# Se convierten en enteros las variables númericas.
x = ['CODIGO INSTITUCION', 'CODIGO DEPARTAMENTO',
     'CODIGO MUNICIPIO', 'AÑO', 'TOTAL MATRICULADOS']
for i in x:
    mat_meta[i] = mat_meta[i].astype('int64')

# Instituciones de educación superior

# Se crea una bodega de datos con las variables de interes
x = ['Código Institución', 'Nombre Institución', 'Principal/Seccional', 'Naturaleza Jurídica', 'Sector',
     'Carácter Académico', 'Departamento Domicilio', 'Municipio Domicilio', '¿Acreditada Alta Calidad?']
datos = []
for i in x:
    datos.append(men_es[i])
men_esta = pd.DataFrame(datos).transpose()

# Se ponen en mayuscula las columnas
men_esta.columns = map(str.upper, men_esta.columns)

# Se colocan las variables en minuscula y se le quitan las tildes
x = ['NOMBRE INSTITUCIÓN', 'PRINCIPAL/SECCIONAL',
     'NATURALEZA JURÍDICA', 'SECTOR', 'CARÁCTER ACADÉMICO',
     'DEPARTAMENTO DOMICILIO', 'MUNICIPIO DOMICILIO',
     '¿ACREDITADA ALTA CALIDAD?']
for i in x:
    men_esta[i] = men_esta[i].str.lower().apply(normalize)

# Se renombra una variable
men_esta['CARÁCTER ACADÉMICO'] = men_esta['CARÁCTER ACADÉMICO'].replace(
    'institucion universitaria/escuela tecnologica', 'escuela tecnologica')

# Se convierten en enteros las variables númericas.
x = ['CÓDIGO INSTITUCIÓN']
for i in x:
    men_esta[i] = men_esta[i].astype('int64')

naturaleza = ['privado']

cambio = ['privada']

for i, j in zip(naturaleza, cambio):
    men_esta['SECTOR'] = men_esta['SECTOR'].replace(i, j)

# Se renombra columna
men_esta.rename(columns={'MUNICIPIO DOMICILIO': 'MUNICIPIO'}, inplace=True)

men_esta = pd.merge(men_esta, coorde, on='MUNICIPIO', how='left').dropna()

conteo = men_esta.groupby(['MUNICIPIO']).count().reset_index()
count = pd.DataFrame()
count['MUNICIPIO'] = conteo['MUNICIPIO']
count['CONTEO'] = conteo['DEPARTAMENTO DOMICILIO']
men_esta = pd.merge(men_esta, count, on = 'MUNICIPIO', how = 'left')


# IETDH

x = ['secretaria', 'codigo_institucion', 'nombre_institucion', 'cod_dpto',
     'departamento', 'cod_mpio', 'municipio', 'naturaleza', 'certificado_calidad']
datos = []
for i in x:
    datos.append(men_ietdh[i])
men_ietdh2 = pd.DataFrame(datos).transpose()

# Se pone en mayuscula todas las columnas
men_ietdh2.columns = map(str.upper, men_ietdh2.columns)

# Se ponen las variables en minuscula y se le quitan tildes
x = ['SECRETARIA', 'NOMBRE_INSTITUCION',
     'DEPARTAMENTO', 'MUNICIPIO', 'NATURALEZA',
     'CERTIFICADO_CALIDAD']
for i in x:
    men_ietdh2[i] = men_ietdh2[i].str.lower().apply(normalize)

# Se convierten en enteros las variables númericas.
x = ['CODIGO_INSTITUCION', 'COD_DPTO', 'COD_MPIO']
for i in x:
    men_ietdh2[i] = men_ietdh2[i].astype('int64')

men_ietdh2 = pd.merge(men_ietdh2, coorde, on='MUNICIPIO', how='left').dropna()
# ----------------------------------------------------------------------------------

# DASH


# # Define your javascript
# my_js = """
# alert("Hola mundo");
# """

# # Wrapt the javascript as html code
# my_html = f"<script>{my_js}</script>"

# # Execute your app
# st.title("Javascript example")
# html(my_html)

st.markdown("<h1 style='text-align: center;'>Educación superior y educación para el trabajo y el desarrollo humano en Colombia </h1>", unsafe_allow_html=True)


tab1, tab2 = st.tabs(["INSTITUCIONES DE EDUCACIÓN SUPERIOR", "INSTITUCIONES EDUCATIVAS PARA EL TRABAJO Y EL DESARROLLO HUMANO"])

with tab1:
    col1, col2 = st.columns([3, 1])

    df = pd.DataFrame()
    df['lat'] = men_ietdh2['LAT']
    df['lon'] = men_ietdh2['LNG']

    col1.map(df)

    col2.subheader("A narrow column with the data")
    col2.write(df)
    # st.header("A cat")
    # st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
    col1, col2 = st.columns([3, 1])
    men_esta['COORDENADAS'] = men_esta['LAT'].astype(str) + ', ' + men_esta['LNG'].astype(str)

    df = pd.DataFrame()
    df['lat'] = men_esta['LAT']
    df['lon'] = men_esta['LNG']

    col1.map(df)

    col2.subheader("A narrow column with the data")
    col2.write(df)

    # SCATTERPLOT_LAYER_DATA = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/bart-stations.json"
    # df = pd.read_json(SCATTERPLOT_LAYER_DATA)

    # # Use pandas to calculate additional data
    # df["exits_radius"] = df["exits"].apply(lambda exits_count: math.sqrt(exits_count))

    # Define a layer to display on a map
    layer = pdk.Layer(
        "ScatterplotLayer",
        men_esta,
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_scale=6,
        radius_min_pixels=1,
        radius_max_pixels=100,
        line_width_min_pixels=1,
        get_position="COORDENADAS",
        get_radius="CONTEO",
        get_fill_color=[255, 140, 0],
        get_line_color=[0, 0, 0],
    )

    # Set the viewport location
    view_state = pdk.ViewState(latitude=4.495415131183657, longitude=-73.5789506384306, zoom=2, bearing=0, pitch=0)

    # Render
    r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{name}\n{address}"})
    r.to_html("scatterplot_layer.html")
    col1.write(r)