# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created Date: 2022/08/12
# Author: Wei-Lun Lin
# Version: 1.0
# Email: weilun9539ny@gmail.com
# Status: Product

# Import modules
from linebot import LineBotApi
from linebot.models import TextSendMessage

from crawler import Crawler
import database
# Finish importing modules

# Initialization
line_bot_api = LineBotApi('quud2/CCW6i43uHAomVe8bMzRjHXbH5i/uqv82BmH6KqEa1BtTn1DU+U1yEnS6W90Sd1y+OW9QSsEmxNU83vl1RQcnj/7c4Qe2B8kSoz4sbzlbNTb1db9ygfHr3nobUlBu9ZWNj5bQFn+wPQ2dc7tgdB04t89/1O/w1cDnyilFU=')
# Finish initializing


def auto_check_mail():
    user_data_list = database.select_data()
    for user_data in user_data_list:
        user_id = user_data[1]
        crawler = Crawler(user_data[2], user_data[3])
        all_mail = crawler.get_mail(user_data[-1])

        if all_mail != []:
            # Update the last email uid in the database
            last_uid = all_mail[0].uid
            database.update_user_info(user_id, last_uid=last_uid)
            # Finish updating last email uid

            # Prepare message
            push_message = "收信囉~\n"
            for i in range(len(all_mail)):
                if len(all_mail) != 1:
                    push_message += f"--------\n信件 {i + 1}：\n"
                push_message += str(all_mail[i])
            # Finish preparing message

            # Send line message
            line_bot_api.push_message(user_id, TextSendMessage(push_message))
            # Finish sending message
# Finish defining functions


# Run the program
if __name__ == "__main__":
    auto_check_mail()
# Finish running the program
