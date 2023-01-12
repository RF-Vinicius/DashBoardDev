import requests
import dash
from dash import html, dcc, Input, Output
#from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import datetime

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],
        suppress_callback_exceptions=True)

app.scripts.config.serve_locally = True
server = app.server

json = []

def requisicao(pagina):
    
    #==========Import e tratamento dos dados=========#
    list_id = "187019727"
    url = "https://api.clickup.com/api/v2/list/" + list_id + "/task"

    query = {
    "archived": "True",
    "page": pagina,
    "reverse": "true",
    "subtasks": "true",
    "include_closed": "true"
    }

    headers = {
    "Content-Type": "application/json",
    "Authorization": "pk_43022943_BG7N2IWWCEB36JHO7PNS71EQEP2M7K30"
    }

    response = requests.get(url, headers=headers, params=query)
    data = response.json()
    return data


def organizar_json(data):
  lista_Json = []  
  list_id_itens = ["1e5c6ba4-aa42-49e0-8b21-4a1ca1cc4635", "30881d36-37f8-4736-b2d5-e8d9d771df99", "d6ee9063-4d4e-4677-b66f-9950db5f17a1", "94899730-a87f-4fd6-964b-b149a796ee85", "8f11bbbd-32d7-42e0-90bd-85d2218061a7", "30fcc6ad-662c-4c3b-9195-29ca24e2bc4f", "54fcdfdd-6ea6-4a4a-b27c-99b84affaaca"]
  for i in data['tasks']:
    list_apoio = []
    for y in i['custom_fields']:
      if y['id'] in list_id_itens:
        try:
          list_apoio.append([y['name'], float(y['value'])])
        except KeyError:
          list_apoio.append([y['name'], np.nan])
    if str(type(i['parent'])) == "<class 'NoneType'>":
        id = i['id']
        id_pai = 'Null'
        sprint = i['name']
        status = i['status']['status']
        date_Criacao = i['date_created']
        date_update = i['date_updated']
    else:
        id = i['id']
        id_pai = i['parent']
        status = i['name']
        date_Criacao = i['date_created']
        date_update = i['date_updated']
     
    lista_Json.append([sprint, status, date_Criacao, date_update, list_apoio, id, id_pai])
  return lista_Json


for i in range(2):
    json += organizar_json(requisicao(i))

lista_organizada = []
colunas = ['id','id_pai','sprint', 'status', 'dateCreate', 'dateUpdate', 'nome', 'pontos']

for spt in json:
  for valorSpt in spt[4]:
    sprint = spt[0]
    status = spt[1]
    data_criacao = spt[2]
    data_update = spt[3]
    nome = valorSpt[0]
    pontos = valorSpt[1]
    id = spt[-2]
    id_pai = spt[-1]

    lista_organizada.append(
      [id,
      id_pai,
      sprint, 
      status, 
      data_criacao,
      data_update,
      nome,
      pontos] 
    )

df = pd.DataFrame(lista_organizada, columns=colunas)
df['dateCreate'] = df['dateCreate'].apply(lambda x: int(x))
df = df.dropna()
#df["dateCreate"] = df["dateCreate"].apply(lambda d: datetime.date.fromtimestamp(int(d)/1000.0))
#df["dateUpdate"] = df["dateUpdate"].apply(lambda d: datetime.date.fromtimestamp(int(d)/1000.0))

