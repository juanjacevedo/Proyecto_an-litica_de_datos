import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit.components.v1 import html
import pydeck as pdk
from PIL import Image

# Para que la página siempre inicie en "formato ancho", que use toda la pantalla
st.set_page_config(layout="wide")
# Datos
coord = pd.read_csv('co.csv')
mat_ietdh2 = pd.read_csv('mat_ietdh2.csv')
mat_ietdh2 = mat_ietdh2.drop(['Unnamed: 0'], axis=1)
mat_meta = pd.read_csv('mat_meta.csv')
mat_meta = mat_meta.drop(['Unnamed: 0'], axis=1)
men_esta = pd.read_csv('men_esta.csv')
men_esta = men_esta.drop(['Unnamed: 0'], axis=1)
men_ietdh2 = pd.read_csv('men_ietdh2.csv')
men_ietdh2 = men_ietdh2.drop(['Unnamed: 0'], axis=1)

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
# my_html = f"<script>{my_js}</script>"  ##Por si queremos usar JavaScript

# # Execute your app
# st.title("Javascript example")
# html(my_html)
st.markdown("<h1 style='text-align: center;'>Educación Superior e Instituciones de Educación para el Trabajo y el Desarrollo Humano en Colombia </h1>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["CONTEXTO", "IETDH", "INSTITUCIONES DE EDUCACIÓN SUPERIOR", 'ESTADISTICAS', 'INFO +']) #Creación de las pestañas


##Primera pestaña de la página 
with tab1:
    image = Image.open('image.jpg')
    st.image(image) #Imagen principal
    intro = """<p>La educación superior en Colombia está dividida en dos frentes: Instituciones Educación Superior (IES) e Instituciones de Educación para el Trabajo y el Desarrollo Humano (IETDH), esto con el fin de ofrecer mayor cobertura educativa, desarrollo profesional y alternativas de adquisición de competencias académicas y laborales a la población en general, en especial a los estudiantes de educación media.
    Sin embargo, en diferentes estudios respecto a la problemática, se exhibe una falta de conexión entre el conocimiento impartido en estas instituciones y las necesidades del mundo laboral. 
    Este contexto, sumado a políticas de estado como la ley 30 de 1992 que buscan ampliar la cobertura educativa profesional, hacen que en los últimos 20 años el sector productivo impulse la creación de IETDH con el fin de obtener mano de obra calificada, posteriormente capacitada dentro de la industria para realizar labores propias de un profesional educado en una IES. Esto trae como beneficio una reducción de costos en contratación, ya que los rangos de salarios entre un técnico o tecnólogo de una IETDH y un profesional de una IES son diferentes debido a la diferencia de preparación académica entre uno y otro. A este fenómeno se le conoce como ¨Tercerización de la Educación Superior¨.
    El objetivo de este estudio es analizar las tendencias de crecimiento y cobertura de estos tipos de instituciones educativas, así como la calidad y sus históricos de matrícula.</p>"""
    st.markdown(intro, unsafe_allow_html=True) #Imprimir en pantalla el texto de las etiquetas <p>
with tab2:
    col1, col2 = st.columns([3, 1])

    df = pd.DataFrame()
    df['lat'] = men_ietdh2['LAT']
    df['lon'] = men_ietdh2['LNG']

    departamento = men_ietdh2.groupby(['DEPARTAMENTO'])[['NOMBRE_INSTITUCION']].count().sort_values(
        'NOMBRE_INSTITUCION', ascending=False).rename(columns={'NOMBRE_INSTITUCION': 'CANTIDAD'}).reset_index() ##DataFrame con la cantitdad de instituciones por departamento

    col1.map(df) #Imprimir mapa de IETDH

    col2.markdown(
        "<h5 style='text-align: center;'>Cantidad de instituciones por Departamento</h5>", unsafe_allow_html=True)
    col2.dataframe(departamento)

    col2.markdown(
        "<br/><br/><h5 style='text-align: center;'>Cantidad de instituciones por Municipio</h5>", unsafe_allow_html=True)

    municipio = men_ietdh2.groupby(['MUNICIPIO'])[['NOMBRE_INSTITUCION']].count().sort_values(
        'NOMBRE_INSTITUCION', ascending=False).rename(columns={'NOMBRE_INSTITUCION': 'CANTIDAD'}).reset_index()
    col2.write(municipio)

    col1.write(pdk.Deck(  # Código para crear el mapa

        # Set up del mapa
        map_style='mapbox://styles/mapbox/dark-v10',
        initial_view_state={
            'latitude': men_ietdh2['LAT'].mean(),
            'longitude': men_ietdh2['LNG'].mean(),
            'zoom': 4.8,
            'pitch': 30
        },

        # Capa con información
        layers=[pdk.Layer(
            'HexagonLayer',
            data=men_ietdh2[['LAT', 'LNG']],
            get_position=['LNG', 'LAT'],
            radius=5000,
            extruded=True,
            elevation_scale=500,
            elevation_range=[0, 1000])] 
    )) #Mapa de IEDTH por cantidad de instituciones en municipios

with tab3:
    col1, col2 = st.columns([3, 1])
    men_esta['COORDENADAS'] = men_esta['LAT'].astype(
        str) + ', ' + men_esta['LNG'].astype(str)

    df = pd.DataFrame()
    df['lat'] = men_esta['LAT']
    df['lon'] = men_esta['LNG']

    data = pd.DataFrame()
    data['MUNICIPIO'] = men_esta['MUNICIPIO']
    data['NOMBRE INSTITUCION'] = men_esta['NOMBRE INSTITUCIÓN']

    departamento1 = men_esta.groupby(['DEPARTAMENTO'])[['NOMBRE INSTITUCIÓN']].count().sort_values(
    'NOMBRE INSTITUCIÓN', ascending=False).rename(columns={'NOMBRE INSTITUCIÓN': 'CANTIDAD'}).reset_index()

    col1.map(df)

    col2.markdown(
        "<h5 style='text-align: center;'>Cantidad de instituciones por Departamento</h5>", unsafe_allow_html=True)
    col2.dataframe(departamento1)

    col2.markdown(
        "<br/><br/><h5 style='text-align: center;'>Cantidad de instituciones por Municipio</h5>", unsafe_allow_html=True)

    # Set the viewport location
    view_state = pdk.ViewState(
        latitude=4.495415131183657, longitude=-73.5789506384306, zoom=2, bearing=0, pitch=0)

    # Define a layer to display on a map
    municipio1 = men_esta.groupby(['MUNICIPIO'])[['NOMBRE INSTITUCIÓN']].count().sort_values(
        'NOMBRE INSTITUCIÓN', ascending=False).rename(columns={'NOMBRE INSTITUCIÓN': 'CANTIDAD'}).reset_index()
    col2.write(municipio1)

    col1.write(pdk.Deck(  # Código para crear el mapa

        # Set up del mapa
        map_style='mapbox://styles/mapbox/dark-v10',
        initial_view_state={
            'latitude': men_esta['LAT'].mean(),
            'longitude': men_esta['LNG'].mean(),
            'zoom': 4.8,
            'pitch': 30
        },

        # Capa con información
        layers=[pdk.Layer(
            'HexagonLayer',
            data=men_esta[['LAT', 'LNG']],
            get_position=['LNG', 'LAT'],
            radius=5000,
            extruded=True,
            elevation_scale=500,
            elevation_range=[0, 1000])]
    ))


##################### GRAFICAS ESTADISTICAS #############################
with tab4:
    st.markdown("<br/><br/><h2 style='text-align: center;'>Total matriculados</h2>",
                unsafe_allow_html=True)
    col1, col2 = st.columns((1, 1))
    # Metodo para remodelar o transformar un DataFrame existente
    # Metodo para remodelar o transformar un DataFrame existente
    mat_ietdh2_2 = pd.melt(mat_ietdh2, id_vars=[
                           'SECRETARÍA', 'CÓDIGO INSTITUCIÓN', 'NOMBRE INSTITUCIÓN', 'ESTADO INSTITUCIÓN', 'DEPARTAMENTO', 'MUNICIPIO'])

    # Corregir el nombre de los 'DEPARTAMENTO'
    año = [' TOTAL MATRÍCULA 2010 ', ' TOTAL MATRÍCULA 2011 ',
           ' TOTAL MATRÍCULA 2012 ', ' TOTAL MATRÍCULA 2013 ',
           ' TOTAL MATRÍCULA 2014 ', ' TOTAL MATRÍCULA 2015 ',
           ' TOTAL MATRÍCULA 2016 ', ' TOTAL MATRÍCULA 2017 ',
           ' TOTAL MATRÍCULA 2018 ', ' TOTAL MATRÍCULA 2019 ',
           ' TOTAL MATRÍCULA 2020 ', ' TOTAL MATRÍCULA 2021 ']

    cambio = ['2010', '2011', '2012', '2013', '2014', '2015',
              '2016', '2017', '2018', '2019', '2020', '2021']

    for i, j in zip(año, cambio):
        mat_ietdh2_2['variable'] = mat_ietdh2_2['variable'].replace(i, j)

    mat_ietdh2_2.rename(
        columns={'variable': 'AÑO', 'value': 'TOTAL MATRICULADOS'}, inplace=True)

    # Crear diagrama de barras para la 2 base de datos opcional
    # crear dataset
    df2 = mat_ietdh2_2.groupby(
        ['AÑO'])[['TOTAL MATRICULADOS']].sum().reset_index()

    fig = px.bar(df2, x='AÑO', y='TOTAL MATRICULADOS',
                 title='<b>Total matriculados en IETDH<b>', height=450, width=800)

    # agregar detalles a la gráfica
    fig.update_layout(
        xaxis_title='Año',
        yaxis_title='Total matriculado',
        template='simple_white',
        title_x=0.5,
        width=700,
        height=500)

    col1.write(fig)


# ¿Cuantos estudiantes se han matriculado a las instituciones de educación superior desde el 2015 hasta el 2020?
    # crear dataset
    df2 = mat_meta.groupby(['AÑO'])[['TOTAL MATRICULADOS']].sum().reset_index()

    fig = px.bar(df2, x='AÑO', y='TOTAL MATRICULADOS',
                 title='<b>Total matriculados en IES<b>')

    # agregar detalles a la gráfica
    fig.update_layout(
        xaxis_title='Año',
        yaxis_title='Total matriculado',
        template='simple_white',
        title_x=0.5,
        width=700,
        height=500)
    col2.write(fig)

    st.markdown("<br/><br/><h2 style='text-align: center;'>Certificado de calidad</h2>",
                unsafe_allow_html=True)
    col1, col2 = st.columns((1, 1))
# ¿Cuántas y que porcentaje instituciones de educación superior están acreditadas con alta calidad?
    # crear dataset
    base = men_esta.groupby(['¿ACREDITADA ALTA CALIDAD?'])[
        ['CARÁCTER ACADÉMICO']].count().reset_index()

    # crear gráfica
    fig = px.pie(base, values='CARÁCTER ACADÉMICO', names='¿ACREDITADA ALTA CALIDAD?',
                 title='<b>% instituciones con acreditación de alta calidad de IES<b>', hole=.3)

    # agregar detalles a la gráfica
    fig.update_layout(
        template='simple_white',
        legend_title='Caracter academico',
        title_x=0.5)

    col2.write(fig)

# ¿Qué porcentaje de las IETDH cuentan con certificado de calidad?
    # crear dataset

    base = men_ietdh2.groupby(['CERTIFICADO_CALIDAD'])[
        ['NOMBRE_INSTITUCION']].count().reset_index()

    # crear gráfica
    fig2 = px.pie(base, values='NOMBRE_INSTITUCION', names='CERTIFICADO_CALIDAD',
                  title='<b>% de IETDH con certificado de calidad', hole=.3)

    # agregar detalles a la gráfica
    fig2.update_layout(
        template='simple_white',
        legend_title='Caracter academico',
        title_x=0.5
    )
    #fig.update_traces(textposition='inside', textinfo='percent+label',insidetextorientation='radial')
    col1.write(fig2)

    st.markdown("<br/><br/><h2 style='text-align: center;'>Tipos de IES y acreditación de calidad</h2>",
                unsafe_allow_html=True)
    col1, col2 = st.columns((1, 1))

# ¿En qué porcentajes se dividen las instituciones de educación superior?
    # crear dataset
    base = men_esta.groupby(['CARÁCTER ACADÉMICO'])[
        ['NOMBRE INSTITUCIÓN']].count().reset_index()
    # crear gráfica
    fig = px.pie(base, values='NOMBRE INSTITUCIÓN', names='CARÁCTER ACADÉMICO',
                 title='<b>% de las diferentes IES', hole=.3)

    # agregar detalles a la gráfica
    fig.update_layout(
        template='simple_white',
        legend_title='Caracter academico',
        title_x=0.28
    )
    col1.write(fig)

# ¿Cuantas instituciones de educación superior están acreditadas con alta calidad segun su caracter académico?
    # crear dataset
    base = men_esta.groupby(['¿ACREDITADA ALTA CALIDAD?', 'CARÁCTER ACADÉMICO'])[
        ['NOMBRE INSTITUCIÓN']].count().reset_index()

    fig = px.bar(base, x='¿ACREDITADA ALTA CALIDAD?', y='NOMBRE INSTITUCIÓN', color='CARÁCTER ACADÉMICO',
                 barmode='group', title='<b>Estado de acreditación de las IES segun carácter academico<b>', text_auto=True)

    # agregar detalles a la gráfica
    fig.update_layout(
        xaxis_title='¿ACREDITADA ALTA CALIDAD?',
        yaxis_title='Total Instituciones',
        template='simple_white',
        title_x=0.5)

    col2.write(fig)

    st.markdown("<br/><br/><h2 style='text-align: center;'>Total de matriculados por municipio</h2>",
                unsafe_allow_html=True)
    col1, col2 = st.columns((1, 1))
# ¿Cuáles son los 5 municipios con mayor cantidad de estudiantes matriculados para las instituciones de Ed superior y IETDH?

    # crear dataset Educación Superior
    base1 = mat_meta.groupby(['MUNICIPIO DOMICILIO'])[['TOTAL MATRICULADOS']].sum(
    ).reset_index().sort_values('TOTAL MATRICULADOS', ascending=False).head(5)
    x = base1
    # sort_values('TOTAL MATRICULADOS', ascending = False)
    # crear gráfica
    fig = px.pie(x, values='TOTAL MATRICULADOS', names='MUNICIPIO DOMICILIO',
                 title='<b>% Municipios con mayor cantidad de IES<b>', hole=.3)

    # agregar detalles a la gráfica
    fig.update_layout(
        template='simple_white',
        legend_title='Municipio domicilio',
        title_x=0.5)

    col1.write(fig)

    # crear dataset IETDH
    base2 = mat_ietdh2_2.groupby(['MUNICIPIO'])[['TOTAL MATRICULADOS']].sum(
    ).reset_index().sort_values('TOTAL MATRICULADOS', ascending=False).head(5)
    y = base2

    # crear gráfica
    fig = px.pie(y, values='TOTAL MATRICULADOS', names='MUNICIPIO',
                 title='<b>Municipios con mayor cantidad de IETDH<b>', hole=.3)

    # agregar detalles a la gráfica
    fig.update_layout(
        template='simple_white',
        legend_title='Municipio domicilio',
        title_x=0.5)

    col2.write(fig)

    st.markdown("<br/><br/><h2 style='text-align: center;'>Total de instituciones por municipio</h2>",
                unsafe_allow_html=True)
    col1, col2 = st.columns((1, 1))
 # ¿Cuáles son los 5 municipios con mayor cantidad de instituciones para las instituciones de Ed superior y IETDH?

    # crear dataset Educación Superior
    base1 = mat_meta.groupby(['MUNICIPIO DOMICILIO'])[['INSTITUCION DE EDUCACION SUPERIOR']].count(
    ).reset_index().sort_values('INSTITUCION DE EDUCACION SUPERIOR', ascending=False).head(5)
    x = base1

    # sort_values('TOTAL MATRICULADOS', ascending = False)
    # crear gráfica
    fig = px.pie(x, values='INSTITUCION DE EDUCACION SUPERIOR', names='MUNICIPIO DOMICILIO',
                 title='<b>% Total de Matriculados por ciudades en instituciones Educación Superior<b>', hole=.3)

    # agregar detalles a la gráfica
    fig.update_layout(
        template='simple_white',
        legend_title='Municipio domicilio',
        title_x=0.5)

    col1.write(fig)

    # crear dataset IETDH
    base2 = mat_ietdh2_2.groupby(['MUNICIPIO'])[['NOMBRE INSTITUCIÓN']].count(
    ).reset_index().sort_values('NOMBRE INSTITUCIÓN', ascending=False).head(5)
    y = base2

    # crear gráfica
    fig = px.pie(y, values='NOMBRE INSTITUCIÓN', names='MUNICIPIO',
                 title='<b>% Total de Matriculados por ciudades en instituciones IETDH<b>', hole=.3)

    # agregar detalles a la gráfica
    fig.update_layout(
        template='simple_white',
        legend_title='Municipio domicilio',
        title_x=0.5)

    col2.write(fig)


# ¿Cuantás instituciones hay de caracter publico y privado para las instituciones de educación superior?
    col1, col2, col3 = st.columns((1, 2, 1))

    # oficial_DB
    oficial = men_esta[men_esta['SECTOR'] == 'oficial'].reset_index()
    oficiales = oficial.groupby(['DEPARTAMENTO'])[['SECTOR']].count(
    ).sort_values('SECTOR', ascending=False).rename(columns={'SECTOR': 'counts'})
    oficiales['ratio'] = oficiales.apply(
        lambda x: x.cumsum()/oficiales['counts'].sum())

    # definir figura
    fig = go.Figure([go.Bar(x=oficiales.index, y=oficiales['counts'], yaxis='y1', name='sessions id'),
                    go.Scatter(x=oficiales.index, y=oficiales['ratio'], yaxis='y2', name='Universidades oficiales', hovertemplate='%{y:.1%}', marker={'color': '#FC0000'})])

    # agregar detalles
    fig.update_layout(template='plotly_white', showlegend=False, hovermode='x', bargap=.3,
                      title={
                          'text': '<b>Pareto universidades de educación superior oficiales por departamento<b>', 'x': .5},
                      yaxis={'title': 'universidades'},
                      yaxis2={'rangemode': "tozero", 'overlaying': 'y', 'position': 1, 'side': 'right', 'title': 'ratio', 'tickvals': np.arange(
                          0, 1.1, .2), 'tickmode': 'array', 'ticktext': [str(i) + '%' for i in range(0, 101, 20)]},
                      width=800,
                      height=800)

    col2.markdown(
        "<br/><br/><h2 style='text-align: center;'>Cantidad de IES publicas y privadas por departamento</h2>", unsafe_allow_html=True)
    col2.write(fig)
###################################################
#     # privada_DB
    privada = men_esta[men_esta['SECTOR'] == 'privada'].reset_index()
    privadas = privada.groupby(['DEPARTAMENTO'])[['SECTOR']].count(
    ).sort_values('SECTOR', ascending=False).rename(columns={'SECTOR': 'counts'})
    privadas['ratio'] = privadas.apply(
        lambda x: x.cumsum()/privadas['counts'].sum())

    # definir figura
    fig2 = go.Figure([go.Bar(x=privadas.index, y=privadas['counts'], yaxis='y1', name='sessions id'),
                      go.Scatter(x=privadas.index, y=privadas['ratio'], yaxis='y2', name='Universidades privadas', hovertemplate='%{y:.1%}', marker={'color': '#FC0000'})])

    # agregar detalles
    fig2.update_layout(template='plotly_white', showlegend=False, hovermode='x', bargap=.3,
                       title={
                           'text': '<b>Pareto universidades de educación superior privadas por departamento<b>', 'x': .5},
                       yaxis={'title': 'universidades'},
                       yaxis2={'rangemode': "tozero", 'overlaying': 'y', 'position': 1, 'side': 'right', 'title': 'ratio', 'tickvals': np.arange(
                           0, 1.1, .2), 'tickmode': 'array', 'ticktext': [str(i) + '%' for i in range(0, 101, 20)]},
                       width=800,
                       height=550)

    col2.write(fig2)

# ¿Cuantás instituciones hay de caracter publico, privado y mixta para las IETDH?

    col2.markdown(
        "<br/><br/><h2 style='text-align: center;'>Cantidad de IETDH oficiales, privadas y mixtas por departamento</h2>", unsafe_allow_html=True)

    # oficial_DB
    oficial = men_ietdh2[men_ietdh2['NATURALEZA'] == 'oficial'].reset_index()
    oficiales = oficial.groupby(['DEPARTAMENTO'])[['NATURALEZA']].count().sort_values(
        'NATURALEZA', ascending=False).rename(columns={'NATURALEZA': 'counts'})
    oficiales['ratio'] = oficiales.apply(
        lambda x: x.cumsum()/oficiales['counts'].sum())

    # definir figura
    fig = go.Figure([go.Bar(x=oficiales.index, y=oficiales['counts'], yaxis='y1', name='sessions id'),
                    go.Scatter(x=oficiales.index, y=oficiales['ratio'], yaxis='y2', name='Instituciones', hovertemplate='%{y:.1%}', marker={'color': '#FC0000'})])

    # agregar detalles
    fig.update_layout(template='plotly_white', showlegend=False, hovermode='x', bargap=.3,
                      title={
                          'text': '<b>Pareto IETDH oficiales por departamento<b>', 'x': .5},
                      yaxis={'title': 'instituciones'},
                      yaxis2={'rangemode': "tozero", 'overlaying': 'y', 'position': 1, 'side': 'right', 'title': 'ratio', 'tickvals': np.arange(
                          0, 1.1, .2), 'tickmode': 'array', 'ticktext': [str(i) + '%' for i in range(0, 101, 20)]},
                      width=800,
                      height=800)

    col2.write(fig)

    # privada_DB
    privada = men_ietdh2[men_ietdh2['NATURALEZA'] == 'privada'].reset_index()
    privados = privada.groupby(['DEPARTAMENTO'])[['NATURALEZA']].count().sort_values(
        'NATURALEZA', ascending=False).rename(columns={'NATURALEZA': 'counts'})
    privados['ratio'] = privados.apply(
        lambda x: x.cumsum()/privados['counts'].sum())

    # definir figura
    fig2 = go.Figure([go.Bar(x=privados.index, y=privados['counts'], yaxis='y1', name='sessions id'),
                      go.Scatter(x=privados.index, y=privados['ratio'], yaxis='y2', name='Instituciones', hovertemplate='%{y:.1%}', marker={'color': "#FC0000"})])

    # agregar detalles
    fig2.update_layout(template='plotly_white', showlegend=False, hovermode='x', bargap=.3,
                       title={
                           'text': '<b>Pareto IETDH privadas por departamento<b>', 'x': .5},
                       yaxis={'title': 'instituciones'},
                       yaxis2={'rangemode': "tozero", 'overlaying': 'y', 'position': 1, 'side': 'right', 'title': 'ratio', 'tickvals': np.arange(
                           0, 1.1, .2), 'tickmode': 'array', 'ticktext': [str(i) + '%' for i in range(0, 101, 20)]},
                       width=800,
                       height=800)

    # mixto_DB
    mixta = men_ietdh2[men_ietdh2['NATURALEZA'] == 'mixta'].reset_index()
    mixtas = mixta.groupby(['DEPARTAMENTO'])[['NATURALEZA']].count().sort_values(
        'NATURALEZA', ascending=False).rename(columns={'NATURALEZA': 'counts'})
    mixtas['ratio'] = mixtas.apply(lambda x: x.cumsum()/mixtas['counts'].sum())

    col2.write(fig2)

    # definir figura
    fig3 = go.Figure([go.Bar(x=mixtas.index, y=mixtas['counts'], yaxis='y1', name='sessions id'),
                      go.Scatter(x=mixtas.index, y=mixtas['ratio'], yaxis='y2', name='Instituciones', hovertemplate='%{y:.1%}', marker={'color': "#FC0000"})])

    # agregar detalles
    fig3.update_layout(template='plotly_white', showlegend=False, hovermode='x', bargap=.3,
                       title={
                           'text': '<b>Pareto IETDH mixtas por departamento<b>', 'x': .5},
                       yaxis={'title': 'instituciones'},
                       yaxis2={'rangemode': "tozero", 'overlaying': 'y', 'position': 1, 'side': 'right', 'title': 'ratio', 'tickvals': np.arange(
                           0, 1.1, .2), 'tickmode': 'array', 'ticktext': [str(i) + '%' for i in range(0, 101, 20)]},
                       width=800,
                       height=500)

    col2.write(fig3)
with tab5:
    col1, col2, col3 = st.columns((1, 2, 1))

    

    col2.write("<h3 style='text-align: center;'>Información complementaria</h3>", unsafe_allow_html=True)
    col2.write('<iframe width="660" height="415" src="https://www.youtube.com/embed/GcFdINjtPAo?start=1" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>', unsafe_allow_html=True)
    col2.write('<iframe width="660" height="415" src="https://www.youtube.com/embed/63FQbzHgKxY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>', unsafe_allow_html=True)

    st.write(
        "<a href='https://github.com/juanjacevedo/Proyecto_analitica_de_datos.git'>Repositorio</a> | <a href='mailto:juan-jo122@hotmail.com'>Contacto</a> ", unsafe_allow_html=True)

    st.write("<h6 style='color:powderblue;'>Elaborado por:</h6>",unsafe_allow_html=True)
    st.write("""<ul>
<LI>Daniel Alejandro Manco
<LI>Fabian Gómez 
<LI>Juan José Acevedo
<LI>Sebastián Zuluaga
</ul>""",unsafe_allow_html=True)