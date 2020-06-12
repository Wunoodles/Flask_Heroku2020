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

from bs4 import BeautifulSoup
import requests
def movie(num):
    target_url = 'http://www.atmovies.com.tw/movie/next/0/'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = []
    for index, data in enumerate(soup.select('ul.filmListAll a')):
        if index == int(num):
            break
        title = data.text.replace('\t', '').replace('\r', '')
        link = "http://www.atmovies.com.tw" + data['href']
        content += [[title, link]]
    return content


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    if event.message.text == '傳送位置':
        message = LocationSendMessage(
            title='消息地點',
            address='花蓮縣玉里鎮國武里中山路２段５８號',
            latitude=23.333096,
            longitude=121.315149,
        )
        
    elif event.message.text.startswith('電影-'):
        _, num = event.message.text.split('-')
        print(num)
        movie_info = movie(num)
        print(movie_info)
        columns_info = []
        for m in movie_info:
            columns_info += [
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/gallery/PddQoYt',
                    title=m[0],
                    text=m[0],
                    actions=[
                        URITemplateAction(
                            label='前往觀看',
                            uri=m[1]
                        )
                    ]
                )
            ]
        Carousel_template = TemplateSendMessage(
            alt_text='新聞文章',
            template=CarouselTemplate(columns= columns_info)
        )

    else:
        message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

if __name__ == '__main__':
    app.run(debug=True)