# from datetime import *
# # from dash import Dash, Input, Output  # pip install dash (version 2.0.0 or higher)
# import dash
# from dash.dependencies import Input, Output
# import dash_bootstrap_components as dbc
# import dash_core_components as dcc
# import dash_html_components as html
# from django_plotly_dash import DjangoDash
# from django.db.models import Count
# from django.db.models.functions import Cast
# import pandas as pd
# import plotly.express as px  # (version 4.7.0 or higher)
# import plotly.graph_objects as go
# from django.shortcuts import redirect
# from custodia.models import *

# app = DjangoDash('dashboard', external_stylesheets=[dbc.themes.BOOTSTRAP])   # replaces dash.Dash

# # DESEMBOLSOS
# df_desembolsos = pd.DataFrame(list(Desembolsos.objects.all().annotate(fecha=Cast('fecha_desembolso', DateField())).order_by('-fecha_desembolso').values('fecha','estado')))

# categorias_desembolso = df_desembolsos['estado'].unique()

# # df = df.groupby('fecha_desembolso').value_counts()
# # prueba = df['estado'].value_counts()
# # df_desembolsos['fecha']=pd.to_datetime(df_desembolsos['fecha_desembolso']).dt.date
# df_desembolsos = df_desembolsos.groupby(['fecha','estado']).agg(estado_count=('estado', 'count'))
# df_desembolsos.reset_index(inplace=True)
# # print(df_desembolsos)

# # OBSERVACIONES
# df_observaciones = pd.DataFrame(list(Observaciones.objects.all().annotate(fecha=Cast('fecha_observación', DateField())).order_by('fecha_observación').values('destino', 'categoria__nombre', 'sub_categoria__nombre', 'observacion__nombre', 'glosa', 'estado', 'fecha', 'estado')))   

# categorias = df_observaciones['categoria__nombre'].unique()
# sub_categorias = df_observaciones['sub_categoria__nombre'].unique()
# observaciones = df_observaciones['observacion__nombre'].unique()


# df_observaciones = df_observaciones.groupby(['fecha','estado']).agg(categoria_count=('categoria__nombre', 'count'),observaciones_count=('observacion__nombre', 'count'), sub_categoria_count=('sub_categoria__nombre', 'count'), glosa_count=('glosa', 'count') )
# df_observaciones.reset_index(inplace=True)
# # print(df_observaciones)

# # EMPATES POR ANALISTA
# df_empates = pd.DataFrame(list(Empate.objects.all().order_by('fecha_modificacion').values('distribucion__tipo__nombre', 'usuario_empate__nombre', 'tiempo_empate', 'fecha_modificacion' )))
# df_empates['fecha']=pd.to_datetime(df_empates['fecha_modificacion']).dt.date

# empatadores = df_empates['usuario_empate__nombre'].unique()
# tipo = df_empates['distribucion__tipo__nombre'].unique()

# df_empates = df_empates.groupby(['fecha','distribucion__tipo__nombre','usuario_empate__nombre',]).agg(tiempo_promedio=('tiempo_empate','mean'), tiempo_total = ('tiempo_empate','sum'))
# df_empates.reset_index(inplace=True)
# print(df_empates)

# # APERTURAS

# df_aperturas = pd.DataFrame(list(Apertura.objects.all().order_by('-fecha_modificacion').values('fecha_modificacion','estado')))
# df_aperturas['fecha']=pd.to_datetime(df_aperturas['fecha_modificacion']).dt.date
# df_aperturas = df_aperturas.groupby(['fecha','estado']).agg(estado_count=('estado','count'))
# df_aperturas.reset_index(inplace=True)
# # print(df_aperturas)

# # PÓLIZAS

# df_polizas = pd.DataFrame(list(Poliza.objects.all().order_by('-fecha_modificacion').values('fecha_modificacion','estado')))
# df_polizas['fecha']=pd.to_datetime(df_polizas['fecha_modificacion']).dt.date
# df_polizas = df_polizas.groupby(['fecha','estado']).agg(estado_count=('estado','count'))
# df_polizas.reset_index(inplace=True)
# # print(df_polizas)

# # DOCUMENTOS SUELTOS

# df_documentos_sueltos = pd.DataFrame(list(DocumentosSueltos.objects.all().order_by('-fecha_modificacion').values('fecha_modificacion','estado')))
# df_documentos_sueltos['fecha']=pd.to_datetime(df_documentos_sueltos['fecha_modificacion']).dt.date
# df_documentos_sueltos = df_documentos_sueltos.groupby(['fecha','estado']).agg(estado_count=('estado','count'))
# df_documentos_sueltos.reset_index(inplace=True)
# # print(df_documentos_sueltos)

