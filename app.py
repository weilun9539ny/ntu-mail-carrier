from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

app = Flask(__name__)

line_bot_api = LineBotApi('quud2/CCW6i43uHAomVe8bMzRjHXbH5i/uqv82BmH6KqEa1BtTn1DU+U1yEnS6W90Sd1y+OW9QSsEmxNU83vl1RQcnj/7c4Qe2B8kSoz4sbzlbNTb1db9ygfHr3nobUlBu9ZWNj5bQFn+wPQ2dc7tgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('27893c48e684e0563636ed0a27674e51')


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
    if event.message.text == "阿彌陀佛狒狒":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="蛤?")
        )


if __name__ == "__main__":
    # app.run()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)