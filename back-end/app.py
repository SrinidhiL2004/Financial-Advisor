from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "Welcome to the Stock Recommendation API!"

@app.route('/stock/<ticker>', methods=['GET'])
def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        live_price = data['Close'].iloc[-1]
        return jsonify({
            'ticker': ticker,
            'live_price': live_price
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_stock_recommendations(risk_profile):
    # Example stocks categorized by risk profile
    stocks_by_risk = {
        'Risk Averse': ['TCS.NS', 'INFY.NS', 'HDFCBANK.NS'],  # Large-cap, stable stocks
        'Conservative': ['RELIANCE.NS', 'ICICIBANK.NS', 'BAJAJFINSV.NS'],  # Stable, dividend-paying stocks
        'Balanced': ['HDFCLIFE.NS', 'BHARTIARTL.NS', 'ASIANPAINT.NS'],  # Balanced stocks with growth potential
        'Growth': ['DMART.NS', 'TATAMOTORS.NS', 'ADANIPORTS.NS'],  # Growth-oriented stocks
        'High Growth': ['ADANIGREEN.NS', 'BAJAJELEC.NS', 'IRCTC.NS'],  # High-risk, high-reward stocks
    }
    
    selected_stocks = stocks_by_risk.get(risk_profile, [])
    
    # Fetch live data for the selected stocks
    stock_data = []
    for symbol in selected_stocks:
        stock_info = yf.Ticker(symbol).info
        stock_data.append({
    'symbol': symbol,
    'name': stock_info.get('longName', ''),
    'price': stock_info.get('regularMarketPrice') or stock_info.get('previousClose', 0)
})

    
    return stock_data

@app.route('/recommend_stocks', methods=['GET'])
def recommend_stocks():
    risk_profile = request.args.get('riskProfile')
    # Fetch stock data based on the risk profile
    stocks = get_stock_recommendations(risk_profile)
    return jsonify(stocks)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
