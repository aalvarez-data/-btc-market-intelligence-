import pandas as pd
df = pd.read_csv(r'C:\Bitcoin project\btc-market-intelligence\btc-market-intelligence\data\raw\btc_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['target'] = (df['Price'].shift(-1) > df['Price']).astype(int)
print(df[['Date', 'Price', 'target']].tail(20))
df['SMA_50'] = df['Price'].rolling(window=50).mean()
df['SMA_200'] = df['Price'].rolling(window=200).mean()
df['SMA_20'] = df['Price'].rolling(window=20).mean()
df['BB_Upper'] = df['SMA_20'] + 2 * df['Price'].rolling(window=20).std()
df['BB_Lower'] = df['SMA_20'] - 2 * df['Price'].rolling(window=20).std()
def calculate_rsi(df, column='Price', period = 14):
    delta = df[column].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
df['RSI_14'] = calculate_rsi(df)
print(df[['Date', 'Price', 'RSI_14']].tail(20))

df = df.dropna()
print(f"Rows after dropna: {len(df)}")

features = ['RSI_14', 'SMA_50', 'SMA_200', 'BB_Upper', 'BB_Lower']
X = df[features]
y = df['target']

split = int(len(df) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

print(f"Train: {len(X_train)} rows, Test: {len(X_test)} rows")

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2%}")
print(classification_report(y_test, y_pred))