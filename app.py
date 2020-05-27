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



def get_time():
	from datetime import datetime 
	now_time = datetime.now().strftime('%Y-%m-%d %H:%M')
	return now_time
	
message = TextSendMessage( get_time())
line_bot_api.push_message(userID, message)


	
if __name__ == '__main__':
    app.run(debug=True)