class Mail:
    def __init__(self, uid, subject, datetime, sender, address):
        self.uid = uid
        self.subject = subject
        self.datetime = datetime
        self.sender = sender
        self.address = address
    

    def __repr__(self):
        subject_str = f"主旨：{self.subject}\n"
        time_str = f"寄達時間：{self.datetime}\n"
        sender_str = f"寄件者：{self.sender}\n"
        address_str = f"寄件者電子郵件：{self.address}"

        output_str = subject_str + time_str + sender_str + address_str
        return output_str
