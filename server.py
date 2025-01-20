from flask import Flask,request
from flask import render_template
import requests
import smtplib
app = Flask(__name__)

my_email = "" # your email
password = "" # your password

def get_blog_posts():
    response = requests.get(url="https://api.npoint.io/b6f4bf5ce0ce3ba99575")
    response.raise_for_status()
    return response.json()

def send_email(message):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email ,to_addrs=my_email ,msg=message)

@app.route('/')
def home():
    posts = get_blog_posts()
    return render_template("home.html", posts=posts)

@app.route('/post/<int:num>')
def blog(num):
    posts = get_blog_posts()
    return render_template('post.html',blog_post=posts[num-1])

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        if not request.form:
            print("No form data received.")
        else:
            print("Form Data:", request.form)

        try:
            data = request.form
            msg = f"Subject: Contacted from BLOG Server\n\nName: {data["name"]}\nEmail: {data['email']}\nPhone: {data['phone']}\nMessage: {data["message"]}."
            send_email(message=msg)
            return render_template("contact.html", msg_sent=True)
        except KeyError as e:
            print(f"KeyError: Missing {e.args[0]} in form data.")
            return render_template("contact.html", msg_sent=False), 400

    return render_template("contact.html", msg_sent=False)

@app.route('/about')
def about():
    posts = get_blog_posts()
    return render_template('about.html')
        
if __name__ == "__main__":
    app.run(debug=True)