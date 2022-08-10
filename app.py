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

    if input_text == "阿彌陀佛狒狒":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=input_text)
        )
    if input_text == "謝謝":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="你很有禮毛餒")
        )
    if input_text == "show user":
        line_bot_api.reply_message(
            event.reply_token, text=str(event)
        )
    if input_text == "NTU mail crawler":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=
                    """本功能可以每小時都檢查一次您的 NTU 信箱有沒有新的信，
                    有的話就在這邊提醒你。
                    但是會需要輸入您的記中帳密，
                    並且會將該帳密和最新一封信件的編號儲存在線上資料庫。
                    如有資安上的疑慮，請勿使用本功能。
                    如果同意以上說明，且欲開啟本功能，
                    請輸入「確認使用 NTU mail crawler」。""")
        )
    if input_text == "確認使用 NTU mail crawler":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="""好的，已開啟此功能。
                接下來請按照下面格式輸入記中帳密：
                「crawler new account b09207052 A123456789」。
                （如果之後要更新帳號，可以輸入「crawler update account」）
                除此之外，輸入帳密之前，請確定收件匣中至少有一封信~""")
        )
    if "crawler" in input_text:
        if "new account" in input_text:
            # Collect user information
            user_account = input_text.split(" ")[-2]
            password = input_text.split(" ")[-1]
            crawler = Crawler(user_account, password)
            last_uid = crawler.get_last_mail_id()
            # Finish collecting user information
# Finish defining functions


# Run the program
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
# Finish running the program