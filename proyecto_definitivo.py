import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import psycopg2
import pandas as pd
from dash.dependencies import Input, Output


# Establecer conexión con la base de datos
conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="123456789",
    database="proyecto"
)

# Primera consulta SQL
query1 = """
SELECT c.nombre, COUNT(e.nit)
FROM empresa e
JOIN ciudad c 
ON c.codigo = e.cod_ciudad
GROUP BY c.nombre;
"""

# Segunda consulta SQL
query2 = """
SELECT t.nombre, COUNT(e.nit)
FROM empresa e 
JOIN tamanio_empresa t
ON t.codigo = e.cod_tamanio_empresa
GROUP BY t.nombre;
"""

# Tercera consulta SQL
query3 = """
SELECT s.nombre, COUNT(e.nit)
FROM empresa e 
JOIN sector_economico s
ON s.codigo = e.cod_sector_economico
GROUP BY s.nombre;
"""

# Cuarta consulta SQL
query4 = """
SELECT estado_empresa.nombre, COUNT(e.nit)
FROM empresa e 
JOIN estado_empresa 
ON estado_empresa.codigo = e.cod_estado_empresa
GROUP BY estado_empresa.nombre;
"""

# Quinta consulta SQL
query5 = """
SELECT c.descripcion, COUNT(ce.nit_empresa)
FROM ciiu_empresa ce 
JOIN ciiu c
ON c.codigo = ce.cod_ciiu
GROUP BY c.descripcion
ORDER BY COUNT(ce.nit_empresa) DESC;
"""

# Sexta consulta SQL
query6 = """
SELECT s.nombre AS sector, t.nombre AS tamaño, COUNT(e.nit)
FROM empresa e
JOIN sector_economico s ON s.codigo = e.cod_sector_economico
JOIN tamanio_empresa t ON t.codigo = e.cod_tamanio_empresa
GROUP BY s.nombre, t.nombre
ORDER BY s.nombre, t.nombre;
"""
# Query SQL 7
query7 = """
SELECT t.nombre, SUM(e.num_empleados)
FROM empresa e
JOIN tamanio_empresa t ON t.codigo = e.cod_tamanio_empresa
GROUP BY t.nombre
ORDER BY SUM(e.num_empleados) DESC;
"""
# Query SQL 8
query8 = """
SELECT t.nombre, COUNT(e.nit)
FROM empresa e
JOIN tipo_juridico t ON t.codigo = e.cod_tipo_juridico
GROUP BY t.nombre
ORDER BY COUNT(e.nit) DESC;
"""
# Novena consulta SQL
query9 = """
SELECT tj.nombre, t.nombre AS tamano, COUNT(e.nit) AS empresas
FROM empresa e
JOIN tipo_juridico tj ON tj.codigo = e.cod_tipo_juridico
JOIN tamanio_empresa t ON t.codigo = e.cod_tamanio_empresa
GROUP BY tj.nombre, t.nombre
ORDER BY tj.nombre;
"""
# Query SQL 10
query10 = """
SELECT t.nombre as tamanio, s.nombre as sector, c.nombre as ciudad, COUNT(e.nit) as empresas
FROM empresa e
JOIN tamanio_empresa t ON t.codigo = e.cod_tamanio_empresa
JOIN sector_economico s ON s.codigo = e.cod_sector_economico
JOIN ciudad c ON c.codigo = e.cod_ciudad
GROUP BY t.nombre, s.nombre, c.nombre
ORDER BY COUNT(e.nit) DESC;
"""

main_title = {
    'font-family': 'Roboto, sans-serif',
    'font-weight': 'bold',
    'text-align': 'center'
}

section_title = {
    'font-family': 'Roboto, sans-serif',
    'font-weight': 'bold',
}

paragraph = {
   'font-family': 'Roboto, sans-serif',
   'font-weight': 'regular', 
}


# Leer los datos a los DataFrames
df1 = pd.read_sql_query(query1, conn)
df2 = pd.read_sql_query(query2, conn)
df3 = pd.read_sql_query(query3, conn)
df4 = pd.read_sql_query(query4, conn)
df5 = pd.read_sql_query(query5, conn)
df6 = pd.read_sql_query(query6, conn)
df7 = pd.read_sql_query(query7, conn)
df8 = pd.read_sql_query(query8, conn)
df9 = pd.read_sql_query(query9, conn)
df10 = pd.read_sql_query(query10, conn)


