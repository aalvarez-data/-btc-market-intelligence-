import requests
import pandas as pd
import sqlite3 
#Se importan requests para poder solicitar la API de coingecko, que es una plataforma web para podr analizar precios de btc
#Pandas para transformar datos a CSV y limpiar datos
#sqlite 3 para poder pasar esos datos a SQL y hacer bases de datos para manipular los datos

Link = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=365&interval=daily"
Gecko = requests.get(Link).json()
# se define una variable llamada Link para resumir la URL de coingecko y se define otra variable llamada Gecko para poder solicitar la API y guardar los datos en formato JSON, que es un formato de datos que se puede manipular fácilmente con Python.

Prices = Gecko['prices']
Market_caps = Gecko['market_caps']
Total_volumes = Gecko['total_volumes']
price = pd.DataFrame(Prices, columns=['Date', 'Price'])
mc = pd.DataFrame(Market_caps, columns=['Date', 'Market_Cap'])
mc['Date'] = pd.to_datetime(mc['Date'], unit='ms')
#Aqui se usa el to_datetime porque coingecko entrega el tiempo en milisegundos (UNIX) y lo ocupamos en fecha legible
tv = pd.DataFrame(Total_volumes, columns=['Date', 'Total_Volume'])
tv['Date'] = pd.to_datetime(tv['Date'], unit='ms')
price['Date'] = pd.to_datetime(price['Date'], unit='ms')
df = price.merge(mc, on='Date').merge(tv, on='Date')
#se usa merge para unir los 3 dataframes en uno solo donde sean unidos por la fecha
# se definen variables para extaer datos como los volumenes totales( cantidad total de Bitcoins que se han comprado y vendido en un mercado o exchange durante un período de tiempo determinado.)
# Otra para extaer el precio y otra para extaer la capitalización de mercado (valor total de todas las monedas en circulación multiplicado por el precio actual de la moneda, es el valor total teorico de todas las monedas que existen al precio actual.)

df.to_csv(r'C:\Bitcoin project\btc-market-intelligence\btc-market-intelligence\data\raw\btc_data.csv', index=False)
conn = sqlite3.connect("btc_data.db")
df.to_sql(name = "btc_data", con = conn, if_exists = "replace", index=False)
conn.close()
# se guardan todos estos datos como un solo dataframe, se exporta a archivo CSV y se guarda en una base de datos SQL