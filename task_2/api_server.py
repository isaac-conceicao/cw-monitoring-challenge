from flask import Flask, request, jsonify
import sqlite3
import pandas as pd
import datetime

app = Flask(__name__)

@app.route('/status_report', methods=['GET'])
def get_status_report():
    conn = sqlite3.connect('transactions.db')
    current_minute = datetime.now().strftime('%H:%M')

    report = pd.read_sql(f"SELECT * FROM status_reports WHERE time = '{current_minute}'", conn).to_dict(orient='records')
    conn.close()

    return jsonify(report)

@app.route('/transaction', methods=['POST'])
def receive_transaction():
    transaction = request.json
    # Process the transaction...
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(port=5000)
