import numpy as np
from flask import Flask, request, render_template
import joblib

# Load the model
model = joblib.load('pipeline.pkl')

# Create Flask app
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/predict", methods=['POST'])
def predict():
    try:
        # Get form data
        N = float(request.form.get('Nitrogen', 0))
        P = float(request.form.get('Phosporus', 0))
        K = float(request.form.get('Potassium', 0))
        Temperature = float(request.form.get('Temperature', 0))
        Humidity = float(request.form.get('Humidity', 0))
        ph = float(request.form.get('potential_of_hydrogen', 0))
        Rainfall = float(request.form.get('Rainfall', 0))

        # Validate form data
        if not all([N, P, K, Temperature, Humidity, ph, Rainfall]):
            return render_template('index.html', error='Please fill out all fields.')

        # Prepare the input data
        input_data = [[N, P, K, Temperature, Humidity, ph, Rainfall]]

        # Predict the crop
        prediction = model.predict(input_data)[0]

        return render_template('index.html', prediction=prediction)
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(debug=True)
