from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import json
from bs4 import BeautifulSoup

from config import Config
from credentials import cookies
from time import sleep
from config import Config


class TumblrSearch:

    def _get_proxy(self):

        url = "http://credsnproxy/api/v1/proxy"
        try:
            creds = requests.get(url=url).json()
            return creds

        except:
            return {"proxy_host": '179.43.159.93',
                    "proxy_port": '22866'}

    def __init__(self):

        self.Cookies = json.loads(cookies)

        self.cred = self._get_proxy()
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        # options.add_argument('--proxy-server=socks://' + self.cred['proxy_host'] + ':' + self.cred['proxy_port'])

        # self.driver = webdriver.Chrome(options=options)

        # remote webdriver
        self.driver = webdriver.Remote(
            command_executor='http://' + Config.SELENIUM_CONFIG['host'] + ':' + Config.SELENIUM_CONFIG[
                'port'] + '/wd/hub',
            desired_capabilities=options.to_capabilities(),
        )
        
    def search(self, query):

        url = 'https://www.tumblr.com/dashboard'
        self.driver.get(url)

        for cookie in self.Cookies:
            cookie_dict = {'domain': cookie['domain'], 'secure': cookie['secure'], 'value': cookie['value'],
                           'name': cookie['name'], 'httpOnly': cookie['httpOnly'], 'storeId': cookie['storeId'],
                           'path': cookie['path'], 'session': cookie['session'], 'hostOnly': cookie['hostOnly'],
                           'sameSite': cookie['sameSite'], 'id': cookie['id']}
            try:
                if cookie['expirationDate']:
                    cookie_dict['expirationDate'] = cookie['expirationDate']
                    # print(cookie['expirationDate'])
            except:
                pass
            # print(cookie_dict)
            self.driver.add_cookie(cookie_dict)
        self.driver.refresh()

        self.driver.find_element_by_id('search_query').send_keys(query)
        self.driver.find_element_by_id('search_query').send_keys(Keys.ENTER)
        # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "search_query"))).send_keys(query)
        # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "search_query"))).send_keys(Keys.ENTER)
        p = self.driver.page_source
        sleep(1)
        self.driver.close()
        # print(p)
        soup = BeautifulSoup(p, 'lxml')
        # print(soup.prettify())
        list1 = []
        post_search = soup.find("div", id="search_posts")
        for i in post_search.find_all("article"):
            # print(json.loads(i['data-json']))
            data = json.loads(i['data-json'])

            dict1 = dict()
            dict1['postid'] = data['id']
            # dict1['type'] = data['type']
            dict1['author_userid'] = data['tumblelog']
            dict1['author_image'] = data['tumblelog-data']['avatar_url']
            dict1['author_url'] = data['tumblelog-data']['url']
            # dict1['description'] = data['tumblelog-data']['description']
            dict1['author_name'] = data['tumblelog-data']['title']
            if not dict1['author_name']:
                dict1['author_name'] = None

            post = i.find("section", class_="post_content")
            try:
                post_image = post.find("img")['src']
                dict1['thumbnail'] = post_image
            except:
                dict1['thumbnail'] = None
            # try:
            #     post_video = post.find("source")['src']
            #     dict1['post_video'] = post_video
            # except:
            #     pass
            try:
                try:
                    post_content = post.find("p").text
                    dict1['content'] = post_content
                    if not dict1['content']:
                        dict1['content'] = None
                except:
                    dict1['content'] = None
            except:
                try:
                    post_content = post.find("h2").text
                    dict1['content'] = post_content
                    if not dict1['content']:
                        dict1['content'] = None
                except:
                    dict1['content'] = None
            tags = i.find("section", class_="post_tags")
            list2 = []
            try:
                for i in tags.find_all("a"):
                    # print(i.text)
                    list2.append(i.text)
            except AttributeError:
                pass

            dict1['tags'] = list2
            if not dict1['tags']:
                dict1['tags'] = None

            list1.append(dict1)
        return {"data":
                     list1
                }


if __name__ == '__main__':
    obj = TumblrSearch()
    print(obj.search('donald trump'))
