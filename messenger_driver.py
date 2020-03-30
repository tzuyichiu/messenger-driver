from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle

MESSENGER_URL = 'https://www.messenger.com'

class MessengerDriver():
    def __init__(self, user=None, pwd=None):
        self._driver = webdriver.Firefox()
        
        # Open Firefox and establish connection with messenger.com
        self._driver.get(MESSENGER_URL)

        self._wait = WebDriverWait(self._driver, 1000)

        try:
            # Load cookies from the file MessengerCookies.pkl 
            # (in order not to login once again)
            for cookie in pickle.load(open("MessengerCookies.pkl", "rb")):
                self._driver.add_cookie(cookie)

            # Reload the page with the loaded cookies
            self._driver.get(MESSENGER_URL)
        
        except FileNotFoundError:
            # Never logged in 

            # if login information specified
            if user and pwd:
                self._wait.until(EC.visibility_of_element_located(
                    (By.ID, "email"))).send_keys(user)
                self._wait.until(EC.visibility_of_element_located(
                    (By.ID, "pass"))).send_keys(pwd)
                self._wait.until(EC.visibility_of_element_located(
                    (By.ID, "loginbutton"))).click()
            # else user have to login manually
            else:
                WebDriverWait(self._driver, 1000).until(
                    EC.visibility_of_element_located((By.XPATH,
                        "//ul[@aria-label='Conversation List']")))
            
            # dump cookies to file once logged in manually
            pickle.dump(self._driver.get_cookies(), 
                open("MessengerCookies.pkl", "wb"))
    
    def send(self, text, url):
        """send a text in a conversation

        :Args:
         - text - the text to send
         - url - the url corresponding to the conversation

        :Raises:
         - ValueError - not a valid Messenger url

        """
        if not url.startswith(MESSENGER_URL+'/t/'):
            raise ValueError('not a valid conversation url')
        
        self._driver.get(url)

        textbox = self._wait.until(
            EC.visibility_of_element_located((By.XPATH, 
            "//div[contains(@class, '_5rpu') and @role='combobox']")))

        textbox.send_keys(text + Keys.ENTER)

    def detect_new(self):
        """detect unread message (bold conversations)

        :Returns:
         - String - the url of the first unread conversation

        """
        new = WebDriverWait(self._driver, 1000).until(
            EC.visibility_of_element_located((By.XPATH,
                "//ul[@aria-label='Conversation List']" +
                "/li[@aria-live='polite']" +
                "/div[1]/a[1]")))
        return new.get_attribute("data-href")

    def close(self):
        """close the browser (Firefox)
        """
        try:
            self._driver.close()
        except:
            pass