# Crear un diccionario para cada ciudad
city_dict = {city: df10[df10['ciudad'] == city] for city in df10['ciudad'].unique()}

# Crear un diccionario con los datos de cada tamaño
tamano_dict = {tamano: df9[df9['tamano'] == tamano] for tamano in df9['tamano'].unique()}

# Cerrar la conexión
conn.close()

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Crear el layout de la aplicación
app.layout = html.Div([
    html.Div(
        children=[
            html.H1("Proyecto de Ingeniería de Datos",style=main_title),
            html.H1('Análisis de los datos de la cámara de comercio de Bucaramanga', style=main_title),
            html.Br()
    ]
    ),
    html.Div(children = [html.H2('Escenario 1: Análisis de distribución geográfica de las empresas', style=section_title),
        dcc.Graph(
            id='city-bar-chart',
            figure={
                'data': [
                    go.Bar(
                        x=df1['nombre'],  # Datos del eje X (Nombres de las ciudades)
                        y=df1['count'],  # Datos del eje Y (Conteos de empresas)
                        text=df1['count'],
                        textposition='auto',
                    )
                ],
                'layout': go.Layout(
                    title='Número de Empresas por Ciudad',
                    xaxis={'title': 'Ciudad', 'automargin': True},
                    yaxis={'title': 'Número de empresas'},
                )
            }
        )]
    ),
    html.Div( children = [
            html.H2('Comentarios', style=section_title),
            html.H3('Diego Benavides', style=section_title),
            html.P('La cantidad de empresas por ubicación indica claramente la diferencia de actividad económica entre municipios en el departamento de Santander. Esta diferencia sucede de acuerdo al tamaño y población del municipio.', style=paragraph),
            html.H3('Andrés Manrique', style=section_title),
            html.P('Dentro del análisis nos podemos dar cuenta que incluso sumando todas las empresas registradas fuera de Bucaramanga, no logra alcanzar a la capital de Santander. Lo cual indica que el mayor movimiento económico sucede en la capita.', style=paragraph),
            html.H3('Jerónimo Manriquez', style=section_title),
            html.P('Se debe notar la falta de empresas de la ciudad en el segundo puesto, está siendo Floridablanca, que tiene una población de alrededor de 260000 personas, comparada con la población de 580000 personas de Bucaramanga, Bucaramanga tiene 3.6 veces más empresas, pero solo 2.2 veces más personas, tal que Bucaramanga tiene más empresas por persona comparadas con el resto de las ciudades, o Floridablanca tiene una falta de personas.', style=paragraph),
            html.Br(),
            html.Br()
        ]
    ),
    
    html.Div(
        children=[html.H2('Escenario 2: Análisis por tamaño de empresa', style=section_title)],
    ),
    dcc.Graph(
        id='size-pie-chart',
        figure={
            'data': [
                go.Pie(
                    labels=df2['nombre'],  # Etiquetas (Tamaños de las empresas)
                    values=df2['count'],  # Valores (Conteos de empresas)
                    textinfo='label+percent',
                    insidetextorientation='radial'
                )
            ],
            'layout': go.Layout(
                title='Número de Empresas por Tamaño',
            )
        }
    ),
    html.Div( children =[
            html.H2('Comentarios', style=section_title),
            html.H3('Diego Benavides', style=section_title),
            html.P('El 99.1% de las empresas registradas son microempresas, un número sorprendente que nos indica que entre PYMES y grandes empresas solo son un 0.9% de las empresas registradas. Lo anterior también refleja la disparidad que hay entre empresas.', style=paragraph),
            html.H3('Andrés Manrique', style=section_title),
            html.P('Dentro del análisis nos podemos dar cuenta que, la distribución de empresas por tamaño sigue una relación inversa, a mayor sea el tamaño de la empresa, menor cantidad de empresas de ese tamaño va a haber.', style=paragraph),
            html.H3('Jerónimo Manriquez', style=section_title),
            html.P('Incluso si no se examinan las microempresas, las empresas de tamaño mediano y grande igual son dominadas en número por las pequeñas empresas, mostrando el gran desafío que exista al crear estas empresas de tamaño considerable.', style=paragraph),
            html.Br(),
            html.Br()
        ]
    ),
    html.Div(
        children=[html.H2('Escenario 3: Análisis por sector ecónomico', style=section_title)],
    ),
    dcc.Graph(
        id='sector-bar-chart',
        figure={
            'data': [
                go.Bar(
                    x=df3['nombre'],  # Datos del eje X (Nombres de los sectores económicos)
                    y=df3['count'],  # Datos del eje Y (Conteos de empresas)
                    text=df3['count'],
                    textposition='auto',
                )
            ],
            'layout': go.Layout(
                title='Número de Empresas por Sector Económico',
                xaxis={'title': 'Sector Económico', 'automargin': True},
                yaxis={'title': 'Número de empresas'},
            )
        }
    ),
    html.Div( children =[
            html.H2('Comentarios', style=section_title),
            html.H3('Diego Benavides', style=section_title),
            html.P('El sector ecónomico de mayor impacto dentro del departamento de Santander es el comercio al por mayor y menor; reparación de vehiculos automotores y motocicletas. Lo anterior señala que dentro de esta región la importancia de este tipo de servicios para los ciudadanos.', style=paragraph),
            html.H3('Andrés Manrique', style=section_title),
            html.P('El tercer sector ecónmico registrado en nuestra base de datos es alojamiento y servicios de comida. Esto es lógico debido a la importancia dentro de la región, ya que es uno de los destinos turisticos predilectos para viajeros. ', style=paragraph),
            html.H3('Jerónimo Manriquez', style=section_title),
            html.P('En comparación con las empresas por tamaño, se debe notar que existen demasiadas industrias manufactureras para que la mayoría sea más grande que microempresas, implicando que existen muchos esfuerzos manufactureros en estas regiones que contratan menos de 10 empleados.', style=paragraph),
            html.Br(),
            html.Br()
        ]
    ),
    html.Div(
        children=[html.H2('Escenario 4: Análisis del estado de las empresas', style=section_title)],
    ),
    dcc.Graph(
        id='estado-bar-chart',
        figure={
            'data': [
                go.Bar(
                    x=df4['nombre'],  # Datos del eje X (Nombres de los estados de la empresa)
                    y=df4['count'],  # Datos del eje Y (Conteos de empresas)
                    text=df4['count'],
                    textposition='auto',
                )
            ],
            'layout': go.Layout(
                title='Número de Empresas por Estado',
                xaxis={'title': 'Estado', 'automargin': True},
                yaxis={'title': 'Número de empresas'},
            )
        }
    ),
    html.Div( children =[
            html.H2('Comentarios', style=section_title),
            html.H3('Diego Benavides', style=section_title),
            html.P('De nuestra base de datos podemos asumir que no hay empresas que se encuentran en liquidación por adjudicación, una posible causa de esto, es que cuando una empresa adjudica a otra, lo más seguro es que sea una empresa pequeña, de ahí que el proceso de liquidación sea rápido y no aparezca reflejado en los registros.', style=paragraph),
            html.H3('Andrés Manrique', style=section_title),
            html.P('La información sugiere que la gran mayoría de empresas se encuentran activas, mientras que empresas que se encuentran en cualquier otro caso son casos excepcionales.', style=paragraph),
            html.H3('Jerónimo Manriquez', style=section_title),
            html.P('La cantidad tan baja de empresas en liquidación es sospechosa en comparación con la gran cantidad de empresas que parecen estar en quiebra, especialmente considerando que la mayoría son negocios pequeños que pueden quebrar fácilmente, posiblemente indicando que la representación de este estado puede ser más pequeña que en la realidad.', style=paragraph),
            html.Br(),
            html.Br()
        ]
    ),
    html.Div(
        children=[html.H2('Escenario 5: Análisis por CIUU', style=section_title)],
    ),
    dcc.Graph(
        id='ciiu-bar-chart',
        figure={
            'data': [
                go.Bar(
                    x=df5['descripcion'],  # Datos del eje X (Descripciones de CIIU)
                    y=df5['count'],  # Datos del eje Y (Conteos de empresas)
                    text=df5['count'],
                    textposition='auto',
                )
            ],
            'layout': go.Layout(
                title='Número de Empresas por CIIU',
                xaxis={'title': 'CIIU', 'automargin': True},
                yaxis={'title': 'Número de empresas'},
            )
        }
    ),
    html.Div( children =[
            html.H2('Comentarios', style=section_title),
            html.H3('Diego Benavides', style=section_title),
            html.P('Observando la descripción de los códigos CIIU podemos darnos cuenta que la mayoría de empresas están registradas en actividades relacionadas con comercio al por menor, desde salones de belleza hasta ferreterías. Todos estos establecimientos de comercio compartiendo la misma caracteristica, ser comercio al por menor. ', style=paragraph),
            html.H3('Andrés Manrique', style=section_title),
            html.P('También, si observamos con detenimiento la mayoría de empresas registradas pertenecen al comercio por mayor y a actividades ecónomicas relacionadas con comida. Estas pueden ser la venta de viveres, o otro tipo de actividad relacionada con la comida, como lo puede ser un establecimiento de comida, es decir un restaurante.', style=paragraph),
            html.H3('Jerónimo Manriquez', style=section_title),
            html.P('Al observar la descripción de los códigos CIIU, se puede observar que todas las empresas en los primeros lugares son aquellas que más fáciles son de encontrar en la región de Bucaramanga, con estos códigos estando relacionados con tiendas y farmacias de barrio', style=paragraph),
            html.Br(),
            html.Br()
        ]
    ),
    html.Div(
        children=[html.H2('Escenario 6: Análisis de la relación entre tamaño y sector económico de las empresas', style=section_title)],
    ),
    dcc.Graph(
        id='sector-size-bar-chart',
        figure={
            'data': [
                go.Bar(
                    name=sector, 
                    x=df6[df6['sector']==sector]['tamaño'],  
                    y=df6[df6['sector']==sector]['count'],  
                    text=df6[df6['sector']==sector]['count'],
                    textposition='auto',
                ) for sector in df6['sector'].unique()
            ],
            'layout': go.Layout(
                title='Número de Empresas por Sector y Tamaño',
                xaxis={'title': 'Sector y Tamaño', 'automargin': True},
                yaxis={'title': 'Número de empresas'},
                barmode='stack',
            )
        }
    ),
    html.Div( children =[
            html.H2('Comentarios', style=section_title),
            html.H3('Diego Benavides', style=section_title),
            html.P('Las microempresas son la mayoría como lo vimos anteriormente, además los sectores predominantes dentro de las microempresas son: El comercio al por mayor y menor de vehiculos, la industria manufacturera y los servicios de alohamiento y comidas. Todas estas actividades llevadas a cabo por empresas de menos de 10 personas y con ganancias anuales inferiores a los 501 smmlv.', style=paragraph),
            html.H3('Andrés Manrique', style=section_title),
            html.P('Este análisis también nos permite saber a que se dedican las pocas grandes empresas que se encuentran en la región. Estas empresas se dedican a la agricultura, ganaderia, silvicultura y pesca. Las grandes empresas tambien comparten este sector con empresas más pequeñas, sin embargo su superficie no es equiparable.', style=paragraph),
            html.H3('Jerónimo Manriquez', style=section_title),
            html.P('Las medianas empresas tienen una sobrerrepresentación de las industrias manufactureras y negocios dedicados al comercio al mayor, indicando que una parte importante de empresas medianas locales involucra la producción y distribución de bienes en esta región, demostrando la importancia de este tipo de negocios.', style=paragraph),
            html.Br(),
            html.Br()
        ]
    ),
    html.Div(
        children=[html.H2('Escenario 7: Análisis de la relación entre tamaño y cantidad de empleados', style=section_title)],
    ),
    dcc.Graph(
        id='employees-bar-chart',
        figure={
            'data': [
                go.Bar(
                    x=df7['nombre'],  # Datos del eje X (Tamaños de las empresas)
                    y=df7['sum'],  # Datos del eje Y (Suma de empleados)
                    text=df7['sum'],
                    textposition='auto',
                )
            ],
            'layout': go.Layout(
                title='Número de Empleados por Tamaño de Empresa',
                xaxis={'title': 'Tamaño de la empresa', 'automargin': True},
                yaxis={'title': 'Número de empleados'},
            )
        }
    ),
    html.Div( children =[
            html.H2('Comentarios', style=section_title),
            html.H3('Diego Benavides', style=section_title),
            html.P('La mayoría de personas trabajan en microempresas, lo cual tiene sentido ya que las microempresas son casi la totalidad de empresas registradas. También es importante analizar que la relación de número de empleados afiliados de acuerdo al tamaño de empresa, es inversa, es decir, las empresas grandes tienen la menor cantidad de empleados afiliados, luego las medianas y así hata llegar a las microempresas.', style=paragraph),
            html.H3('Andrés Manrique', style=section_title),
            html.P('Con este análisis reforzamos la idea de que las empresas con mayor representación y empleados son las microempresas. Tenemos que tener en cuenta que esas 131787 personas que trabajan en microempresas estan agrupadas en empresas de no más de 10 personas.', style=paragraph),
            html.H3('Jerónimo Manriquez', style=section_title),
            html.P('Aunque las empresas grandes tengan la mayor cantidad de empleados, existen muy pocas empresas grandes en comparación los otros tipos de empresas, tal que la gran mayoría de empleados no trabajan en empresas grandes, aunque se pueden considerar las más importantes.', style=paragraph),
            html.Br(),
            html.Br()
        ]
    ),
    html.Div(
        children=[html.H2('Escenario 8: Análisis de las empresas por tipo jurídico', style=section_title)],
    ),
    dcc.Graph(
        id='tipo-juridico-pie-chart',
        figure={
            'data': [
                go.Pie(
                    labels=df8['nombre'],  # Datos de las etiquetas (Nombres de los tipos jurídicos)
                    values=df8['count'],  # Datos de los valores (Conteos de empresas)
                )
            ],
            'layout': go.Layout(
                title='Número de Empresas por Tipo Jurídico',
            )
        }
    ),
    html.Div( children =[
            html.H2('Comentarios', style=section_title),
            html.H3('Diego Benavides', style=section_title),
            html.P('Podemos ver como la mayoría de empresas son de tipo persona natural lo cual tiene sentido de acuerdo a la cantidad de las microempresas de una sola persona. Sin embargo, vemos que el tipo jurídico es SAS, sociedad por acciones simplificada, esto es lógico pensando que es una de los tipos jurídicos que mejores oportunidades brinda.', style=paragraph),
            html.H3('Andrés Manrique', style=section_title),
            html.P('Si dejamos a un lado a las empresas SAS y a las personas naturales podemos apreciar que la mayoría de empresas son sociedades limitadas, lo cual esperariamos ver ya que es un tipo juridico muy popular despúes de las SAS.', style=paragraph),
            html.H3('Jerónimo Manriquez', style=section_title),
            html.P('La razón por la cual las personas naturales dominan esta grafica es debido a la facilidad de crear una microempresa empresa como persona natural, aunque sea una empresa de uno o dos empleados no importa el tamaño de la empresa el ver la distribución de tipos jurídicos. ', style=paragraph),
            html.Br(),
            html.Br()
        ]
    ),
    html.Div(
        children=[html.H2('Escenario 9: Análisis de tamaño de empresas por ciudad y sector económico', style=section_title)],
    ),
    html.Div([
    html.Label("Seleccione la ciudad"),
    dcc.Dropdown(
        id="city_dropdown",
        options=[{"label": i, "value": i} for i in df10["ciudad"].unique()],
        value=df10["ciudad"].unique()[0]
    )
    ]),
    dcc.Graph(
        id='tamano-sector-city-bar-chart',
    ),
    html.Div( children =[
            html.H2('Comentarios', style=section_title),
            html.H3('Diego Benavides', style=section_title),
            html.P('El sector ecónomico predominante que era la venta y reparación de vehiculos automotores, es el que domina en las grandes ciudades del departamento como Bucaramanga o Floridablanca.', style=paragraph),
            html.H3('Andrés Manrique', style=section_title),
            html.P('Al analizar los datos nos podemos dar cuenta que los servicios de alojamiento y comida son los que predominan casi con completa totalidad los lugares más turisticos del departamento de Santander.', style=paragraph),
            html.H3('Jerónimo Manriquez', style=section_title),
            html.P('La tendencia que los alojamientos y servicios de comida se mantengan en los primeros lugares se mantiene en todas las ciudades, desde Bucaramanga, la ciudad más grande hasta los pueblos más pequeños como Jordán y Macaravita. ', style=paragraph),
            html.Br(),
            html.Br()
        ]
    ),
    html.Div(
        children=[html.H2('Escenario 10: Análisis por tamaño y tipo jurídico.', style=section_title)],
    ),
    html.Div([
        dcc.Dropdown(
            id='tamano_dropdown',
            options=[{'label': tamano, 'value': tamano} for tamano in df9['tamano'].unique()],
            value=df9['tamano'].unique()[0]
        ),
        dcc.Graph(id='tipo-juridico-pie-chart')
    ]),
    html.Div( children =[
            html.H2('Comentarios', style=section_title),
            html.H3('Diego Benavides', style=section_title),
            html.P('Dentro de las grandes empresas solo encontramos dos tipos jurídicos: Sociedad por acciones simplificada y sociedades anónimas. Estos tipos juridicos se encuentran practicamente en un 50 50, habiendo 11 empresas SAS y 10 empresas como sociedades anónimas.', style=paragraph),
            html.H3('Andrés Manrique', style=section_title),
            html.P('Las microempresas están dominadas por personas naturales, lo cual no es raro ser empresas con máximo 10 trabajadores, sin embargo, dentro de las microempresas también podemos encontrar una cantidad importante de sociedades por acciones simplificadas SAS.', style=paragraph),
            html.H3('Jerónimo Manriquez', style=section_title),
            html.P('Aunque en las grandes empresas solo existan sociedades por acciones simplificadas y sociedad anónima, en las medianas empresas aún se pueden encontrar diferentes tipos jurídicos, como personas naturales y sociedades limitadas.  ', style=paragraph),
            html.Br(),
            html.Br()
        ]
    ),
    html.Div(
        children=[html.H1('Conclusiones', style=section_title)],
    ),
    html.Div( children =[
            html.H2('Comentarios', style=section_title),
            html.H3('Diego Benavides', style=section_title),
            html.P('La actividad económica, ubicación y tamaño de la empresa son determinantes clave en la economía local y regional: Las empresas, dependiendo de su tamaño y del sector al que pertenezcan, pueden influir significativamente en la economía de su ubicación. El análisis de estos factores puede ayudar a entender las tendencias económicas y a planificar estrategias de desarrollo económico a nivel local y regional como por ejemplo el niver de inversión en el área manufacturera o turistica.', style=paragraph),
            html.H3('Andrés Manrique', style=section_title),
            html.P('El tipo jurídico, el tamaño de la empresa y la ciudad pueden influir en la configuración y desarrollo del paisaje empresarial: El tipo jurídico puede determinar las responsabilidades legales y fiscales de una empresa, lo cual puede a su vez influir en su capacidad para crecer y competir. Además, el tamaño de la empresa puede afectar su capacidad para generar empleo, contribuir a la economía local y atraer inversiones. Por último, la ubicación de una empresa en una ciudad específica puede ofrecer ciertas ventajas o desventajas en términos de acceso a mercados, recursos y mano de obra. En conjunto, estos factores pueden tener un impacto significativo en la diversidad y fortaleza del tejido empresarial en una ciudad o región.', style=paragraph),
            html.H3('Jerónimo Manriquez', style=section_title),
            html.P('Mi conclusión principal al examinar estas estadísticas es la importancia de las microempresas para la economía y sociedad, estas estando compuestas por tiendas de barrio y restaurantes familiares, los cuales mueven una gran cantidad de empleados y por ende servicios por todas las regiones de Bucaramanga, no se puede subestimar el valor de estas empresas por su pequeño tamaño, ya que debido a su enorme cantidad comparadas con las empresas más grandes pueden tener un impacto igual o incluso mayor que estas en la economía de la región.', style=paragraph),
            html.Br(),
            html.Br()
        ]
    ),
])


