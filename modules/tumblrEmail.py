from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import requests

from config import Config


class EmailChecker:

    def _get_proxy(self):
        url = "http://credsnproxy/api/v1/proxy"
        try:
            req = requests.get(url=url)
            if req.status_code != 200:
                raise ValueError
            return req.json()
        except:
            return {"proxy_host": '103.59.95.71',
                    "proxy_port": '23344'}

    def __init__(self):

        self.cred = self._get_proxy()
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        # options.add_argument('--proxy-server=socks://' + self.cred['proxy_host'] + ':' + self.cred['proxy_port'])

        # self.driver = webdriver.Chrome(chrome_options=options)

        # remote webdriver
        self.driver = webdriver.Remote(
            command_executor='http://' + Config.SELENIUM_CONFIG['host'] + ':' + Config.SELENIUM_CONFIG[
                'port'] + '/wd/hub',
            desired_capabilities=options.to_capabilities(),
        )

        self.EMAILFIELD = (By.ID, "signup_determine_email")
        self.SUBMITBUTTON = (By.ID, "signup_forms_submit")


    def checker(self, emailId):
        url = "https://www.tumblr.com/login#"
        self.driver.get(url)
        sleep(1)
        # print(emailId)

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.EMAILFIELD)).send_keys(emailId)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.SUBMITBUTTON)).click()
        # print("%s seconds" % (time.time() - start_time))
        sleep(0.5)
        try:
            mailid1 = self.driver.find_element_by_xpath('//*[@id="signup_form_errors"]/li')
            sleep(0.5)
            print(mailid1.text)
            self.driver.quit()

            return {'profileExists': False}
        except:
            mailid = self.driver.find_element_by_xpath('//*[@id="signup_magiclink"]/div[1]/a')
            sleep(2)
            print(mailid.text)
            self.driver.quit()

            return {'profileExists': True,
                    'profile': emailId}


if __name__ == '__main__':
    obj = EmailChecker()
    # justinmat1994@gmail.com
    print(obj.checker('justinmat1994@gmail.com'))