# # SOBRES

# df_sobres = pd.DataFrame(list(Sobre.objects.all().order_by('-fecha_creacion').values('fecha_creacion','estado')))
# df_sobres['fecha']=pd.to_datetime(df_sobres['fecha_creacion']).dt.date
# df_sobres = df_sobres.groupby(['fecha','estado']).agg(estado_count=('estado','count'))
# df_sobres.reset_index(inplace=True)
# # print(df_sobres)

# # PRESTAMOS
# df_prestamos = pd.DataFrame(list(Prestamo.objects.all().order_by('-fecha_creacion').values('fecha_creacion','estado')))
# df_prestamos['fecha']=pd.to_datetime(df_prestamos['fecha_creacion']).dt.date
# df_prestamos = df_prestamos.groupby(['fecha','estado']).agg(estado_count=('estado','count'))
# df_prestamos.reset_index(inplace=True)
# # print(df_prestamos)

# # TARJETAS
# # desembolsos = df_origen['estado'].agg('count')
# # desembolsos_pendientes = df_origen['estado'][df_origen['estado']=='Pendiente'].agg('count')
# # print(desembolsos_pendientes)

# # # Iris bar figure
# # LAYOUT
# def serve_layout():
#     return html.Div([
#     dcc.Interval(
#                 id='my_interval',
#                 disabled=False,
#                 interval=1000*3,
#                 n_intervals=0,
#                 ),
#     dbc.Card(
#         dbc.CardBody([
#             dbc.Row([
#                 dbc.Col([
#                     dbc.Card([
#                         dbc.CardBody([
#                             # html.P(f"Total: {desembolsos}"),
#                             # html.P(f"Pendientes: {desembolsos_pendientes}")
#                             ])
#                     ]),
#                 ], width=2)
#             ]),
#             dbc.Row([
#                 dbc.Col([
#                     html.Div([
#                     html.H5("Desembolsos")], style={'textAlign': 'center'}),
                
#                     dcc.DatePickerRange(
#                     id='fechas_desembolsos_id',
#                     min_date_allowed=date(1900, 1, 1),
#                     max_date_allowed=date(2099, 12, 31),
#                     initial_visible_month=df_desembolsos['fecha'].min(),
#                     start_date=date(2000, 1, 1),
#                     end_date=date(2099, 12, 31),
#                     display_format='DD-MM-YYYY'
#                 ),
#                 ], width=2),
#                 dbc.Col([
#                     dcc.Graph(id = 'grafico_desembolsos_id')
                       
#                 ], width=10),
                
#             ], align='center'), 
#             html.Br(),
#             dbc.Row([
#                 dbc.Col([
#                     html.Div([
#                     html.H5("Observaciones")], style={'textAlign': 'center'}),
                    
#                     dcc.DatePickerRange(
#                     id='fechas_observaciones_id',
#                     min_date_allowed=date(1900, 1, 1),
#                     max_date_allowed=date(2099, 12, 31),
#                     initial_visible_month=df_observaciones['fecha'].min(),
#                     start_date = date(2000, 1, 1),
#                     end_date = date(2099, 12, 31),
#                     display_format='DD-MM-YYYY'
#                     ),
#                     # dcc.Dropdown(id="categoria_id",
#                     # options=[{"label": i, "value": i} for i in categorias],
#                     # multi= False,
#                     # value='',
#                     # style={'width': "100%"}
#                     # ),
#                     # dcc.Dropdown(id="sub_categoria_id",
#                     # options=[{"label": i, "value": i} for i in sub_categorias],
#                     # multi= False,
#                     # value='',
#                     # style={'width': "100%"}
#                     # ),
#                     # dcc.Dropdown(id="observacion_id",
#                     # options=[{"label": i, "value": i} for i in observaciones],
#                     # multi= False,
#                     # value='',
#                     # style={'width': "100%"}
#                     # ),
#                 ], width=2),
#                 dbc.Col([
#                     dcc.Graph(id = 'grafico_observaciones_id')
#                 ], width=10),
#             ], align='center'), 
#             html.Br(),
#             dbc.Row([
#                 dbc.Col([
#                     html.Div([
#                     html.H5("Empates por analista")], style={'textAlign': 'center'}),

