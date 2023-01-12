import requests
import pandas as pd
import numpy as np

list_id = "187019727"
url = "https://api.clickup.com/api/v2/list/" + list_id + "/task"

query = {
  "archived": "True",
  "page": "0",
  "reverse": "true",
  #"subtasks": "false",
  "include_closed": "true"
}

headers = {
  "Content-Type": "application/json",
  "Authorization": "pk_43022943_BG7N2IWWCEB36JHO7PNS71EQEP2M7K30"
}

#1ª ideia, aprender a ler o Json e transformar em df
#2ª Transformar Json em dict e ler como DF
response = requests.get(url, headers=headers, params=query)
json = []
data = response.json()

def organizar_json(data):

  list_id_itens = ["1e5c6ba4-aa42-49e0-8b21-4a1ca1cc4635", "30881d36-37f8-4736-b2d5-e8d9d771df99", "d6ee9063-4d4e-4677-b66f-9950db5f17a1", "94899730-a87f-4fd6-964b-b149a796ee85", "8f11bbbd-32d7-42e0-90bd-85d2218061a7", "30fcc6ad-662c-4c3b-9195-29ca24e2bc4f", "54fcdfdd-6ea6-4a4a-b27c-99b84affaaca"]
  lista_Json = []

  for i in data['tasks']:
    list_apoio = []
    nome = i['name']
    status = i['status']['status']
    date_Criacao = i['date_created']
    date_update = i['date_updated']
    date_closed = i['date_closed']
    for y in i['custom_fields']:
      if y['id'] in list_id_itens:
        try:
          list_apoio.append([y['name'], y['value']])
        except KeyError:
          list_apoio.append([y['name'], 'none'])
    
    #x.append(list_apoio)
    lista_Json.append([nome, status, date_Criacao, date_update, date_closed, list_apoio])
  return lista_Json

json = organizar_json(data)

lista_organizada = []
colunas = ['sprint', 'status', 'dateCreate', 'dateUpdate', 'dateClosed', 'nome', 'pontos']

for spt in json:
  for valorSpt in spt[5]:
    sprint = spt[0]
    status = spt[1]
    data_criacao = spt[2]
    data_update = spt[3]
    data_fechamento = spt[4]
    nome = valorSpt[0]
    pontos = valorSpt[1]

    lista_organizada.append(
      [sprint, 
      status, 
      data_criacao,
      data_update,
      data_fechamento,
      nome,
      pontos] 
    )

df = pd.DataFrame(lista_organizada, columns=colunas)