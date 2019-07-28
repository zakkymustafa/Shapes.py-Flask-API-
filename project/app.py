import math
from math import pi
from flask import jsonify, request
from flask import Flask
app = Flask(__name__)


@app.route("/",methods=["GET"])
def home():
    return jsonify({"about":"Welcome to my Calculator"})

# Start Circle
@app.route("/area/circle/<int:radius>",methods=["GET"])
def area_of_circle(radius):
    return jsonify({"result":radius**2*pi})

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







