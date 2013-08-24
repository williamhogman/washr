from washr.server import app
from flask import url_for

@app.route("/")
def index():
    template = app.config["washr_template"]
    posts = app.config["washr_posts"]
    ctx = dict(app.config["washr_ctx"])

    ctx["Posts"] = [{
        "PostType": post["type"].capitalize(),
        "Permalink": url_for("post", id=post["id"], slug=post["slug"]),
        "PostID": post["id"],
        "Title": post.get("title", ""),
        "Body": post.get("body", ""),
        "Text": True if post["type"] == "text" else False
    } for post in posts]

    return template.render(ctx)

@app.route("/post/<int:id>/<slug>", endpoint="post")
def post(id, slug):
    template = app.config["washr_template"]
    posts = app.config["washr_posts"]
    ctx = dict(app.config["washr_ctx"])

    ctx["Posts"] = [{
        "PostType": post["type"].capitalize(),
        "Permalink": url_for("post", id=post["id"], slug=post["slug"]),
        "PostID": post["id"],
        "Title": post.get("title", ""),
        "Body": post.get("body", ""),
        "Text": True if post["type"] == "text" else False
    } for post in posts if post["id"] == id]

    return template.render(ctx)
