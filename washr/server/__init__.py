from datetime import date
from flask import Flask
from washr.server.tumblr import Tumblr

app = Flask(__name__)

from washr.server import routes

def setup(api_key, hostname, template):
    app.config["washr_template"] = template
    tumblr = Tumblr(api_key, hostname)

    info = tumblr.info()
    avatars = {
        16: tumblr.avatar(16),
        24: tumblr.avatar(24),
        30: tumblr.avatar(30),
        40: tumblr.avatar(40),
        48: tumblr.avatar(48),
        64: tumblr.avatar(64),
        96: tumblr.avatar(96),
        128: tumblr.avatar(128)
    }
    app.config["washr_posts"] = tumblr.posts()

    app.config["washr_ctx"] = {
        "Title": info["title"],
        "Description": info["description"],
        "Favicon": avatars[64],
        "PortraitURL-16": avatars[16],
        "PortraitURL-24": avatars[24],
        "PortraitURL-30": avatars[30],
        "PortraitURL-40": avatars[40],
        "PortraitURL-48": avatars[48],
        "PortraitURL-64": avatars[64],
        "PortraitURL-96": avatars[96],
        "PortraitURL-128": avatars[128],
        "CopyrightYears": date.today().year
    }
