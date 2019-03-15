import pytest
from modules.tumblr import Tumblr


@pytest.mark.parametrize("query",["reasonandempathy", "somecutethings"])
def test_tumblr_search(query):
    obj = Tumblr()
    res = obj.getPosts(query)

    for i in res['data']['results']:

        try:
            assert isinstance(i['post_id'], int)
            assert i['post_id'] is not ''
        except:
            assert i['post_id'] is None

        try:
            assert isinstance(i['post_content'], str)
            assert i['post_content'] is not ''
        except:
            assert i['post_content'] is None

        try:
            assert isinstance(i['post_title'], str)
            assert i['post_title'] is not ''
        except:
            assert i['post_title'] is None

        try:
            assert isinstance(i['post_image'], str)
            assert i['post_image'] is not ''
            assert i['post_image'].startswith('http')
        except:
            assert i['post_image'] is None

        try:
            assert isinstance(i['post_url'], str)
            assert i['post_url'] is not ''
            assert i['post_url'].startswith('http')
        except:
            assert i['post_url'] is None

        try:
            assert type(i['tags']) == list
        except:
            assert i['tags'] is None

        assert i['polarity'] is 'positive' or 'negative' or 'neutral'

        try:
            assert isinstance(i['post_time'], int)
        except:
            assert i['post_time'] is None