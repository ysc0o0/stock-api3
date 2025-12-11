from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Stock API is running!"})

@app.route("/stock")
def get_stock():
    symbols = request.args.get("symbols")

    if not symbols:
        return jsonify({"error": "Missing ?symbols= parameter"}), 400

    symbols_list = symbols.split(",")
    result = {}

    for symbol in symbols_list:
        ticker = yf.Ticker(symbol)
        info = ticker.history(period="1d")

        if info.empty:
            result[symbol] = {"error": "Invalid symbol or no data"}
        else:
            last_quote = info.iloc[-1]
            result[symbol] = {
                "close": float(last_quote["Close"]),
                "open": float(last_quote["Open"]),
                "high": float(last_quote["High"]),
                "low": float(last_quote["Low"]),
                "volume": float(last_quote["Volume"]),
            }

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
