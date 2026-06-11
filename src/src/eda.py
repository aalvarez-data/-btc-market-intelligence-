import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
#Se importan pandas para manipular los datos y matplotlib para graficar los datos y hacer visualizaciones de los mismos

df = pd.read_csv(r'C:\Bitcoin project\btc-market-intelligence\btc-market-intelligence\data\raw\btc_data.csv')
#se lee el archivo CSV que hicimos anteriormente para poder continuar a graficar y hacer EDA

df['Date'] = pd.to_datetime(df['Date'])
df['daily_return'] = df['Price'].pct_change()
#se convierte la columna de fecha a formato datetime para poder manipularla mejor.
#se crea una nueva columna llamada daily_return que calcula el cambio porcentual diario del precio de Bitcoin utilizando la función pct_change() de pandas.

print(df.head(5))
print(df.info())
print(df.describe())
#se imprimen las primeras 5 filas del dataframe para tener una idea de cómo se ven los datos, se imprime la información del dataframe para ver el tipo de datos y si hay valores nulos, y se imprime la descripción estadística del dataframe para ver medidas como la media, mediana, desviación estándar, etc.

plt.hist(df['daily_return'], bins=20)
plt.xlabel ('Daily Return')
plt.ylabel ('Frequency')
plt.title ('Distribution of Daily Returns')
# se crea un histograma de la distribucion de los retornos diarios usando matplotlib, daily return en el eje x
#la frecuencia en el eje y, se le da un titulo a la grafica y se etiquetan los ejes
plt.savefig(r'C:\Bitcoin project\btc-market-intelligence\btc-market-intelligence\data\processed\daily_returns_distribution.png')
plt.clf()
#estos dos comandos de arriba guardan la grafica en otra carpeta y luego limpia la figura para poder hacer otra grafica sin que intefiera.

plt.plot(df['Date'], df['Price'])
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Bitcoin Price Over Time')
#se crea una grafica de linea para mostrar la evolucion del precio de Bitcoin a lo largo del tiempo, con la fecha en el eje x y el precio en el eje y, se le da un titulo a la grafica y se etiquetan los ejes
plt.savefig(r'C:\Bitcoin project\btc-market-intelligence\btc-market-intelligence\data\processed\price_over_time.png')
plt.clf()

plt.plot(df['Date'], df['Total_Volume'] / 1e9)
plt.xlabel('Date')
plt.ylabel('Volume (Billions USD)')
plt.title('Bitcoin Daily Volume Over Time')
#se crea una grafica de barras para mostrar la evolucion del volumen total de Bitcoin a lo largo del tiempo, con la fecha en el eje x y el volumen total en el eje y, se le da un titulo a la grafica y se etiquetan los ejes
plt.savefig(r'C:\Bitcoin project\btc-market-intelligence\btc-market-intelligence\data\processed\total_volume_over_time.png')
plt.clf()
# Q-Q Plot
stats.probplot(df['daily_return'], dist="norm", plot=plt)
plt.title('BTC Daily Returns Q-Q Plot')
plt.xlabel("Theoretical Quantiles")
plt.ylabel("Sample Quantiles")
plt.savefig(r'C:\Bitcoin project\btc-market-intelligence\btc-market-intelligence\data\processed\qq_plot.png')
plt.clf()
#se hace un qqplot para ver si los retornos diarios siguen una distribucion normal
plt.plot(df['Date'], df['daily_return'])
plt.xlabel('Date')
plt.ylabel('Daily Return')
plt.title('BTC Daily Returns Over Time')
plt.savefig(r'C:\Bitcoin project\btc-market-intelligence\btc-market-intelligence\data\processed\daily_returns_over_time.png')
plt.clf()
#se comprueba homoseasticidad graficando los retornos diarios a lo largo del tiempo, si los retornos diarios muestran una variabilidad constante a lo largo del tiempo, entonces se puede decir que son homocedasticos, si muestran una variabilidad creciente o decreciente, entonces se puede decir que son heterocedasticos.
correlation = df[['Price', 'Market_Cap', 'Total_Volume', 'daily_return']].corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.savefig(r'C:\Bitcoin project\btc-market-intelligence\btc-market-intelligence\data\processed\correlation_heatmap.png')
plt.clf()
#se calcula la matriz de correlacion entre las columnas de precio, capitalizacion de mercado, volumen total y retorno diario, se crea un mapa de calor usando seaborn para visualizar estas correlaciones, se le da un titulo a la grafica y se guarda en la carpeta de processed.

print(df[['Date', 'Price']].head(10))
print(df[['Date', 'Price']].tail(10))
print(df[df['Price'] == df['Price'].min()])
print(df[df['Price'] == df['Price'].max()])
print(df[df['daily_return'] == df['daily_return'].min()])
print(df[df['daily_return'] == df['daily_return'].max()])