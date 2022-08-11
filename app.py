# Import libraries
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    QuickReply, QuickReplyButton,
    PostbackAction, PostbackEvent
)
import os
import psycopg2

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    input_text = event.message.text

    if input_text == "謝謝":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="你很有禮毛餒")
        )
    if "crawler" in input_text:
        reply_text = crawler_commands(event)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_text))


def crawler_commands(event):
    input_text = event.message.text
    user_id = event.source.user_id

    if input_text == "NTU mail crawler":
        reply_text = "本功能會每十分鐘檢查一次您的 NTU 信箱有沒有新的信，\n有的話會用訊息提醒！\n但是會需要輸入您的記中帳密，\n並且會將該帳密和最新一封信件的編號儲存在線上資料庫。\n如有資安上的疑慮，請勿使用本功能。\n如果同意以上說明，且欲開啟本功能，\n請輸入「確認使用 NTU mail crawler」。"
    elif input_text == "確認使用 NTU mail crawler":
        reply_text = "好的，已開啟此功能。\n接下來請先確認收件匣中至少有一封信，\n然後按照下面格式輸入記中帳密：\n「crawler new account b092070XX XXXXXXXXXXX」。"
    elif "command" in input_text:
        reply_text = "目前可用的指令有：\n1. crawler command: 查詢所有可用的指令。\n\n2. crawler new account '學號' '密碼': 在指令後面接著記中帳密，就可以加入新帳號。\n\n3. crawler update password '學號' '密碼': 更新該學號的密碼\n\n4. crawler delete account '學號': 把該組記中帳密從資料庫中移除"
    elif "new account" in input_text:
        try:
            new_account(user_id, input_text)
            reply_text = "已完成資料上傳，將開始自動檢查新信件!!!\n如果要查詢其他指令，\n請輸入「crawler command」~"
        except:
            reply_text = "失敗了qq\n檢查看看帳密有打錯嗎?"
    elif "update password" in input_text:
        try:
            [account, password] = input_text.split(' ')[-2:]
            database.update_user_info(user_id, account=account, password=password)
            reply_text = f"已更新{account}的密碼~"
        except:
            reply_text = "失敗了qq\n"
    elif "delete account" in input_text:
        try:
            account = input_text.split(" ")[-1]
            database.delete_data(user_id, account)
            reply_text = f"已刪除{account}的學號，\n以及資料庫中所有和該學號有關的資料。\n感謝您的使用~"
        except:
            reply_text = "失敗了qq\n可能是資料庫中已經沒有該學號的資料，\n有其他問題請聯絡渭毛本人~"
    else:
        reply_text = "請確認輸入指令是否正確，或是洽詢渭毛本人w"
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