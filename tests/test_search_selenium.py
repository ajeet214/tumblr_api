import pytest
from modules.search_selenium import TumblrSearch


@pytest.mark.parametrize("query",["bill gates", "emmanuel"])
def test_selenium_search(query):
    obj = TumblrSearch()
    res = obj.search(query)

    for i in res['data']:

        try:
            assert isinstance(i['author_userid'], str)
            assert i['author_userid'] is not ''
            assert ' ' not in i['author_userid']
        except:
            assert i['author_userid'] is None

        try:
            assert isinstance(i['postid'], str)
            assert i['postid'] is not ''
            assert ' ' not in i['postid']
        except:
            assert i['postid'] is None

        try:
            assert isinstance(i['author_name'], str)
            assert i['author_name'] is not ''
        except:
            assert i['author_name'] is None

        try:
            assert isinstance(i['content'], str)
            assert i['content'] is not ''
        except:
            assert i['content'] is None

        try:
            assert isinstance(i['author_image'], str)
            assert i['author_image'] is not ''
            assert i['author_image'].startswith('http')
        except:
            assert i['author_image'] is None

        try:
            assert isinstance(i['thumbnail'], str)
            assert i['thumbnail'] is not ''
            assert i['thumbnail'].startswith('http')
        except:
            assert i['thumbnail'] is None

        try:
            assert isinstance(i['author_url'], str)
            assert i['author_url'] is not ''
            assert i['author_url'].startswith('http')
        except:
            assert i['author_url'] is None

        try:
            assert type(i['tags']) == list
        except:
            assert i['tags'] is None
