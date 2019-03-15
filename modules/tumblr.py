# from pymongo import MongoClient
import json
from bs4 import BeautifulSoup
import requests
from modules.sentiment import SentimentAnalysis
from credentials import api_key
# class Mongodata():
#     def mongodataa(self, data, db="tumblrdb", collection="tumblrcol"):
#
#         client = MongoClient()
#         db = client.db
#         collection = db.collection
#         collection.insert(data)


class Tumblr:
    
    def __init__(self):

        self.proxy = self._get_proxy()
        self.neg_count = 0
        self.neu_count = 0
        self.pos_count = 0
        self.obj = SentimentAnalysis()
        self.key = self._get_key()

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

    def _get_key(self):
        url = "http://credsnproxy/api/v1/tumblr"
        try:
            creds = requests.get(url=url).json()
            return creds['api_key']
        except:
            return api_key

    def getHtmlSoup(self, url, getRequestObject=False):
        req = requests.get(url=url, allow_redirects=False, proxies={"http": "socks5://"+self.proxy['proxy_host']+':'+self.proxy['proxy_port']})
        soup = BeautifulSoup(req.text, 'html.parser')
        if getRequestObject:
            return [req, soup]
        else:
            return soup

    def getPosts(self, query):

        domain = "https://api.tumblr.com/v2/blog/"+query+".tumblr.com/posts/text?api_key="+self.key+"&notes_info=true"
        k = requests.get(domain)
        m = k.text
        # print(m)
        n = json.loads(m)
        l = []
        # print(json.dumps(n))
        d = {}

        result = {}
        result["description"] = n["response"]["blog"]["description"]
        result["id"] = n["response"]["blog"]["name"]
        result["name"] = n["response"]["blog"]["title"]
        result["updated_at"] = n["response"]["blog"]["updated"]
        result["total_posts"] = n["response"]["blog"]["total_posts"]
        result["url"] = n["response"]["blog"]["url"]
        d["blog"] = result

        li = (n["response"]["posts"])
        count = 0
        for data in li:
            postresult = {}
            # postresult["type"] = data["type"]
            # postresult["blog_name"] = data["blog_name"]
            postresult["post_id"] = data["id"]
            postresult["post_url"] = data["post_url"]
            # postresult["slug"] = data["slug"]
            # postresult["date_time_string"] = data["date"]
            postresult["post_time"] = data["timestamp"]
            postresult["tags"] = data["tags"]
            if not postresult["tags"]:
                postresult["tags"] = None

            postresult["post_content"] = data["summary"]
            if not postresult["post_content"]:
                postresult["post_content"] = None

            t = data["summary"]
            # -------------------sentiments------
            pol = self.obj.analize_sentiment(t)
            postresult['polarity'] = pol

            if pol == 1:
                postresult['polarity'] = 'positive'
                self.pos_count += 1
            elif pol == -1:
                postresult['polarity'] = 'negative'
                self.neg_count += 1
            else:
                postresult['polarity'] = 'neutral'
                self.neu_count += 1

            postresult["post_title"] = data["title"]
            try:
                soup = BeautifulSoup(data["body"], 'html.parser')
                postresult["post_image"] = soup.find('img')['src']
            except:
                postresult["post_image"] = None
            l.append(postresult)

        ps = self.pos_count
        ng = self.neg_count
        nu = self.neu_count
        total = ps + ng + nu

        sentiments = dict()
        sentiments["positive"] = ps
        sentiments["negative"] = ng
        sentiments["neutral"] = nu

        d["post"] = l
        return {
            'data': {
                'results': d['post'],
                'blog': d['blog'],
                # 'total': len(d['post']),
                # 'sentiment': Sentiments
            }
        }


if __name__ == "__main__":

    obj = Tumblr()
    print(obj.getPosts("dragoni"))
# reasonandempathy
# somecutethings
