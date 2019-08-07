import math
from math import pi
from flask import jsonify, request, render_template,flash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_user,logout_user,current_user
from forms import RegistrationForm,LoginForm

app = Flask(__name__)
app.config['SECRET_KEY']= '2dfca79bbfaa26c3fa36f265427564'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(30),unique=True,nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"




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

@app.route("/github_login",methods=["GET"])
def github_login():
    return render_template("gitlogin.html",)    

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
    app.run(debug=True)