#                     dcc.DatePickerRange(
#                     id='fecha_empate',
#                     min_date_allowed=date(1900, 1, 1),
#                     max_date_allowed=date(2099, 12, 31),
#                     display_format='DD-MM-YYYY',
#                     initial_visible_month=df_empates['fecha'].min(),
#                     start_date = date(2000, 1, 1),
#                     end_date = date(2099, 12, 31),
#                     ),
#                     # dcc.Dropdown(id="empatador",
#                     # options=[
#                     #     {"label": i, "value": i} for i in empatadores
#                     #     ],
#                     # multi=False,
#                     # value= '',
#                     # style={'width': "100%"}
#                     # ),   
#                     # dcc.Dropdown(id="tipo",
#                     # options=[
#                     #     {"label": i, "value": i} for i in tipo
#                     #     ],
#                     # multi=False,
#                     # value=tipo[0],
#                     # style={'width': "100%"}
#                     # ),  
#                 ], width=2),
#                 dbc.Col([
#                     # dcc.Graph(id = 'grafico_empate_1_id'),
#                     dcc.Graph(id = 'grafico_empate_2_id'),
#                 ], width=10),
#             ], align='center'),
#             dbc.Row([
#                 dbc.Col([
#                     html.Div([
#                     html.H5("Aperturas")], style={'textAlign': 'center'}),

#                     dcc.DatePickerRange(
#                     id='fecha_aperturas',
#                     min_date_allowed=date(1900, 1, 1),
#                     max_date_allowed=date(2099, 12, 31),
#                     display_format='DD-MM-YYYY',
#                     initial_visible_month=df_aperturas['fecha'].min(),
#                     start_date = date(2000, 1, 1),
#                     end_date = date(2099, 12, 31),
#                     ),    
#                 ], width = 2),
#                 dbc.Col([
#                     dcc.Graph(id ='grafico_aperturas_id') 
#                 ], width = 10)
#             ], align='center'),
#             dbc.Row([
#                 dbc.Col([
#                     html.Div([
#                     html.H5("Pólizas")], style={'textAlign': 'center'}),

#                     dcc.DatePickerRange(
#                     id='fecha_polizas',
#                     min_date_allowed=date(1900, 1, 1),
#                     max_date_allowed=date(2099, 12, 31),
#                     display_format='DD-MM-YYYY',
#                     initial_visible_month=df_polizas['fecha'].min(),
#                     start_date = date(2000, 1, 1),
#                     end_date = date(2099, 12, 31),
#                     ),        
#                 ], width=2),
#                 dbc.Col([
#                     dcc.Graph(id = 'grafico_polizas_id')
#                 ], width=10)
#             ], align='center'),
#             dbc.Row([
#                 dbc.Col([
#                     html.Div([
#                     html.H5("Documentos Sueltos")], style={'textAlign': 'center'}),

#                     dcc.DatePickerRange(
#                     id='fecha_documentos_sueltos',
#                     min_date_allowed=date(1900, 1, 1),
#                     max_date_allowed=date(2099, 12, 31),
#                     display_format='DD-MM-YYYY',
#                     initial_visible_month=df_documentos_sueltos['fecha'].min(),
#                     start_date = date(2000, 1, 1),
#                     end_date = date(2099, 12, 31),
#                     ),            
#                 ], width = 2),
#                 dbc.Col([
#                     dcc.Graph(id = 'grafico_documentos_sueltos_id')    
#                 ], width = 10)
#             ], align='center'),
#             dbc.Row([
#                 dbc.Col([
#                     html.Div([
#                     html.H5("Sobres")], style={'textAlign': 'center'}),

#                     dcc.DatePickerRange(
#                     id='fecha_sobres',
#                     min_date_allowed=date(1900, 1, 1),
#                     max_date_allowed=date(2099, 12, 31),
#                     display_format='DD-MM-YYYY',
#                     initial_visible_month=df_sobres['fecha'].min(),
#                     start_date = date(1900, 1, 1),
#                     end_date = date(2099, 12, 31),
#                     )    
#                 ], width=2),
#                 dbc.Col([
#                     dcc.Graph(id = 'grafico_sobres_id')    
#                 ], width=9)
#             ], align='center'),
#             dbc.Row([
#                 dbc.Col([
#                     html.Div([
#                     html.H5("Préstamos")], style={'textAlign': 'center'}),

