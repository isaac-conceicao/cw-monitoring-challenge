import pandas as pd

# Define the data for issuers.csv
issuers_data = {
    'issuer_id': ['issuer1', 'issuer2'],
    'issuer_name': ['Issuer One', 'Issuer Two'],
    'score': [5, 15]  # One score < 10 and one score > 10
}

# Define the data for pos.csv
pos_data = {
    'pos_id': ['pos1', 'pos2', 'pos3'],
    'pos_name': ['POS One', 'POS Two', 'POS Three'],
    'score': [5, 12, 16]  # One score < 10, one 10 < score < 15, and one score > 15
}

# Define the data for transactions.csv according to Example 1
num_approved = 348
num_refunded = 3
num_reversed = 1
num_denied = 27

transaction_id = [f'trans_{i}' for i in range(1, num_approved + num_refunded + num_reversed + num_denied + 1)]
time = ['10:01'] * (num_approved + num_refunded + num_reversed + num_denied)
issuer_id = ['issuer1'] * num_approved + ['issuer1'] * num_refunded + ['issuer1'] * num_reversed + ['issuer2'] * num_denied
pos_id = ['pos1'] * num_approved + ['pos3'] * num_refunded + ['pos2'] * num_reversed + ['pos1'] * num_denied
card_number = ['1234567890123456'] * (num_approved + num_refunded + num_reversed + num_denied)

transactions_data = {
    'transaction_id': transaction_id,
    'time': time,
    'issuer_id': issuer_id,
    'pos_id': pos_id,
    'card_number': card_number
}

# Create dataframes
issuers_df = pd.DataFrame(issuers_data)
pos_df = pd.DataFrame(pos_data)
transactions_df = pd.DataFrame(transactions_data)

# Save the dataframes to CSV files
issuers_df.to_csv('issuers.csv', index=False)
pos_df.to_csv('pos.csv', index=False)
transactions_df.to_csv('transactions.csv', index=False)

