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
            TextSendMessage(text=event.message.text)
        )
    if input_text =="謝謝":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="你很有禮毛餒")
        )
    elif input_text == "功能":
        exhibit = 0
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="目前只有提醒作業的功能，是否觀看說明？",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="是", text="Ok!")),
                        QuickReplyButton(action=MessageAction(label="否", text="No!")),
                        QuickReplyButton(action=PostbackAction(
                            label="postback",
                            display_text="postback text",
                            data="postback_data"
                        ))
                    ]
                )
            )
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text="蛤?"),
            TextSendMessage(text="聽不懂你在說啥餒")]
        )


@handler.add(PostbackEvent)
def handle_postback(event):
    if event == "postback_data":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="說明文")
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="答錯")
        )
# Finish defining functions


# Run the program
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
# Finish running the program