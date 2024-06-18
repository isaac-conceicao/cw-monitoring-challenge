def isValid(card_number):
    return len(card_number) == 16 and int(card_number[-1]) % 2 == 0

def determine_status(transaction, issuer_score, pos_score):
    if not isValid(transaction['card_number']):
        return 'failed'
    elif issuer_score > 10:
        return 'denied'
    elif 10 < pos_score < 15:
        return 'reversed'
    elif pos_score > 15:
        return 'refunded'
    return 'approved'
