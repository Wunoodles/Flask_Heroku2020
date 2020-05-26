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

def getNews():
	"""
	建立一個抓最新消息的function
	"""
	import requests
	import re
	from bs4 import BeautifulSoup

	url = 'https://www.ettoday.net/news/focus/3C%E5%AE%B6%E9%9B%BB/'
	r = requests.get(url)
	reponse = r.text

	url_list = re.findall(r'<h3><a href="/news/[\d]*/[\d]*.htm" .*>.*</a>',reponse)

	soup = BeautifulSoup(url_list[0])
	url = 'https://fashion.ettoday.net/' + soup.find('a')['href']
	title = soup.text


	tmp = title + ': ' +url
	return tmp
	
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 傳送文字
    if event.message.text == '傳送文字':
        message = TextSendMessage(getNews())

    # 傳送圖片
    elif event.message.text == '傳送圖片':
        message = ImageSendMessage(
            original_content_url='https://i.imgur.com/QPJ8A1b.png',
            preview_image_url='https://i.imgur.com/QPJ8A1b.png'
        )

    # 傳送影片
    elif event.message.text == '傳送影片':
        message = VideoSendMessage(
            original_content_url='https://i.imgur.com/hOKAE06.mp4',
            preview_image_url='https://i.imgur.com/hOKAE06.mp4'
        )

    # 傳送貼圖
    elif event.message.text == '傳送貼圖':
        message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )


    # 傳送多重圖片訊息
    elif event.message.text == '多項傳送':
        message = TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/N3oQXjW.png',
                        action=PostbackTemplateAction(
                            label='postback1',
                            text='postback text1',
                            data='action=buy&itemid=1'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/OBdCHB9.png',
                        action=PostbackTemplateAction(
                            label='postback2',
                            text='postback text2',
                            data='action=buy&itemid=2'
                        )
                    )
                ]
            )
        )
    # 傳送位置
    elif event.message.text == '傳送位置':
        message = LocationSendMessage(
            title='消息地點',
            address='桃園',
            latitude=24.984210,
            longitude=121.293203
        )

    # 傳送按鈕介面訊息
    elif event.message.text == '快速選單':
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/vkqbLnz.png',
                title='Menu',
                text='Please select',
                actions=[
                    MessageTemplateAction(
                        label='發生地點',
                        text='傳送位置'
                    ),
                    MessageTemplateAction(
                        label='看新聞',
                        text='傳送文字'
                    ),
                    URITemplateAction(
                        label='URL',
                        uri='https://tw.appledaily.com/local/realtime/20180817/1412804'
                    )
                ]
            )
        )

    # 傳送組圖訊息
    elif event.message.text == '我要看報紙':
        message = ImagemapSendMessage(
            base_url='https://i.imgur.com/mLZTo24',
            alt_text='Imagemap',
            base_size=BaseSize(height=1040, width=1040),
            actions=[
                URIImagemapAction(
                    link_uri='https://tw.appledaily.com/',
                    area=ImagemapArea(
                        x=0, y=0, width=520, height=1040
                    )
                ),
                MessageImagemapAction(
                    text='您需要付費喔！',
                    area=ImagemapArea(
                        x=520, y=0, width=520, height=1040
                    )
                )
            ]
        )
    # 傳送確認介面訊息
    elif event.message.text == '我想要評分':
        message = TemplateSendMessage(
            alt_text='你覺得這個機器人方便嗎？',
            template=ConfirmTemplate(
                text='你覺得這個機器人方便嗎？',
                actions=[
                    MessageTemplateAction(
                        label='很棒！',
                        text='ＧＯＯＤ'
                    ),
                    MessageTemplateAction(
                        label='有待加強',
                        text='ＢＡＤ'
                    )
                ]
            )
        )

    # 傳送多重按鈕介面訊息
    elif event.message.text == '所有功能':
        message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/vkqbLnz.png',
                        title='新聞預警',
                        text='新聞來源-蘋果新聞',
                        actions=[
                            MessageTemplateAction(
                                label='發生地點',
                                text='傳送位置'
                            ),
                            MessageTemplateAction(
                                label='看新聞',
                                text='傳送文字'
                            ),
							URITemplateAction(
								label='URL',
								uri='https://tw.appledaily.com/local/realtime/20180817/1412804'
							)
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/Dt97YFG.png',
                        title='其他功能',
                        text='這裡存放各種功能！',
                        actions=[
                            MessageTemplateAction(
                                label='為機器人評分',
                                text='我想要評分'
                            ),
                            MessageTemplateAction(
                                label='更多新聞',
                                text='傳送文字'
                            ),
                            MessageTemplateAction(
                                label='放鬆一下',
                                text='傳送貼圖'
                            )
                        ]
                    )
                ]
            )
        )
    else:
        message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

	
if __name__ == '__main__':
    app.run(debug=True)