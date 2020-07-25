from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time
import errno

MESSENGER_URL = 'https://www.messenger.com'

class MessengerDriver():
    def __init__(self, browser, user=None, pwd=None):
        
        if browser == 'firefox' or browser == 'Firefox':
            self._driver = webdriver.Firefox()
        elif browser == 'chrome' or browser == 'Chrome':
            self._driver = webdriver.Chrome()
        else:
            raise ValueError('Invalid browser: has to be Firefox or Chrome')
        
        # Open Firefox or Chrome and establish connection with messenger.com
        self._driver.get(MESSENGER_URL)

        try:
            # Load cookies from the file MessengerCookies.pkl 
            # (in order not to login once again)
            for cookie in pickle.load(open("MessengerCookies.pkl", "rb")):
                self._driver.add_cookie(cookie)

            # Reload the page with the loaded cookies
            self._driver.get(MESSENGER_URL)
        
        # Never logged in
        except EnvironmentError as e:
            # FileNotFoundError in Python3 and IOError or OSError in Python2
            if e.errno == errno.ENOENT:
                # if login information specified
                wait = WebDriverWait(self._driver, 30)
                if user and pwd:
                    wait.until(EC.visibility_of_element_located(
                        (By.ID, "email"))).send_keys(user)
                    wait.until(EC.visibility_of_element_located(
                        (By.ID, "pass"))).send_keys(pwd)
                    wait.until(EC.visibility_of_element_located(
                        (By.ID, "loginbutton"))).click()
                # else user have to login manually
                else:
                    wait.until(
                        EC.visibility_of_element_located((By.XPATH,
                            "//ul[@aria-label='Conversation List']")))
                
                # dump cookies to file once logged in manually
                pickle.dump(self._driver.get_cookies(), 
                    open("MessengerCookies.pkl", "wb"))
    
    def sendto(self, url):
        """get inside a conversation

        :Args:
         - url - the url corresponding to the conversation

        :Raises:
         - ValueError - not a valid Messenger url

        """

        if not url.startswith(MESSENGER_URL+'/t/'):
            raise ValueError('not a valid conversation url')
        
        self._driver.get(url)
    
    def send(self, text, nb=1, interval=0.5):
        """send a text

        :Args:
         - text     - the text to send
         - nb       - if multiple sending
         - interval - time interval between multiple messages

        """
        
        textbox = WebDriverWait(self._driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, 
            "//div[contains(@class, '_5rpu') and @role='combobox']")))

        for _ in range(nb):
            textbox.send_keys(text + Keys.ENTER)
            time.sleep(interval)

    def detect_new(self):
        """detect unread message (bold conversations)

        :Returns:
         - String - the url of the first unread conversation

        """
        new = WebDriverWait(self._driver, 100000).until(
            EC.visibility_of_element_located((By.XPATH,
                "//ul[@aria-label='Conversation List']" +
                "/li[@aria-live='polite']" +
                "/div[1]/a[1]")))
        return new.get_attribute("data-href")

    def close(self):
        """close the browser
        """
        try:
            self._driver.close()
        except Exception as e:
            print(e)
            pass
