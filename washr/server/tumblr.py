from datetime import date
import requests

info_url = "http://api.tumblr.com/v2/blog/{0}/info"
avatar_url = "http://api.tumblr.com/v2/blog/{0}/avatar/{1}"
posts_url = "http://api.tumblr.com/v2/blog/{0}/posts"

def ctx(api_key, hostname):
    url = posts_url.format(hostname)
    r = requests.get(url, params={"api_key": api_key})
    data = r.json()["response"]
    info = data["blog"]
    posts = data["posts"]

    url = posts_url.format(hostname)
    r = requests.get(url, params={"api_key": api_key})

    return {
        "Title": info["title"],
        "Description": info["title"],
        "MetaDescription": info["title"],
        "RSS": info["title"],
        "Favicon": info["title"],
        "CustomCSS": info["title"],
        "PortraitURL-16": "",
        "PortraitURL-24": "",
        "PortraitURL-30": "",
        "PortraitURL-40": "",
        "PortraitURL-48": "",
        "PortraitURL-64": "",
        "PortraitURL-96": "",
        "PortraitURL-128": "",
        "CopyrightYears": date.today().year,
    }


class Tumblr(object):
    def __init__(self, api_key, hostname):
        self.hostname = hostname
        self.api_key = api_key

    def info(self):
        url = info_url.format(self.hostname)
        r = requests.get(url, params={"api_key": self.api_key})
        return r.json()["response"]["blog"]

    def avatar(self, size=64):
        url = avatar_url.format(self.hostname, str(size))
        return url
        #r = requests.get(url, params={"api_key": self.api_key})
        #print(r.text)
        #return r.json()["response"]["avatar_url"]

    def posts(self):
        url = posts_url.format(self.hostname)
        r = requests.get(url, params={"api_key": self.api_key})
        posts = r.json()["response"]["posts"]
