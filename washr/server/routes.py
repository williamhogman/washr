from washr.server import app

@app.route("/")
def index():
    template = app.config["washr_template"]
    posts = app.config["washr_posts"]
    ctx = dict(app.config["washr_ctx"])

    return template.render(ctx)

@app.route("/post/<id>/<slug>")
def post(id, slug):
    passapp.config["washr_posts"]
