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
        if len(title) == 0:
            num += 1
            continue
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
    elif event.message.text == '範例':
        tmp = [CarouselColumn(
                        thumbnail_image_url='https://example.com/item1.jpg',
                        title='this is menu1',
                        text='description1',
                        actions=[
                            PostbackTemplateAction(
                                label='postback1',
                                text='postback text1',
                                data='action=buy&itemid=1'
                            ),
                            MessageTemplateAction(
                                label='message1',
                                text='message text1'
                            ),
                            URITemplateAction(
                                label='uri1',
                                uri='http://example.com/1'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://example.com/item2.jpg',
                        title='this is menu2',
                        text='description2',
                        actions=[
                            PostbackTemplateAction(
                                label='postback2',
                                text='postback text2',
                                data='action=buy&itemid=2'
                            ),
                            MessageTemplateAction(
                                label='message2',
                                text='message text2'
                            ),
                            URITemplateAction(
                                label='uri2',
                                uri='http://example.com/2'
                            )
                        ]
                    )]
        print(tmp)
        message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=tmp
            )
        )

    elif event.message.text.startswith('電影-'):
        _, num = event.message.text.split('-')
        print(num)
        movie_info = movie(num)
        print(movie_info)
        columns_info = []
        for m in movie_info:
            colum = CarouselColumn(
                    thumbnail_image_url='https://example.com/item1.jpg',
                    title=m[0],
                    text=m[0],
                    actions=[
                        URITemplateAction(
                            label='前往觀看',
                            uri=m[1]
                        )
                    ]
                )
            columns_info += [colum]
        print(columns_info)        
        message = TemplateSendMessage(
            alt_text='新聞文章',
            template=CarouselTemplate(columns= columns_info)
        )

    else:
        message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

if __name__ == '__main__':
    app.run(debug=True)