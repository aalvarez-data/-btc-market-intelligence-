import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
df = pd.read_csv(r'C:\Bitcoin project\btc-market-intelligence\btc-market-intelligence\data\raw\btc_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['SMA_50'] = df['Price'].rolling(window=50).mean()
df['SMA_200'] = df['Price'].rolling(window=200).mean()
#se crean dos nuevas columnas en el dataframe, una para la media movil de 50 dias y otra para la media movil de 200 dias
# usando la funcion rolling() de pandas para calcular la media movil con una ventana de 50 y 200 respectivamente.
#la media movil o SMA es un indicador que promedia el precio de los ultimos 50 o 200 dias para ver tendencias reales.
print(df[["Date", 'Price', 'SMA_50', 'SMA_200']].tail(20))

def calculate_rsi(df, column='Price', period = 14):
    # Calcular diferencias de precios, perdidas y ganancias
    delta = df[column].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    #Usar SMA  para iniciar
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    #usar el metodo de suavizado de Wilder para calcular el RSI
    avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()

    #calcular fuerza relativa
    rs = avg_gain / avg_loss

    #calcular RSI
    rsi = 100 - (100 / (1 + rs))
    return rsi
df['RSI_14'] = calculate_rsi(df)
print(df[['Date', 'Price', 'RSI_14']].tail(20))

#Bandas de Bollinger, es un metodo de analisis que utiliza la media movil y dos bandas, superior e inferior usando desviacion 
#estandar, se usa para medir volatilidad de mercado y posibles puntos de entrada o salida
df['SMA_20'] = df["Price"].rolling(window=20).mean()
df['BB_Upper'] = df['SMA_20'] + 2 * df['Price'].rolling(window=20).std()
df['BB_Lower'] = df['SMA_20'] - 2 * df['Price'].rolling(window=20).std()         
print(df[['Date', 'Price', 'SMA_20', 'BB_Upper', 'BB_Lower']].tail(20))

plt.plot(df['Date'], df['Price'], label = 'Price')
plt.plot(df['Date'], df['SMA_50'], label = 'SMA 50')
plt.plot(df['Date'], df['SMA_200'], label = 'SMA 200')
plt.plot(df['Date'], df['BB_Upper'], label = 'Upper Band')
plt.plot(df['Date'], df['BB_Lower'], label = 'Lower Band')
plt.legend()
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(r'C:\Bitcoin project\btc-market-intelligence\btc-market-intelligence\data\processed\technical_indicators.png')