#=================Layout==================#
app.layout = html.Div(children=[
                dbc.Row([

                    dbc.Row([
                        dbc.Col([
                            dbc.Row([
                                dcc.Dropdown(
                                    df["nome"].value_counts().index,
                                    df["nome"].value_counts().index,
                                    multi=True,
                                    id='list_dev',
                                    style={"color": "black"}
                                )
                            ])
                        ], md=6),

                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Input(placeholder="dd/mm/yyyy", id='data-inicio', value='0'),
                                ], md=6),
                                dbc.Col([
                                    dbc.Input(placeholder="dd/mm/yyyy", id='data-fim', value='0'),
                                ], md=6)
                            ])
                        ], md= 6),

                    ], align="center", style={"margin-bottom": "16px", "border-radius": "10px", "background-color": "#4E4E4E", "height": "75px"}),

                    dbc.Row([
                        dbc.Col([
                            dbc.Row([
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.H5("Executado (%)", className="card-title"),
                                            html.H3(className="card-title", id="porcentagem-executado-planejado")
                                        ]
                                    ),
                                style={"width": "18rem", "text-align": "center"},
                            )
                            ], justify='center')
                        ], md=2),

                        dbc.Col([
                            dbc.Row([
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.H5("Média por pessoa", className="card-title"),
                                            html.H3(className="card-title", id="media-por-pessoa")
                                        ]
                                    ),
                                style={"width": "18rem", "text-align": "center"},
                            )
                            ], justify='center')
                        ], md=2),

                        dbc.Col([
                            dbc.Row([
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.H5("Média da equipe", className="card-title"),
                                            html.H3(className="card-title", id="media-equipe")
                                        ]
                                    ),
                                style={"width": "18rem", "text-align": "center"},
                            )
                            ], justify='center')
                        ], md=2),

                        dbc.Col([
                            dbc.Row([
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.H5("Pontuação máxima", className="card-title"),
                                            html.H3(className="card-title", id="max-pontos-equipe")
                                        ]
                                    ),
                                style={"width": "18rem", "text-align": "center"},
                            )
                            ], justify='center')
                        ], md=2),

                        dbc.Col([
                            dbc.Row([
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.H5("Pontuação mínima", className="card-title"),
                                            html.H3(className="card-title", id="min-pontos-equipe")
                                        ]
                                    ),
                                style={"width": "18rem", "text-align": "center"},
                            )
                            ], justify='center')
                        ], md=2)

                        ],justify='center', style={"margin-bottom": "16px"}),

                        dbc.Row([
                            dbc.Col(dcc.Graph(id="Desempenho-dev"), md=6, ),
                            dbc.Col(dcc.Graph(id="planejado-executado"), md=6)
                        ], style={"margin-bottom": "16px"}),

                        dbc.Row([
                            dbc.Col(dcc.Graph(id="dante"), md=4),
                            dbc.Col(dcc.Graph(id="ricson"), md=4),
                            dbc.Col(dcc.Graph(id="lopes"), md=4),
                        ], style={"margin-bottom": "16px"}), 

                        dbc.Row([
                            dbc.Col(dcc.Graph(id="gama"), md=4),
                            dbc.Col(dcc.Graph(id="lucas"), md=4),
                            dbc.Col(dcc.Graph(id="joao"), md=4),
                        ], style={"margin-bottom": "16px"}), 

                    ],  style={"margin": "25px", "text-align": "center",}, justify="center")
            ], style={})


#======Callback=======#

def filtroData(dataframe, data_inicio, data_fim):
    
    try:
        data_inicio = time.mktime(datetime.datetime.strptime(data_inicio , "%d/%m/%Y").timetuple())
        data_fim = time.mktime(datetime.datetime.strptime(data_fim , "%d/%m/%Y").timetuple())
        dataFrameFilter = dataframe[dataframe['dateCreate'] / 1000 >= data_inicio]
        dataFrameFilter = dataFrameFilter[dataFrameFilter['dateCreate'] / 1000 <= data_fim]
    except ValueError:
        dataFrameFilter = dataframe

    return dataFrameFilter


@app.callback(
                Output("media-por-pessoa", "children"),
                Output("media-equipe", "children"),
                Output("max-pontos-equipe", "children"),
                Output("min-pontos-equipe", "children"),
                Output('porcentagem-executado-planejado', 'children'),
            
                [
                    Input("list_dev", "value"),
                    Input("data-inicio", "value"),
                    Input("data-fim", "value"),
                ])
def big_numbers(list_dev, data_inicio, data_fim):
    """data_inicio = '01/10/2022'
    data_fim = '31/12/2022'"""

    #list_dev = ['Dante', 'Dionísio', 'Leandro', 'Leandro Gama', 'Lopes', 'Lucas', 'Ricson']
    df_list_por_dev = df[df["nome"].isin(list_dev)]
    df_list_por_dev = filtroData(df_list_por_dev, data_inicio, data_fim).dropna()
    df_media = df_list_por_dev[df_list_por_dev["status"] == "executado"]['pontos'].mean()
    df_media_time = df_list_por_dev[df_list_por_dev["status"] == "executado"].groupby('sprint').sum().mean()
    df_max_pontos = df_list_por_dev[df_list_por_dev["status"] == "executado"].groupby('sprint').sum().max()
    df_min_pontos = df_list_por_dev[df_list_por_dev["status"] == "executado"].groupby('sprint').sum().min()
    df_planejado_para = df_list_por_dev[df_list_por_dev["status"] == "planejado para semana"].groupby('sprint').sum().mean()['pontos']
    df_executado = df_list_por_dev[df_list_por_dev["status"] == "Planejado"].groupby('sprint').sum().mean()['pontos']
    porcentagem = (df_executado * 100)/df_planejado_para
    return round(df_media, 2), round(df_media_time['pontos'], 2), round(df_max_pontos['pontos'], 2), round(df_min_pontos['pontos'], 2), round(porcentagem, 2)


@app.callback([
                Output("Desempenho-dev", "figure"),
            ], 
                [
                    Input("list_dev", "value"),
                    Input("data-inicio", "value"),
                    Input("data-fim", "value"),
                ])
