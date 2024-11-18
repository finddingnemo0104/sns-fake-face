from flask import Flask, render_template

app = Flask(__name__)


@app.route('/login')
def hello_world():  # put application's code here
    return render_template('login.html', title="My Flask App ", heading="Hello, Flask!")

@app.route("/register")
def register():
    return render_template('register.html')  # Hiển thị file dangky.html


if __name__ == '__main__':
    app.run()
