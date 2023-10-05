#API DA SANTANDER DEV.WEEK#

sdw2023_api_url = "https://sdw-2023-prd.up.railway.app"

import pandas as pd

df = pd.read_csv('PROJETO-ETL-PYTHON.csv')
user_ids = df['UserID'].tolist()
print(user_ids)

import requests
import json

def get_user(id):
  response = requests.get(f'{sdw2023_api_url}/users/{id}')
  return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))


!pip install openai

openai_api_key = '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'

import openai

openai.api_key = openai_api_key

def generate_ai_news(user): 
 completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
          {
          "role": "system",
          "content":"Você é um especialista de Marketing Financeiro de uma agencia bancaria."
          },
          {
          "role": "user",
          "content": f"Crie uma mensagem para o {user['name']} sobre a importância da segurança financeira, os risco e as possibilidades de investimento e segurança que a empresa oferece, (máximo de 200 caracteres)."
          }
        ]
      )
 return completion.choices[0].message.content.strip('\"')

for user in users:
  news = generate_ai_news(user)
  print(news)
  user['news'].append({
      "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icon/credit.svg",
      "descripition": news
  })

      
def update_user(user_id):
    response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
    return True if response.status_code == 200 else False

for user_id in user_ids: 
    success = update_user(user_id)
    print(f"User {user['name']} updated? {success}!")     