def desempenho_dev(list_dev, data_inicio, data_fim):

    """list_dev = ['Dante', 'Dionísio', 'Leandro', 'Leandro Gama', 'Lopes', 'Lucas', 'Ricson']
    data_inicio = '01/08/2022'
    data_fim = '01/12/2022'"""
    df_desempenho = df[df["nome"].isin(list_dev)]
    df_desempenho = filtroData(df_desempenho, data_inicio, data_fim)
    
    #df_desempenho['mes'] = df['dateCreate'].apply(lambda x: x.month)
    #df_desempenho = df_desempenho[df_desempenho['status'] == 'executado']
    df_desempenho = df_desempenho.groupby(["sprint","dateCreate", 'status']).sum('pontos').reset_index().sort_values('dateCreate')
    
    fi_desempenho = go.Figure(data=[
        go.Bar(name='Planejado', x=np.array(df_desempenho[df_desempenho['status'] == 'Planejado']['sprint']), y=np.array(df_desempenho[df_desempenho['status'] == 'Planejado']['pontos']), marker_color="#78736E"),
        go.Bar(name='Imprevisto', x=np.array(df_desempenho[df_desempenho['status'] == 'Imprevisto']['sprint']), y=np.array(df_desempenho[df_desempenho['status'] == 'Imprevisto']['pontos']), marker_color="#A80101"),
        go.Bar(name='Suporte', x=np.array(df_desempenho[df_desempenho['status'] == 'Suporte']['sprint']), y=np.array(df_desempenho[df_desempenho['status'] == 'Suporte']['pontos']), marker_color="#FF6B00")
    ])

    fi_desempenho.update_layout(barmode='stack', title_text='Executado por sprint')

    return [go.Figure(data=fi_desempenho)]
    
    
@app.callback([
                Output("planejado-executado", "figure"),
            ], 
                [
                    Input("list_dev", "value"),
                    Input("data-inicio", "value"),
                    Input("data-fim", "value"),
                ])
def planejado_executado(list_dev, data_inicio, data_fim):
    #list_dev = ['Dante', 'Dionísio', 'Leandro', 'Leandro Gama', 'Lopes', 'Lucas', 'Ricson']
    list_status = ['planejado para semana', 'executado']
    df_list_dev_filter = df[df["nome"].isin(list_dev)]
    df_list_dev_filter = filtroData(df_list_dev_filter, data_inicio, data_fim)
    df_list_dev_filter = df_list_dev_filter[df_list_dev_filter['status'].isin(list_status)]
    df_planejado_executado = df_list_dev_filter = df_list_dev_filter.groupby(["sprint","dateCreate", 'status']).sum('pontos').reset_index().sort_values('dateCreate')
    
    fig_planejado_executado = px.line(df_planejado_executado, x="sprint", y="pontos", color="status", line_shape="spline", color_discrete_sequence=["#78736E", "#31B236"], title='Executado vs Planejado')
    return [go.Figure(data=fig_planejado_executado)]


@app.callback(
                Output("dante", "figure"),
                Output("ricson", "figure"),
                Output("lopes", "figure"),
                Output("gama", "figure"),
                Output("lucas", "figure"),
                Output("joao", "figure"),
                [
                    Input("data-inicio", "value"),
                    Input("data-fim", "value"),
                ])
def relatorio_por_dev(data_inicio, data_fim):

    df_dev = df[df['status'] == "executado"]
    df_dev_filter = filtroData(df_dev, data_inicio, data_fim)
    
    df_dev_filter['media'] = df_dev_filter['pontos'].mean()
    df_dante = df_dev_filter[df_dev_filter['nome'] == 'Dante'][['sprint', 'pontos', 'nome', 'media']]
    df_dante['media dev'] = df_dante['pontos'].mean()

    df_ricson = df_dev_filter[df_dev_filter['nome'] == 'Ricson'][['sprint', 'pontos', 'nome', 'media']]
    df_ricson['media dev'] = df_ricson['pontos'].mean()

    df_lopes = df_dev_filter[df_dev_filter['nome'] == 'Lopes'][['sprint', 'pontos', 'nome', 'media']]
    df_lopes['media dev'] = df_lopes['pontos'].mean()

    df_gama = df_dev_filter[df_dev_filter['nome'] == 'Leandro Gama'][['sprint', 'pontos', 'nome', 'media']]
    df_gama['media dev'] = df_gama['pontos'].mean()

    df_Lucas = df_dev_filter[df_dev_filter['nome'] == 'Lucas'][['sprint', 'pontos', 'nome', 'media']]
    df_Lucas['media dev'] = df_Lucas['pontos'].mean()

    df_joao = df_dev_filter[df_dev_filter['nome'] == 'Dionísio'][['sprint', 'pontos', 'nome', 'media']]
    df_joao['media dev'] = df_joao['pontos'].mean()


    cor_media_time = "#000000"
    cor_media_dev = "#A80101"

