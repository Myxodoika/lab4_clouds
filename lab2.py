import requests
import json
import matplotlib.pyplot as plt
import boto3
import pandas as pd

url_usd = "https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode=usd&sort=exchangedate&order=desc&json"
url_eur = "https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode=eur&sort=exchangedate&order=desc&json"
response_usd = requests.get(url_usd)
response_eur = requests.get(url_eur)

data_usd = response_usd.json()
with open('exchange_rates_usd.json', 'w') as f:
	json.dump(data_usd, f, indent=1)

data_eur = response_eur.json()
with open('exchange_rates_eur.json', 'w') as f:
	json.dump(data_eur, f, indent=1)

with open('exchange_rates_usd.json', 'r') as f:
	data_usd = json.load(f)

df = pd.DataFrame(data_usd)

df.to_csv('exchange_rates_usd.csv')

with open('exchange_rates_eur.json', 'r') as f:
	data_eur = json.load(f)

df = pd.DataFrame(data_eur)

df.to_csv('exchange_rates_eur.csv')

s3 = boto3.client('s3')

bucket_name = 'lab4-2'
file_name = 'exchange_rates_usd.csv'
file_name1 = 'exchange_rates_eur.csv'

s3.upload_file(file_name, bucket_name, file_name)
s3.upload_file(file_name1, bucket_name, file_name1)

obj = s3.get_object(Bucket='lab4-2', Key='exchange_rates_eur.csv')
df_eur = pd.read_csv(obj['Body'])
obj = s3.get_object(Bucket='lab4-2', Key='exchange_rates_usd.csv')
df_usd = pd.read_csv(obj['Body'])

df_eur = df_eur.iloc[::5, :]
df_usd = df_usd.iloc[::5, :]

plt.figure(figsize=(18, 10))
plt.plot(df_eur['exchangedate'], df_eur['rate'], label='EUR')
plt.plot(df_usd['exchangedate'], df_usd['rate'], label='USD')
plt.xlabel('Дата')
plt.ylabel('Курс')
plt.title('Курс валют')
plt.legend()
plt.xticks(rotation=90)

plt.savefig('exchange_rate_graph.png')

with open('exchange_rate_graph.png', 'rb') as f:
	s3.upload_fileobj(f, 'lab4-2', 'exchange_rate_graph.png')
    
plt.show()
