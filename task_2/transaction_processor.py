import sqlite3
from datetime import datetime
import auth_engine
import pandas as pd

def process_transactions():
    conn = sqlite3.connect('transactions.db')
    current_minute = '10:01'#datetime.now().strftime('%H:%M')

    
    transactions = pd.read_sql(f"SELECT * FROM transactions WHERE time = '{current_minute}'", conn)
    issuers = pd.read_sql("SELECT * FROM issuers", conn)
    pos = pd.read_sql("SELECT * FROM pos", conn)

    for index, transaction in transactions.iterrows():
        issuer_score = issuers.loc[issuers['issuer_id'] == transaction['issuer_id'], 'score'].values[0]
        pos_score = pos.loc[pos['pos_id'] == transaction['pos_id'], 'score'].values[0]
        status = auth_engine.determine_status(transaction, issuer_score, pos_score)

        conn.execute(f"UPDATE transactions SET status = '{status}' WHERE transaction_id = '{transaction['transaction_id']}'")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    process_transactions()