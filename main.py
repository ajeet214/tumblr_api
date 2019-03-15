from flask import Flask, jsonify, request
from modules.tumblr import Tumblr
from modules.tumblr_db import ProfileExistence
from modules.search_selenium import TumblrSearch
from raven.contrib.flask import Sentry

app = Flask(__name__)
sentry = Sentry(app)


@app.route('/api/v1/search')
def search():
    query = request.args.get('q')
    tumblr = TumblrSearch()
    return jsonify(tumblr.search(query))


@app.route('/api/v1/profile/posts')
def posts():
    query = request.args.get('id')
    tumblr = Tumblr()
    return jsonify(tumblr.getPosts(query))


@app.route('/api/v1/search/id')
def search_email():
    mail = request.args.get('q')
    # obj = EmailChecker()
    obj1 = ProfileExistence()
    data = obj1.db_check(mail)
    # return jsonify({'result': data})
    return jsonify({'data': {"availability": data['profileExists']}})


if __name__ == '__main__':
    app.run(port=5019)
