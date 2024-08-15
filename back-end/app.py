from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
import yfinance as yf
import os
import logging

# Initialize Flask application
app = Flask(__name__, template_folder='../public', static_folder='../public')
CORS(app, resources={r"/recommend_stocks/*": {"origins": "*"}})

# Set up logging
logging.basicConfig(level=logging.DEBUG)

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
        app.logger.error(f"Error fetching stock data for {ticker}: {e}")
        return jsonify({'error': str(e)}), 500

def get_stock_recommendations(risk_profile):
    stocks_by_risk = {
        'Risk Averse': ['TCS.NS', 'INFY.NS', 'HDFCBANK.NS'],
        'Conservative': ['RELIANCE.NS', 'ICICIBANK.NS', 'BAJAJFINSV.NS'],
        'Balanced': ['HDFCLIFE.NS', 'BHARTIARTL.NS', 'ASIANPAINT.NS'],
        'Growth': ['DMART.NS', 'TATAMOTORS.NS', 'ADANIPORTS.NS'],
        'High Growth': ['ADANIGREEN.NS', 'BAJAJELEC.NS', 'IRCTC.NS'],
    }

    if risk_profile not in stocks_by_risk:
        app.logger.error(f"Invalid risk profile: {risk_profile}")
        return jsonify({'error': 'Invalid risk profile'}), 400

    selected_stocks = stocks_by_risk[risk_profile]
    
    stock_data = []
    for symbol in selected_stocks:
        try:
            stock_info = yf.Ticker(symbol).info
            stock_data.append({
                'symbol': symbol,
                'name': stock_info.get('longName', ''),
                'price': stock_info.get('regularMarketPrice') or stock_info.get('previousClose', 0)
            })
        except Exception as e:
            app.logger.error(f"Error fetching data for stock {symbol}: {e}")
    
    return stock_data

@app.route('/recommend_stocks', methods=['GET'])
def recommend_stocks():
    try:
        risk_profile = request.args.get('riskProfile')
        if not risk_profile:
            app.logger.error("Missing riskProfile parameter")
            return jsonify({'error': 'Missing riskProfile parameter'}), 400

        stocks = get_stock_recommendations(risk_profile)
        if isinstance(stocks, tuple):  # Check if the function returned a tuple (error response)
            return stocks
        return jsonify(stocks)
    except Exception as e:
        app.logger.error(f"Error in /recommend_stocks endpoint: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Serve static files like images
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(app.root_path, '../public'), filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
