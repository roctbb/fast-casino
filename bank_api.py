import requests
from config import trading_token

host = 'https://bank.goto.msk.ru'


def ask_money(from_id, amount, description):
    answer = requests.post(host + '/api/ask', json={
        'token': trading_token,
        'account_id': from_id,
        'amount': amount,
        'description': description
    })

    return answer.json()


def verify_transaction(transaction_id, code):
    answer = requests.post(host + '/api/verify', json={
        "transaction_id": transaction_id,
        "code": code
    })

    return answer.json()
