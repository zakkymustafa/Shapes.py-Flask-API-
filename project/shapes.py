import math
from math import pi
from flask import jsonify, request, render_template,flash,redirect,session
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_user,logout_user,current_user
from forms import RegistrationForm,LoginForm
from oauth import OAuthSignIn


app = Flask(__name__)
app.config['SECRET_KEY']= '2dfca79bbfaa26c3fa36f265427564'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['OAUTH CREDENTIALS']= {
    "github": {
       "client_id": "47f92ab628588bc22769",
       "client_secret": "b5da0114e0c6f50c3cc0c88b7968fa69aac1b092"
    }
}

db = SQLAlchemy(app)
lm=LoginManager(app)
lm.login_view= "github"

class User(UserMixin,db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(30),unique=True,nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("github"))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('github'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/login/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('github'))
    oauth = OAuthSignIn.get_provider(provider)
    username, email = oauth.callback()
    if username is None:
        flash('Authentication failed.')
        return redirect(url_for('github'))
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username,email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('github'))




@app.route("/",methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/register",methods=["GET"])
def register():
    form=RegistrationForm()
    return render_template("register.html",form=form)

@app.route("/login",methods=["GET"])
def login():
    form=LoginForm()
    return render_template("login.html",form=form)

@app.route("/github",methods=["GET"])
def github():
    return render_template("gitlogin.html")   

# Start Circle
@app.route("/area/circle/<int:radius>",methods=["GET"])
def area_of_circle(radius):
    return jsonify({
        "result":radius**2*pi})

@app.route("/circumference/circle/<int:radius>",methods=["GET"])
def circumference_of_circle(radius):
    return jsonify({"result":2*pi*radius})

# End Circle

# Start Square
@app.route("/area/square/<int:side>",methods=["GET"])
def area_of_square(side):
    return jsonify({"result": side*side})

@app.route("/perimeter/square/<int:side>",methods=["GET"])
def perimeter_of_square(side):
    return jsonify({"result":side*4})
# End Square

# Start Rectangle
@app.route("/area/rectangle/<int:length>/<int:width>",methods=["GET"])
def area_of_rectangle(length,width):
    return jsonify({"result":length*width})

@app.route("/perimeter/rectangle/<int:length>/<int:width>",methods=["GET"])
def perimeter_of_rectangle(length,width):
    return jsonify({"result":2*length+2*width})
# End Rectangle

# Start Sphere
@app.route("/surfacearea/sphere/<int:radius>",methods=["GET"])
def surface_area(radius):
    return jsonify({"result":4*pi*radius**2})

@app.route("/volume/sphere/<int:radius>",methods=["GET"])
def volume(radius):
    return jsonify({"result":4/3*pi*radius*radius*radius})

# End Sphere

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)







