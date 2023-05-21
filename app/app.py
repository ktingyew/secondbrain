import base64
import json
import os

import requests

from query import send_query

ALLOWED_TELE_USER = os.getenv('ALLOWED_TELE_USER')
TELE_TOKEN = os.getenv('TELE_TOKEN')
URL = f"https://api.telegram.org/bot{TELE_TOKEN}/"
# print(f"{ALLOWED_TELE_USER=}")

# def send_message(text, chat_id):
#     url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
#     requests.get(url)


def telegram_bot_send_long_msg(message, chat_id, msg_id, chunk_len=1000):
    chunks = [message[i:i + chunk_len] for i in range(0, len(message), chunk_len)]
    for chunk in chunks:
        telegram_bot_sendtext(chunk, chat_id, msg_id)


def telegram_bot_sendtext(bot_message, chat_id, msg_id):
    data = {
        'chat_id': chat_id,
        'text': bot_message,
        'reply_to_message_id': msg_id
    }
    requests.post(
        'https://api.telegram.org/bot' + TELE_TOKEN + '/sendMessage',
        json=data
    )


def lambda_handler(event, context):
    print(f"{event=}")
    body = json.loads(event["body"])
    # print(f"{body=}")

    sender_id = str(body["message"]["from"]["id"])
    # print(f"{sender_id=}")
    # print(f"{type(sender_id)=}")

    if sender_id != ALLOWED_TELE_USER:
        return {
            "statusCode": 200
        }

    # print("Message from permitted user.")
    chat_id = body['message']['chat']['id']
    msg_id = str(int(body['message']['message_id']))
    text = body['message']['text']

    llm_response = str(send_query(text))

    # print(f"{type(llm_response)=}")

    telegram_bot_send_long_msg(llm_response, chat_id, msg_id)
    return {
        # "reply": reply,
        "statusCode": 200
    }