#Dante
    fig_dante = go.Figure()
    fig_dante.add_trace(go.Bar(
        name="Dante",
        x=np.array(df_dante['sprint']), 
        y=np.array(df_dante['pontos']),
        marker_color = "#31B236"
    ))
    fig_dante.add_trace(go.Scatter(
        name="Média do time",
        x=np.array(df_dante['sprint']), 
        y=np.array(df_dante['media']),
        marker_color = cor_media_time,
    ))
    fig_dante.add_trace(go.Scatter(
        name="Média dev",
        x=np.array(df_dante['sprint']), 
        y=np.array(df_dante['media dev']),
        marker_color = cor_media_dev,
    ))
    fig_dante.update_layout(title_text='Dante')
        
#Ricson
    fig_ricson = go.Figure()
    fig_ricson.add_trace(go.Bar(
        name="Ricson",
        x=np.array(df_ricson['sprint']), 
        y=np.array(df_ricson['pontos']),
        marker_color = "#31B236"
    ))
    fig_ricson.add_trace(go.Scatter(
        name="Média do time",
        x=np.array(df_ricson['sprint']), 
        y=np.array(df_ricson['media']),
        marker_color = cor_media_time,
    ))
    fig_ricson.add_trace(go.Scatter(
        name="Média dev",
        x=np.array(df_ricson['sprint']), 
        y=np.array(df_ricson['media dev']),
        marker_color = cor_media_dev,
    ))
    fig_ricson.update_layout(title_text='Ricson')

#Lopes
    fig_lopes = go.Figure()
    fig_lopes.add_trace(go.Bar(
        name="Lopes",
        x=np.array(df_lopes['sprint']), 
        y=np.array(df_lopes['pontos']),
        marker_color = "#31B236"
    ))
    fig_lopes.add_trace(go.Scatter(
        name="Média do time",
        x=np.array(df_lopes['sprint']), 
        y=np.array(df_lopes['media']),
        marker_color = cor_media_time,
    ))
    fig_lopes.add_trace(go.Scatter(
        name="Média dev",
        x=np.array(df_lopes['sprint']), 
        y=np.array(df_lopes['media dev']),
        marker_color = cor_media_dev,
    ))
    fig_lopes.update_layout(title_text='Lopes')

#Leandro Gama
    fig_gama = go.Figure()
    fig_gama.add_trace(go.Bar(
        name="Gama",
        x=np.array(df_gama['sprint']), 
        y=np.array(df_gama['pontos']),
        marker_color = "#31B236"
    ))
    fig_gama.add_trace(go.Scatter(
        name="Média do time",
        x=np.array(df_gama['sprint']), 
        y=np.array(df_gama['media']),
        marker_color = cor_media_time,
    ))
    fig_gama.add_trace(go.Scatter(
        name="Média dev",
        x=np.array(df_gama['sprint']), 
        y=np.array(df_gama['media dev']),
        marker_color = cor_media_dev,
    ))
    fig_gama.update_layout(title_text='Gama')

#Lucas
    fig_lucas = go.Figure()
    fig_lucas.add_trace(go.Bar(
        name="Lucas",
        x=np.array(df_Lucas['sprint']), 
        y=np.array(df_Lucas['pontos']),
        marker_color = "#31B236"
    ))
    fig_lucas.add_trace(go.Scatter(
        name="Média do time",
        x=np.array(df_Lucas['sprint']), 
        y=np.array(df_Lucas['media']),
        marker_color = cor_media_time,
    ))
    fig_lucas.add_trace(go.Scatter(
        name="Média dev",
        x=np.array(df_Lucas['sprint']), 
        y=np.array(df_Lucas['media dev']),
        marker_color = cor_media_dev,
    ))
    fig_lucas.update_layout(title_text='Lucas')

#João
    fig_joao = go.Figure()
    fig_joao.add_trace(go.Bar(
        name="João",
        x=np.array(df_joao['sprint']), 
        y=np.array(df_joao['pontos']),
        marker_color = "#31B236"
    ))
    fig_joao.add_trace(go.Scatter(
        name="Média do time",
        x=np.array(df_joao['sprint']), 
        y=np.array(df_joao['media']),
        marker_color = cor_media_time,
    ))
    fig_joao.add_trace(go.Scatter(
        name="Média dev",
        x=np.array(df_joao['sprint']), 
        y=np.array(df_joao['media dev']),
        marker_color = cor_media_dev,
    ))
    fig_joao.update_layout(title_text='João')

    return go.Figure(data=fig_dante), go.Figure(data=fig_ricson), go.Figure(data=fig_lopes), go.Figure(data=fig_gama), go.Figure(data=fig_lucas), go.Figure(data=fig_joao)

if __name__ == "__main__":
    app.run_server(debug=True, port='8051')