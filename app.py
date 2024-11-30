
from flask import Flask, request, render_template,jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

# Specify the directory where the model is saved
model_directory = os.path.abspath(r'C:\Users\prasad bolgss\OneDrive\Documents\car\Model.pkl')

# Specify the directory where the scaler and label encoder pickle files are saved


# Load the trained model
with open(model_directory, 'rb') as model_file:
    model = pickle.load(model_file)
with open(r"C:\Users\prasad bolgss\OneDrive\Documents\car\Scaler.pkl", "rb") as scaler_file:
    sc=pickle.load(scaler_file)

# Load the label encoder

@app.route('/')
def car():
    return render_template('vehicle.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from the form
        model_year = int(request.form['Year'])
        kms_driven = int(request.form['Kms_Driven'])
        current_market_price = float(request.form['Present_Price'])
        vehicle_type = request.form['vehicle_type']
        fuel_type = request.form['Fuel_Type']
        seller_type = request.form['Seller_Type']
        owner_type = int((request.form['Owner']))
        transmission = request.form['Transmission']

        # Prepare input data as a list of features
        input_data = np.array([[
            model_year,
            current_market_price,
            kms_driven,
            fuel_type,
            seller_type,
            transmission,
            owner_type,
            vehicle_type
        ]])
        x=sc.transform(input_data)
        x=x.reshape(1,-1)

        # Make predictions using the preprocessed input data
        prediction = model.predict(x) # Assuming you expect a single prediction
        prediction=float(prediction*100000)
        # Format the prediction result as a dictionary
        result = round(prediction,2)

        return str(f"The Predicted Price of Your vehicle is Rs.{result}")


    except Exception as e:
        # Handle errors gracefully and return an error message
        error_message = str(e)
        return jsonify({'error': error_message}), 400  # Return a 400 Bad Request status code

if __name__ == '__main__':
    app.run(debug=True)
