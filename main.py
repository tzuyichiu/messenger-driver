import sys, getopt
from messenger_driver import MessengerDriver

'''
Create automatic response to any unread conversation.
'''
def parse(argv):
    browser = None
   
    try:
        opts, args = getopt.getopt(argv, "hb:", ['help', 'browser'])
    except getopt.GetoptError:
        print('usage: python main.py -b <browser>')
        sys.exit(1)
    
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('usage: python main.py -b <browser>')
            sys.exit(1)
        elif opt in ('-b', '--browser'):
            browser = arg
    
    if not browser:
        print('usage: python main.py -b <browser>')
        sys.exit(1)

    return browser

def autoreply(browser, text):
    sender = MessengerDriver(browser)
    try:
        while True:
            url = sender.detect_new()
            sender.sendto(url)
            sender.send(text)

    except Exception as e:
        sender.close()
        print(e)

def flood(browser, url, text, nb, interval=0.5):
    sender = MessengerDriver(browser)
    try:
        sender.sendto(url)
        sender.send(text, nb=nb, interval=interval)
    except Exception as e:
        sender.close()
        print(e)
    finally:
        sender.close()

if __name__ == "__main__":
    browser = parse(sys.argv[1:])
    autoreply(browser, 'hello')
