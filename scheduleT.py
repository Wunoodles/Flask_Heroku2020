# -*- coding: utf-8 -*-
from flask import Flask, request, abort
import schedule
import time

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

userID = 'U5da47e52a532692416abefc9655ca12c'

def get_time():
	from datetime import datetime 
	now_time = datetime.now().strftime('%Y-%m-%d %H:%M')
	message = TextSendMessage( now_time )
	line_bot_api.push_message(userID, message)

second_5_j = schedule.every(10).seconds.do(get_time)


# 無窮迴圈
while True: 
    schedule.run_pending()
    time.sleep(1)


#