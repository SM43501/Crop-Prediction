import numpy as np
from flask import Flask, request, render_template
import pickle
import os

# Create Flask app
flask_app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))

# Home route
@flask_app.route("/")
def Home():
    return render_template("index.html")

# Predict route
@flask_app.route("/predict", methods=["POST"])
def predict():
    # Get input values from the form
    float_features = [float(x) for x in request.form.values()]
    features = [np.array(float_features)]

    # Predict the crop
    prediction = model.predict(features)
    crop_name = prediction[0].lower()  # Make the prediction lowercase to match the image file name

    # Compose the image filename (assuming .jpg format)
    image_filename = f"{crop_name}.jpg"
    image_path = os.path.join("static", "images", image_filename)

    # Check if the image exists in the static/images folder
    if not os.path.exists(image_path):
        image_filename = None  # Set to None if no image is found
    else:
        image_filename = f"images/{image_filename}"  # Use relative path for HTML rendering

    # Render the template with prediction and image filename
    return render_template(
        "index.html",
        prediction_text=f"The Predicted Crop is {prediction[0]}",
        image_filename=image_filename
    )

# Help route
@flask_app.route("/help")
def help():
    return render_template("help.html")  # Ensure you have a 'help.html' in the 'templates' folder

# Tips route
@flask_app.route("/tips")
def tips():
    return render_template("tips.html")  # Ensure you have a 'tips.html' in the 'templates' folder

if __name__ == "__main__":
    flask_app.run(debug=True)
