from messenger_driver import MessengerDriver

'''
Create automatic response to any unread conversation.
'''
if __name__ == '__main__':
    sender = MessengerDriver()
    msg = "您好，因為疫情關係目前被隔離中，請勿拍打餵食。"
    try:
        while True:
            url = sender.detect_new()
            sender.send(msg, url)
    except Exception:
        sender.close()

