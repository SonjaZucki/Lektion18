import random
from flask import Flask, render_template, request, redirect, url_for, make_response
from models import User, db

app = Flask(__name__)
db.create_all()


@app.route("/", methods=["GET"])
def index():
    email_address = request.cookies.get("email")

    if email_address:
        user = db.query(User).filter_by(email=email_address).first()
    else:
        user = None

    return render_template("index.html", user=user)

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")

    secret_number = random.randint(1, 30)

    user = db.query(User).filter_by(email=email).first()

    if not user:
        user = User(name=name, email=email, secret_number=secret_number)

        db.add(user)
        db.commit()

    response = make_response(redirect(url_for('index')))
    response.set_cookie("email", email)

    return response

@app.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("guess"))

    email_address = request.cookies.get("email")

    user = db.query(User).filter_by(email=email_address).first()

    if guess == user.secret_number:
        message = "Yes! The secret number is {0}".format(str(guess))

        new_secret = random.randint(1, 30)

        user.secret_number = new_secret

        db.add(user)
        db.commit()
    elif guess > user.secret_number:
        message = "Your guess is wrong ... try something smaller."
    elif guess < user.secret_number:
        message = "Your guess is wrong ... try something bigger."

    return render_template("result.html", message=message)


if __name__ == '__main__':
    app.run(debug=True)
