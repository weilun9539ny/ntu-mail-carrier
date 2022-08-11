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


def auto_check_mail():
    user_data_list = database.select_data()
    for user_data in user_data_list:
        user_id = user_data[1]
        crawler = Crawler(user_data[2], user_data[3])
        all_mail = crawler.get_mail(user_data[-1])

        if all_mail != []:
            # Update the last email uid in the database
            last_uid = all_mail[0].uid
            # database.update_user_info(user_id, last_uid=last_uid)
            # Finish updating last email uid

            # Prepare message
            push_message = ""
            for i in range(len(all_mail)):
                push_message += f"信件 {i + 1}：\n"
                push_message += str(all_mail[i])
                if i < (len(all_mail) - 1):
                    push_message += "\n-----\n"
            # Finish preparing message

            # Send line message
        line_bot_api.push_message(user_id, TextSendMessage(push_message))
# Finish defining functions


# Run the program
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    auto_check_mail()
# Finish running the program