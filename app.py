from flask import Flask, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, db

app = Flask(__name__, template_folder=".", static_folder=".", static_url_path="")

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:vengat%40123@localhost/flask_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def home():
    return redirect(url_for("signup"))

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if password != confirm_password:
        return "Passwords do not match"

    if User.query.filter_by(email=email).first():
        return "Email already registered"

    user = User(
        name=name,
        email=email,
        password=generate_password_hash(password)
    )

    db.session.add(user)
    db.session.commit()

    return redirect(url_for("signin"))

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        return "Login successful"

    return "Invalid email or password"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)