# Callback para actualizar el gráfico en función de la ciudad seleccionada
@app.callback(
    dash.dependencies.Output('tamano-sector-city-bar-chart', 'figure'),
    [dash.dependencies.Input('city_dropdown', 'value')]
)
def update_graph(selected_city):
    df = city_dict[selected_city]
    figure = go.Figure(data=[
        go.Bar(
            x=df['sector'][df['tamanio'] == tamanio], 
            y=df['empresas'][df['tamanio'] == tamanio], 
            name=tamanio,
            text=df['empresas'][df['tamanio'] == tamanio],
            textposition='auto',
        ) for tamanio in df['tamanio'].unique()
    ])
    figure.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'}, title=f'Número de Empresas por Tamaño y Sector Económico en {selected_city}')
    return figure

# Callback para actualizar la gráfica en función del tamaño seleccionado
@app.callback(
    Output('tipo-juridico-pie-chart', 'figure'),
    [Input('tamano_dropdown', 'value')]
)
def update_graph_2(selected_tamano):
    df = tamano_dict[selected_tamano]
    fig = go.Figure(data=[
        go.Pie(labels=df['nombre'], values=df['empresas'])
    ])
    fig.update_layout(title=f'Número de Empresas por Tipo Jurídico (Tamaño: {selected_tamano})')
    return fig

# Correr el servidor
if __name__ == '__main__':
    app.run_server(debug=False)

