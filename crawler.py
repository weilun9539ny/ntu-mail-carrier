# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created Date: 2022/08/12
# Author: Wei-Lun Lin
# Version: 1.0
# Email: weilun9539ny@gmail.com
# Status: Product

# Import libraries
import time
import json
import requests
from bs4 import BeautifulSoup as bs4
# Finish importing libraries

# Import a class
from mail import Mail
# Finish importing a class


# Define a class
class Crawler(object):
    def __init__(self, account, password):
        self.account = account
        self.password = password

    def _login(self, s):
        # Set up
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67"
            " Safari/537.36"}
        login_data = {}
        login_url = "https://wmail1.cc.ntu.edu.tw/rc/index.php"
        # Finish setting up

        # To know where the user and password should be filled in
        pre_login_req = s.get(login_url, headers=headers)
        form = bs4(pre_login_req.text, "html.parser").find("form")
        time.sleep(2)
        for input in form.find_all("input"):
            login_data[input.get("name")] = input.get("value") or ""
        login_data["_user"] = self.account
        login_data["_pass"] = self.password
        # Finish finding the input locations

        # Login with user and password
        login_req = s.post(
            login_url,
            data=login_data,
            allow_redirects=True,
            headers=headers
        )
        time.sleep(1)

    def _mail_info_intepreter(self, mail):
        # Cope with the string
        begin_index = mail.find("subject") - 2
        end_index = mail.find("seen") - 3
        mail_dic = json.loads(mail[begin_index: end_index])
        # Done with the string, find the dictionary

        # Get all the information
        subject = mail_dic["subject"]
        date = mail_dic["date"]

        fromto = mail_dic["fromto"]
        i_1 = fromto.find("title") + 7
        i_2 = fromto.find("class=\"rcmContact") - 2
        i_3 = fromto.find("Address") + 9
        i_4 = fromto.find("<\span><\span>") - 13
        email_address = fromto[i_1: i_2]
        sender = fromto[i_3: i_4]

        index_id_begin = mail.find("add_message_row") + 16
        index_id_end = begin_index - 1
        mail_id = int(mail[index_id_begin:index_id_end])
        # Finish getting information

        # Create a mail object
        new_mail = Mail(mail_id, subject, date, sender, email_address)
        # Finish creating a mail object
        return new_mail

    def get_mail(self, last_uid):
        # Set up
        inbox_url = "https://wmail1.cc.ntu.edu.tw/rc/?_task=mail&_action=list\
            &_refresh=1&_layout=widescreen&_mbox=INBOX&_remote=1"
        mail_list = []
        i_mail = 0
        # Finish setting up

        with requests.Session() as s:
            self._login(s)
            r = s.get(inbox_url)
            mail_box = json.loads(r.text)
            existing_mail = mail_box["env"]["exists"]
            mails = mail_box["exec"].split("\n")[4:-2]

            while True:
                if i_mail >= existing_mail:
                    break  # Prevent the situation that running out of index

                # Get a mail object
                mail = mails[i_mail]
                new_mail = self._mail_info_intepreter(mail)
                # Finish getting a mail object

                # Check if the mail was crawled
                if new_mail.uid == last_uid:
                    break
                # Finish checking older mail

                mail_list.append(new_mail)  # Store the information
                i_mail += 1
        return mail_list

    def get_last_mail_id(self):
        # Set up
        inbox_url = "https://wmail1.cc.ntu.edu.tw/rc/?_task=mail&_action=list\
            &_refresh=1&_layout=widescreen&_mbox=INBOX&_remote=1"
        # Finish setting up

        with requests.Session() as s:
            self._login(s)
            r = s.get(inbox_url)
            mail_box = json.loads(r.text)

            # Get a mail object
            first_mail = mail_box["exec"].split("\n")[4]
            first_mail = self._mail_info_intepreter(first_mail)
            # Finish getting a mail object

            time.sleep(2)
            last_uid = first_mail.uid
            return last_uid
# Finish defining a class


# Test code
if __name__ == "__main__":
    account = "b09207052"
    password = "Chaeyoung0423"

    crawler = Crawler(account, password)
    # mail = crawler.get_mail()
    uid = crawler.get_last_mail_id()
    # print(mail)
    print(uid)
# Finish testing code