#                     dcc.DatePickerRange(
#                     id='fecha_prestamos',
#                     min_date_allowed=date(1900, 1, 1),
#                     max_date_allowed=date(2099, 12, 31),
#                     display_format='DD-MM-YYYY',
#                     initial_visible_month=df_prestamos['fecha'].min(),
#                     start_date = date(1900, 1, 1),
#                     end_date = date(2099, 12, 31),
#                     )        
#                 ], width=2),
#             dbc.Col([
#                     dcc.Graph(id = 'grafico_prestamos_id')  
#                 ], width=10)
#             ], align='center'),
#             dbc.Row([], align='center'),
#         ]), color = 'light'
#     )
# ])

# app.layout = serve_layout

# @app.callback(
#     Output(component_id = 'grafico_desembolsos_id', component_property= 'figure'),
#     [Input('my_interval', 'n_intervals'),
#     Input('fechas_desembolsos_id', 'start_date'),
#     Input('fechas_desembolsos_id', 'end_date'),
#     ])
# def grafico_desembolsos(n, start_date, end_date):
#     df_desembolsos = pd.DataFrame(list(Desembolsos.objects.all().annotate(fecha=Cast('fecha_desembolso', DateField())).order_by('-fecha_desembolso').values('fecha','estado')))

#     categorias_desembolso = df_desembolsos['estado'].unique()

#     # df = df.groupby('fecha_desembolso').value_counts()
#     # prueba = df['estado'].value_counts()
#     # df_desembolsos['fecha']=pd.to_datetime(df_desembolsos['fecha_desembolso']).dt.date
#     df_desembolsos = df_desembolsos.groupby(['fecha','estado']).agg(estado_count=('estado', 'count'))
#     df_desembolsos.reset_index(inplace=True)
#     # print(df_desembolsos)

#     start_date_object_d = date.fromisoformat(start_date)
#     end_date_object_d = date.fromisoformat(end_date)
#     dff = df_desembolsos[df_desembolsos["fecha"].between(start_date_object_d, end_date_object_d)]

#     fig = px.bar(
#         data_frame=dff, 
#         title = "Desembolsos",
#         x='fecha', 
#         y='estado_count',
#         color='estado').update_layout(xaxis_title="Fecha", yaxis_title="N desembolsos")
#     return fig

# @app.callback(
#     Output(component_id = 'grafico_observaciones_id', component_property= 'figure'),
#     [Input('fechas_observaciones_id', 'start_date'),
#     Input('fechas_observaciones_id', 'end_date'),
#     # Input(component_id = 'categoria_id', component_property = 'value'),
#     # Input(component_id = 'sub_categoria_id', component_property = 'value'),
#     # Input(component_id = 'observacion_id', component_property = 'value')
#     ]
# )
# def grafico_observaciones(start_date, end_date):
    
#     df_observaciones = pd.DataFrame(list(Observaciones.objects.all().annotate(fecha=Cast('fecha_observación', DateField())).order_by('fecha_observación').values('destino', 'categoria__nombre', 'sub_categoria__nombre', 'observacion__nombre', 'glosa', 'estado', 'fecha', 'estado')))   

#     categorias = df_observaciones['categoria__nombre'].unique()
#     sub_categorias = df_observaciones['sub_categoria__nombre'].unique()
#     observaciones = df_observaciones['observacion__nombre'].unique()


#     df_observaciones = df_observaciones.groupby(['fecha','estado']).agg(categoria_count=('categoria__nombre', 'count'),observaciones_count=('observacion__nombre', 'count'), sub_categoria_count=('sub_categoria__nombre', 'count'), glosa_count=('glosa', 'count') )
#     df_observaciones.reset_index(inplace=True)
#     # print(df_observaciones)
    
    
#     # categoria, sub_categoria, observacion,
#     start_date_object = date.fromisoformat(start_date)
#     end_date_object = date.fromisoformat(end_date)
    
#     dff = df_observaciones[df_observaciones["fecha"].between((start_date_object),(end_date_object))]
#     # dff = dff[dff['categoria__nombre'] == categoria]
#     # dff = dff[dff['sub_categoria__nombre'] == sub_categoria]
#     # dff = dff[dff['observacion__nombre'] == observacion]
    
#     fig = px.scatter(
#         data_frame= dff, 
#         title = "Observaciones",
#         x='fecha', 
#         y='glosa_count', 
#         size='observaciones_count',
#         color = 'estado').update_layout(xaxis_title = "Fecha", yaxis_title = "Nº Observaciones")
#     return fig

