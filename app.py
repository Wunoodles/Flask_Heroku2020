# -*- coding: utf-8 -*-
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel access token (long-lived)
line_bot_api = LineBotApi('73dYdWd9LTZ+z/nMDvbZVHIeHJKkhTQW8oFK1mUaHw8pgOclBx3EpbgM9vG9sQ4kkfUvLC53N3xZlfcmWobSOXCBVjnqsSyb+2OjzupXnwkQTpGTIbbx61k89TDnlY7Xf7o6H7+0kxmW9UNko6iXPAdB04t89/1O/w1cDnyilFU=')
# Channel secret 
handler = WebhookHandler('0e4384641b9c12109bcf4ebcb0e146b0')

@app.route('/')
def hello_world():
    return 'Hello, World! '


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

import requests
import json
def get_mask_info(name):
    r = requests.get('https://raw.githubusercontent.com/kiang/pharmacies/master/json/points.json')
    response = r.text

    person_dict = json.loads(response)
    for info in person_dict['features']:
        store_name = info['properties']['name']
        address = info['properties']['address']
        audlt = info['properties']['mask_adult']
        mask_child = info['properties']['mask_child']

        geo = info['geometry']['coordinates']

        if store_name == name:
            return [address, audlt, mask_child, geo]

    return ['查無此店']

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
        
    elif event.message.text == '傳送位置':
        message = LocationSendMessage(
            title='消息地點',
            address='花蓮縣玉里鎮國武里中山路２段５８號',
            latitude=23.333096,
            longitude=121.315149,
        )

    elif event.message.text.startswith('口罩查詢-'):
        text = event.message.text
        _, name = text.split('-')
        result = get_mask_info(name)

        if len(result) == 1:
            message = TextSendMessage(result[0])
        else:
            title = "{},大人:{},小孩:{}".format(name, result[1], result[2])
            message = LocationSendMessage(
                title=name,
                address=result[0],
                latitude=float(result[3][1]),
                longitude=float(result[3][0])
            )
    else:
        message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

if __name__ == '__main__':
    app.run(debug=True)