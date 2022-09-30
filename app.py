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
coord = pd.read_csv('co.csv')
mat_ietdh2 = pd.read_csv('mat_ietdh2.csv')
mat_ietdh2 = mat_ietdh2.drop(['Unnamed: 0'], axis = 1)
mat_meta = pd.read_csv('mat_meta.csv')
mat_meta = mat_meta.drop(['Unnamed: 0'], axis = 1)
men_esta = pd.read_csv('men_esta.csv')
men_esta = men_esta.drop(['Unnamed: 0'], axis = 1)
men_ietdh2 = pd.read_csv('men_ietdh2.csv')
men_ietdh2 = men_ietdh2.drop(['Unnamed: 0'], axis = 1)

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


tab1, tab2, tab3= st.tabs(["IETDH", "INSTITUCIONES DE EDUCACIÓN SUPERIOR",'ESTADISTICAS'])

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

with tab2:
    col1, col2 = st.columns([3, 1])
    men_esta['COORDENADAS'] = men_esta['LAT'].astype(str) + ', ' + men_esta['LNG'].astype(str)

    df = pd.DataFrame()
    df['lat'] = men_esta['LAT']
    df['lon'] = men_esta['LNG']

    col1.map(df)

    col2.subheader("A narrow column with the data")
    col2.write(df)

    # Set the viewport location
    view_state = pdk.ViewState(latitude=4.495415131183657, longitude=-73.5789506384306, zoom=2, bearing=0, pitch=0)

    # Render

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

with tab3:
    col1, col2 = st.columns([2,1])
    #Metodo para remodelar o transformar un DataFrame existente 
    #Metodo para remodelar o transformar un DataFrame existente
    mat_ietdh2_2 = pd.melt(mat_ietdh2, id_vars = ['SECRETARÍA', 'CÓDIGO INSTITUCIÓN', 'NOMBRE INSTITUCIÓN', 'ESTADO INSTITUCIÓN', 'DEPARTAMENTO', 'MUNICIPIO'])

    #Corregir el nombre de los 'DEPARTAMENTO'
    año = [' TOTAL MATRÍCULA 2010 ', ' TOTAL MATRÍCULA 2011 ',
        ' TOTAL MATRÍCULA 2012 ', ' TOTAL MATRÍCULA 2013 ',
        ' TOTAL MATRÍCULA 2014 ', ' TOTAL MATRÍCULA 2015 ',
        ' TOTAL MATRÍCULA 2016 ', ' TOTAL MATRÍCULA 2017 ',
        ' TOTAL MATRÍCULA 2018 ', ' TOTAL MATRÍCULA 2019 ',
        ' TOTAL MATRÍCULA 2020 ', ' TOTAL MATRÍCULA 2021 ']

    cambio = ['2010', '2011', '2012', '2013', '2014', '2015','2016', '2017', '2018', '2019', '2020', '2021']

    for i,j in zip(año,cambio):
        mat_ietdh2_2['variable'] = mat_ietdh2_2['variable'].replace(i,j)

    mat_ietdh2_2.rename(columns = {'variable':'AÑO', 'value' : 'TOTAL MATRICULADOS'}, inplace = True)

    ##Crear diagrama de barras para la 2 base de datos opcional
    # crear dataset
    df2 = mat_ietdh2_2.groupby(['AÑO'])[['TOTAL MATRICULADOS']].sum().reset_index()

    fig = px.bar(df2, x='AÑO', y='TOTAL MATRICULADOS', title ='<b>Total matriculados en instituciones de educación para el trabajo y el desarrollo humano<b>', height=400, width=1000)

    # agregar detalles a la gráfica
    fig.update_layout(
        xaxis_title = 'Año',
        yaxis_title = 'Total matriculado',
        template = 'simple_white',
        title_x = 0.5)

    col1.write(fig)

    # col1.write(mat_ietdh2_2)
    # crear dataset
    base = men_esta.groupby(['¿ACREDITADA ALTA CALIDAD?'])[['CARÁCTER ACADÉMICO']].count().reset_index()

    # crear gráfica
    fig = px.pie(base , values = 'CARÁCTER ACADÉMICO', names = '¿ACREDITADA ALTA CALIDAD?', title = '<b>% instituciones con acreditación de alta calidad de instuciones de educación superior<b>', hole = .3)

    # agregar detalles a la gráfica
    fig.update_layout(
        template = 'simple_white',
        legend_title = 'Caracter academico',
        title_x = 0.5,
        width = 400,
        height = 300)

    col2.plotly_chart(fig)

    

##################### GRAFICAS #############################