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

# User ID
userID = 'U5da47e52a532692416abefc9655ca12c'

def get_time():
	from datetime import datetime 
	now_time = datetime.now().strftime('%Y-%m-%d %H:%M')
	return now_time
	
message = TextSendMessage( get_time())
line_bot_api.push_message(userID, message)


	
if __name__ == '__main__':
    app.run(debug=True)