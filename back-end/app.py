from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
import yfinance as yf
import os

app = Flask(__name__, template_folder='../public', static_folder='../public')
CORS(app)

@app.route('/')
def index():
    return render_template('home.html')

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
    stocks_by_risk = {
        'Risk Averse': ['TCS.NS', 'INFY.NS', 'HDFCBANK.NS'],
        'Conservative': ['RELIANCE.NS', 'ICICIBANK.NS', 'BAJAJFINSV.NS'],
        'Balanced': ['HDFCLIFE.NS', 'BHARTIARTL.NS', 'ASIANPAINT.NS'],
        'Growth': ['DMART.NS', 'TATAMOTORS.NS', 'ADANIPORTS.NS'],
        'High Growth': ['ADANIGREEN.NS', 'BAJAJELEC.NS', 'IRCTC.NS'],
    }
    
    selected_stocks = stocks_by_risk.get(risk_profile, [])
    
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
    stocks = get_stock_recommendations(risk_profile)
    return jsonify(stocks)

# Serve static files like images
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(app.root_path, '../public'), filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
