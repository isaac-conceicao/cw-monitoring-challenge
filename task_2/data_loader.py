import pandas as pd
import sqlite3

def load_data():
    conn = sqlite3.connect('transactions.db')
    transactions = pd.read_csv('transactions.csv',dtype={'card_number': object})
    issuers = pd.read_csv('issuers.csv')
    pos = pd.read_csv('pos.csv')

    transactions.to_sql('transactions', conn, if_exists='replace', index=False)
    issuers.to_sql('issuers', conn, if_exists='replace', index=False)
    pos.to_sql('pos', conn, if_exists='replace', index=False)

    conn.close()

if __name__ == '__main__':
    load_data()
