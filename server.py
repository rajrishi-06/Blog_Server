from flask import Flask
from flask import render_template
import requests

app = Flask(__name__)

def get_blog_posts():
    response = requests.get(url="https://api.npoint.io/55c36f62cc51a5bca5b5")
    response.raise_for_status()
    return response.json()

@app.route('/')
def home():
    posts = get_blog_posts()
    return render_template("home.html", posts=posts)

@app.route('/post/<int:num>')
def blog(num):
    posts = get_blog_posts()
    return render_template('post.html',blog_post=posts[num-1])
if __name__ == "__main__":
    app.run(debug=True)