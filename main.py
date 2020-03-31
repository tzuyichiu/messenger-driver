from messenger_driver import MessengerDriver

'''
Create automatic response to any unread conversation.
'''
if __name__ == '__main__':
    sender = MessengerDriver()
    try:
        while True:
            url = sender.detect_new()
            if url.endswith('12345678'): # example
                sender.send('Hello', url)
    except Exception as e:
        sender.close()
        print(e)

