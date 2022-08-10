class Mail:
    def __init__(self, uid, subject, datetime, sender, address):
        self.uid = uid
        self.subject = subject
        self.datetime = datetime
        self.sender = sender
        self.address = address
    

    def __repr__(self):
        uid_str = f"uid: {self.uid}\n"
        subject_str = f"subject: {self.subject}\n"
        time_str = f"Send time: {self.datetime}\n"
        sender_str = f"Sender: {self.sender}\n"
        address_str = f"Email address: {self.address}\n"

        output_str = "Email information:\n" + uid_str + subject_str + time_str + sender_str + address_str
        return output_str
