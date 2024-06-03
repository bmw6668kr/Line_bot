# -*- coding: utf-8 -*-

import requests
import json
from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction
import os
import random

load_dotenv('.env')
app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower()
    if '排球' in user_message:
        replies = [
            "排球是一項非常有趣且富有挑戰性的運動！",
            "排球比賽分為室內排球和沙灘排球兩種形式。",
            "排球運動要求球員具備高度的協調能力和團隊合作精神。"
        ]
        reply = random.choice(replies)
    elif '規則' in user_message:
        replies = [
            "排球的基本規則包括：每隊最多有六名球員，球不可以觸地，每次最多三次擊球。",
            "在排球比賽中，球員不可以連續兩次擊球。",
            "每局比賽先得25分且至少領先2分的一隊勝出。"
        ]
        reply = random.choice(replies)
    elif '選單' in user_message:
        reply = TemplateSendMessage(
            alt_text='選單模板',
            template=ButtonsTemplate(
                title='排球資訊選單',
                text='請選擇以下選項',
                actions=[
                    MessageAction(label='排球規則', text='規則'),
                    MessageAction(label='排球簡介', text='排球'),
                    MessageAction(label='比賽結果', text='比賽'),
                    MessageAction(label='最新動態', text='動態')
                ]
            )
        )
    elif '動態' in user_message:
        replies = [
            "排球界最近有很多新動態，歡迎關注相關新聞。",
            "排球明星最近的表現非常出色，值得期待！",
            "排球比賽季即將來臨，各隊伍正在積極備戰。"
        ]
        reply = random.choice(replies)
    else:
        replies = [
            "對不起，我不太明白你的意思。請問你想知道關於排球的哪些訊息呢？",
            "可以告訴我更多細節嗎？我會盡力解答。",
            "請問有什麼具體的排球相關問題嗎？"
        ]
        reply = random.choice(replies)
    
    if isinstance(reply, str):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
    else:
        line_bot_api.reply_message(event.reply_token, reply)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=13313)
