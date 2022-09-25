# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created Date: 2022/08/12
# Author: Wei-Lun Lin
# Version: 1.0
# Email: weilun9539ny@gmail.com
# Status: Product

# Import libraries
import os
from flask import Flask, request, abort
from linebot import (
    LineBotApi,
    WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)

from crawler import Crawler
import database
# Finish importing libraries

# Initialization
app = Flask(__name__)

line_bot_api = LineBotApi('quud2/CCW6i43uHAomVe8bMzRjHXbH5i/uqv82BmH6KqEa1BtTn1DU+U1yEnS6W90Sd1y+OW9QSsEmxNU83vl1RQcnj/7c4Qe2B8kSoz4sbzlbNTb1db9ygfHr3nobUlBu9ZWNj5bQFn+wPQ2dc7tgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('27893c48e684e0563636ed0a27674e51')
# Finish initializing


# Define functions
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
        invalid_message = "Invalid signature. Please check your "
        invalid_message += "channel access token/channel secret."
        print(invalid_message)
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    input_text = event.message.text

    if input_text == "謝謝":
        reply_text = "你很有禮毛餒"
    elif input_text == "阿彌陀佛狒狒":
        reply_text = input_text

    if "功能介紹" in input_text:
        reply_text = "目前有的功能只有「NTU mail carrier」，\n其他功能還沒想法 or 懶得做www"
        reply_text += "\n------\n可以直接輸入該功能，查看該功能的介紹。\n"
        reply_text += "也可以在功能後面加上「command」，查看該功能有哪些指令。"

    if "NTU mail carrier" in input_text:
        reply_text = mail_carrier_commands(event)

    line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_text))


def mail_carrier_commands(event):
    input_text = event.message.text
    user_id = event.source.user_id

    if input_text == "NTU mail carrier":
        reply_text = "本功能會每十分鐘檢查一次您的 NTU 信箱有沒有新的信，\n有的話會用訊息提醒！\n\n"
        reply_text += "只是本功能需要輸入您的記中帳密，\n並且會將該帳密和最新一封信件的編號儲存在線上資料庫。\n"
        reply_text += "使用過程中取得的所有資訊均僅會使用於本程序，絕不會使用在其他地方。\n如有資安上的疑慮，請勿使用本功能。"
        reply_text += "\n\n若同意以上說明，可以承擔風險，且欲開啟本功能，\n"
        reply_text += "請按照以下步驟開啟此功能：\n\n1. 確認目前收件匣中至少有一封信。\n2. 按照以下格式輸入記中帳密："
        reply_text += "「NTU mail carrier new account b092070XX XXXXXXXXX」。"
    elif "command" in input_text:
        reply_text = "目前可用的指令有：\n1. NTU mail carrier command：查詢本功能的所有指令\n\n"
        reply_text += "2. NTU mail carrier new account '學號' '密碼'：加入新的記中帳號\n\n"
        reply_text += "3. NTU mail carrier update password '學號' '密碼'：更新密碼\n\n"
        reply_text += "4. NTU mail carrier delete account '學號'：把該記中帳密從資料庫中移除"
    elif "new account" in input_text:
        try:
            new_account(user_id, input_text)
            reply_text = "已成功開啟此功能，並且完成資料上傳，將開始自動檢查新信件!!!\n"
            reply_text += "如果要查詢其他指令，\n請輸入「NTU mail carrier command」~"
        except Exception:
            reply_text = "失敗了qq\n檢查看看帳密有打錯嗎?"
    elif "update password" in input_text:
        try:
            [account, password] = input_text.split(' ')[-2:]
            database.update_user_info(
                user_id,
                account=account,
                password=password
            )
            reply_text = f"已更新{account}的密碼~"
        except Exception:
            reply_text = "失敗了qq\n"
    elif "delete account" in input_text:
        try:
            account = input_text.split(" ")[-1]
            database.delete_data(user_id, account)
            reply_text = f"已刪除{account}的學號，\n以及資料庫中所有和該學號有關的資料。\n感謝您的使用~"
        except Exception:
            reply_text = "失敗了qq\n可能是資料庫中已經沒有該學號的資料，\n有其他問題請聯絡渭毛本人~"
    else:
        reply_text = "請確認輸入指令是否正確，或是聯絡渭毛本人w"
    return reply_text


def new_account(user_id, input_text):
    # Collect user information
    [account, password] = input_text.split(" ")[-2:]
    crawler = Crawler(account, password)
    last_uid = crawler.get_last_mail_id()
    # Finish collecting user information

    # Insert the user data to the database
    user_data = [user_id, account, password, last_uid]
    database.insert_user_data(user_data)
    # Finish inserting user data
# Finish defining functions


# Run the program
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
# Finish running the program