# # @app.callback(
# #     Output(component_id = 'grafico_empate_1_id', component_property= 'figure'),
# #     [Input('fecha_empate', 'start_date'),
# #     Input('fecha_empate', 'end_date'),
# #     Input(component_id = 'empatador', component_property = 'value'),
# #     Input(component_id = 'tipo', component_property = 'value')
# #     ]
# # )
# # def grafico_empate_1(start_date, end_date, empatador, tipo):

# #     start_date_object = date.fromisoformat(start_date)
# #     end_date_object = date.fromisoformat(end_date)
    
# #     dff = df_empates[df_empates["fecha"].between((start_date_object),(end_date_object))]
# #     dff = dff[dff['usuario_empate__nombre'] == empatador]
# #     df= px.bar(
# #         data_frame=dff,
# #         title = "Tiempos de empate por fecha", 
# #         x='fecha', y='tiempo_total', 
# #         colorf = dff[dff['distribucion__tipo__nombre'] == tipo]
    
# #     fig ='tiempo_promedio').update_layout(xaxis_title= "Fecha", yaxis_title= "Tiempo Total")
# #     return fig

# @app.callback(
#     Output(component_id = 'grafico_empate_2_id', component_property= 'figure'),
#     [Input('fecha_empate', 'start_date'),
#     Input('fecha_empate', 'end_date'),
#     # Input(component_id = 'tipo', component_property = 'value')
#     ]
# )
# def grafico_empate_2(start_date, end_date):
#     df_empates = pd.DataFrame(list(Empate.objects.all().order_by('fecha_modificacion').values('distribucion__tipo__nombre', 'usuario_empate__nombre', 'tiempo_empate', 'fecha_modificacion' )))
#     df_empates['fecha']=pd.to_datetime(df_empates['fecha_modificacion']).dt.date

#     empatadores = df_empates['usuario_empate__nombre'].unique()
#     tipo = df_empates['distribucion__tipo__nombre'].unique()

#     df_empates = df_empates.groupby(['fecha','distribucion__tipo__nombre','usuario_empate__nombre',]).agg(tiempo_promedio=('tiempo_empate','mean'), tiempo_total = ('tiempo_empate','sum'))
#     df_empates.reset_index(inplace=True)

#     start_date_object = date.fromisoformat(start_date)
#     end_date_object = date.fromisoformat(end_date)
    
#     dff = df_empates[df_empates["fecha"].between((start_date_object),(end_date_object))]
#     # dff = dff[dff['distribucion__tipo__nombre'] == tipo]
    
#     fig = px.bar(
#             data_frame= dff, 
#             title= 'Tiempos de empate por analista', 
#             x='usuario_empate__nombre', 
#             y='tiempo_promedio', 
#             color='distribucion__tipo__nombre').update_layout(xaxis_title="Analista", yaxis_title="Tiempo Total")
#     return fig

# @app.callback(
#     Output(component_id = 'grafico_aperturas_id', component_property= 'figure'),
#     [Input('fecha_aperturas', 'start_date'),
#     Input('fecha_aperturas', 'end_date'),
#     ]
# )
# def grafico_aperturas(start_date, end_date):

#     df_aperturas = pd.DataFrame(list(Apertura.objects.all().order_by('-fecha_modificacion').values('fecha_modificacion','estado')))
#     df_aperturas['fecha']=pd.to_datetime(df_aperturas['fecha_modificacion']).dt.date
#     df_aperturas = df_aperturas.groupby(['fecha','estado']).agg(estado_count=('estado','count'))
#     df_aperturas.reset_index(inplace=True)

#     start_date_object = date.fromisoformat(start_date)
#     end_date_object = date.fromisoformat(end_date)
    
#     dff = df_aperturas[df_aperturas["fecha"].between((start_date_object),(end_date_object))]
    
#     fig = px.bar(
#             data_frame= dff, 
#             title= 'Aperturas', 
#             x='fecha', 
#             y='estado_count', 
#             color='estado').update_layout(xaxis_title="Fecha", yaxis_title="Nº Aperturas")
#     return fig

# @app.callback(
#     Output(component_id = 'grafico_polizas_id', component_property= 'figure'),
#     [Input('fecha_polizas', 'start_date'),
#     Input('fecha_polizas', 'end_date'),
#     ]
# )
# def grafico_polizas(start_date, end_date):

