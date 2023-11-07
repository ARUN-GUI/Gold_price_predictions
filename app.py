from flask import Flask, render_template, request, jsonify
import requests
import json
from datetime import datetime, timedelta
import numpy as np
from tensorflow import keras

app = Flask(__name__)

# Replace with your actual Gold API key
API_KEY = "goldapi-1d67wrlogrj9de-io"

# Load the pre-trained model
model = keras.models.load_model('model.h5')

@app.route('/', methods=['GET', 'POST'])
def index():
    current_date = datetime.today()

    # Calculate the date for the previous day
    previous_date = current_date - timedelta(days=1)

    # Format the date as '/YYYYMMDD'
    date_str = previous_date.strftime("/%Y%m%d")

    # Build the API URL
    symbol = "XAU"
    curr = "USD"
    url = f"https://www.goldapi.io/api/{symbol}/{curr}{date_str}"

    # Set headers for the API request
    headers = {
        "x-access-token": API_KEY,
        "Content-Type": "application/json"
    }
    if request.method == 'POST':
        prev_close_price = float(request.form['prev_close_price'])
        ch = float(request.form['ch'])
        chp = float(request.form['chp'])
        if prev_close_price is None:
            prev_close_price = 0.0  # or any other default value
        if ch is None:
            ch = 0.0  # or any other default value
        if chp is None:
            chp = 0.0
        # Prepare input data for the model
        input_data = np.array([[prev_close_price, ch, chp]])

        # Make predictions using the loaded model
        price_prediction = model.predict(input_data)[0][0]

        return render_template('result1.html',
                               price_prediction=price_prediction)
    try:
        # Make the API request
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse the JSON response
        gold_data = json.loads(response.text)

        # Extract the desired fields (prev_close_price, ch, chp)
        prev_close_price = gold_data.get("prev_close_price")
        ch = gold_data.get("ch")
        chp = gold_data.get("chp")
        if prev_close_price is None and ch is None and chp is None:
            current_date = datetime.today()

            # Calculate the date for the previous day
            previous_date = current_date - timedelta(days=2)

            # Format the date as '/YYYYMMDD'
            date_str = previous_date.strftime("/%Y%m%d")

            # Build the API URL
            symbol = "XAU"
            curr = "USD"
            url = f"https://www.goldapi.io/api/{symbol}/{curr}{date_str}"

            # Set headers for the API request
            headers = {
                "x-access-token": API_KEY,
                "Content-Type": "application/json"
            }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse the JSON response
        gold_data = json.loads(response.text)

        # Extract the desired fields (prev_close_price, ch, chp)
        prev_close_price = gold_data.get("prev_close_price")
        ch = gold_data.get("ch")
        chp = gold_data.get("chp")

        # Prepare input data for the model
        input_data = np.array([[prev_close_price, ch, chp]])

        # Make predictions using the loaded model
        price_prediction = model.predict(input_data)[0][0]
        
        return render_template('result.html',
                               date=previous_date.strftime("%Y-%m-%d"),
                               prev_close_price=prev_close_price,
                               ch=ch,
                               chp=chp,
                               price_prediction=price_prediction)
    except requests.exceptions.RequestException as e:
        error_message = {"error": str(e)}
        return jsonify(error_message), 500  # Return a 500 Internal Server Error

if __name__ == '__main__':
    app.run(debug=True)
