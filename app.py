from app import create_app, db


@app.route('/login')
def hello_world():  # put application's code here
    return render_template('login.html', title="My Flask App ", heading="Hello, Flask!")

@app.route("/register")
def register():
    return render_template('register.html')  # Hiển thị file dangky.html

app = create_app()
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run()