#     df_polizas = pd.DataFrame(list(Poliza.objects.all().order_by('-fecha_modificacion').values('fecha_modificacion','estado')))
#     df_polizas['fecha']=pd.to_datetime(df_polizas['fecha_modificacion']).dt.date
#     df_polizas = df_polizas.groupby(['fecha','estado']).agg(estado_count=('estado','count'))
#     df_polizas.reset_index(inplace=True)

#     start_date_object = date.fromisoformat(start_date)
#     end_date_object = date.fromisoformat(end_date)
    
#     dff = df_polizas[df_polizas["fecha"].between((start_date_object),(end_date_object))]
    
#     fig = px.bar(
#             data_frame= dff, 
#             title= 'Pólizas', 
#             x='fecha', 
#             y='estado_count', 
#             color='estado').update_layout(xaxis_title="Fecha", yaxis_title="Nº Pólizas")
#     return fig

# @app.callback(
#     Output(component_id = 'grafico_documentos_sueltos_id', component_property= 'figure'),
#     [Input('fecha_documentos_sueltos', 'start_date'),
#     Input('fecha_documentos_sueltos', 'end_date'),
#     ]
# )
# def grafico_documentos_sueltos(start_date, end_date):

#     df_documentos_sueltos = pd.DataFrame(list(DocumentosSueltos.objects.all().order_by('-fecha_modificacion').values('fecha_modificacion','estado')))
#     df_documentos_sueltos['fecha']=pd.to_datetime(df_documentos_sueltos['fecha_modificacion']).dt.date
#     df_documentos_sueltos = df_documentos_sueltos.groupby(['fecha','estado']).agg(estado_count=('estado','count'))
#     df_documentos_sueltos.reset_index(inplace=True)

#     start_date_object = date.fromisoformat(start_date)
#     end_date_object = date.fromisoformat(end_date)
    
#     dff = df_documentos_sueltos[df_documentos_sueltos["fecha"].between((start_date_object),(end_date_object))]
    
#     fig = px.bar(
#             data_frame= dff, 
#             title= 'Documentos Sueltos', 
#             x='fecha', 
#             y='estado_count', 
#             color='estado').update_layout(xaxis_title="Fecha", yaxis_title="Nº Documentos Sueltos")
#     return fig

# @app.callback(
#     Output(component_id = 'grafico_sobres_id', component_property= 'figure'),
#     [Input('fecha_sobres', 'start_date'),
#     Input('fecha_sobres', 'end_date'),
#     ]
# )
# def grafico_sobres(start_date, end_date):

#     df_sobres = pd.DataFrame(list(Sobre.objects.all().order_by('-fecha_creacion').values('fecha_creacion','estado')))
#     df_sobres['fecha']=pd.to_datetime(df_sobres['fecha_creacion']).dt.date
#     df_sobres = df_sobres.groupby(['fecha','estado']).agg(estado_count=('estado','count'))
#     df_sobres.reset_index(inplace=True)

#     start_date_object = date.fromisoformat(start_date)
#     end_date_object = date.fromisoformat(end_date)
    
#     dff = df_sobres[df_sobres["fecha"].between((start_date_object),(end_date_object))]
    
#     fig = px.bar(
#             data_frame= dff, 
#             title= 'Sobres', 
#             x='fecha', 
#             y='estado_count', 
#             color='estado').update_layout(xaxis_title="Fecha", yaxis_title="Nº Sobres")
#     return fig

# @app.callback(
#     Output(component_id = 'grafico_prestamos_id', component_property= 'figure'),
#     [Input('fecha_prestamos', 'start_date'),
#     Input('fecha_prestamos', 'end_date'),
#     ]
# )
# def grafico_prestamos(start_date, end_date):

#     df_prestamos = pd.DataFrame(list(Prestamo.objects.all().order_by('-fecha_creacion').values('fecha_creacion','estado')))
#     df_prestamos['fecha']=pd.to_datetime(df_prestamos['fecha_creacion']).dt.date
#     df_prestamos = df_prestamos.groupby(['fecha','estado']).agg(estado_count=('estado','count'))
#     df_prestamos.reset_index(inplace=True)

#     start_date_object = date.fromisoformat(start_date)
#     end_date_object = date.fromisoformat(end_date)
    
#     dff = df_prestamos[df_prestamos["fecha"].between((start_date_object),(end_date_object))]
    
#     fig = px.bar(
#             data_frame= dff, 
#             title= 'Préstamos', 
#             x='fecha', 
#             y='estado_count', 
#             color='estado').update_layout(xaxis_title="Fecha", yaxis_title="Nº Préstamos")
#     return fig