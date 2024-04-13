from flask_cors import CORS
from flask import Flask, request, jsonify
import torch
import pandas as pd

app = Flask(__name__)
cors = CORS(app)

# Load the model
model_loaded = torch.load("./full_model.pt")

@app.route('/predict_price', methods=['POST'])
def predict_price():
    try:
        # Get the parameters from the request
        data = request.json

        # resolve parameter
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        Type = data['Type']
        bedroom = float(data['bedroom'])
        bathroom = float(data['bathroom'])
        hydro = data['hydro']
        heat = data['heat']
        water = data['water']
        wi_fi_and_more = data['wi_fi_and_more']
        parking_included = int(data['parking_included'])
        agreement_type = data['agreement_type']
        move_in_date = data['move_in_date']
        pet_friendly = data['pet_friendly']
        size_sqft = float(data['size_sqft'])
        furnished = data['furnished']
        laundry_in_unit = data['laundry_in_unit']
        laundry_in_building = data['laundry_in_building']
        dishwasher = data['dishwasher']
        air_conditioning = data['air_conditioning']
        personal_outdoor_space = data['personal_outdoor_space']
        smoking_permitted = data['smoking_permitted']

        hydro = hydro.capitalize()
        heat = heat.capitalize()
        water = water.capitalize()
        utilities_included = ", ".join([f"Yes: {hydro}" if hydro == 'Yes' else "No: Hydro",
                                        f"Yes: {heat}" if heat == 'Yes' else "No: Heat",
                                        f"Yes: {water}" if water == 'Yes' else "No: Water"])

        if laundry_in_unit == 'yes' and laundry_in_building == 'no' and dishwasher == 'no':
            appliances = 'Laundry (In Unit)'
        elif laundry_in_unit == 'no' and laundry_in_building == 'yes' and dishwasher == 'no':
            appliances = 'Laundry (In Building)'
        elif laundry_in_unit == 'no' and laundry_in_building == 'no' and dishwasher == 'yes':
            appliances = 'Dishwasher'
        elif laundry_in_unit == 'yes' and laundry_in_building == 'yes' and dishwasher == 'no':
            appliances = 'Laundry (In Unit), Laundry (In Building)'
        elif laundry_in_unit == 'yes' and laundry_in_building == 'no' and dishwasher == 'yes':
            appliances = 'Laundry (In Unit), Dishwasher'
        elif laundry_in_unit == 'no' and laundry_in_building == 'yes' and dishwasher == 'yes':
            appliances = 'Laundry (In Building), Dishwasher'
        elif laundry_in_unit == 'yes' and laundry_in_building == 'yes' and dishwasher == 'yes':
            appliances = 'Laundry (In Unit), Laundry (In Building), Dishwasher'
        else:
            appliances = 'Not included'

        # Construct feature vectors
        input_data = {
            'Latitude': latitude,
            'Longitude': longitude,
            'Type': Type,
            'Bedroom': bedroom,
            'Bathroom': bathroom,
            'Utilities_Included': utilities_included,
            'Wi_Fi_and_More': wi_fi_and_more,
            'Parking_Included': parking_included,
            'Agreement_Type': agreement_type,
            'Move_In_Date': move_in_date,
            'Pet_Friendly': pet_friendly,
            'Size_sqft': size_sqft,
            'Furnished': furnished,
            'Appliances': appliances,
            'Air_Conditioning': air_conditioning,
            'Personal_Outdoor_Space': personal_outdoor_space,
            'Smoking_Permitted': smoking_permitted
        }

        # Make the price prediction
        X = pd.DataFrame(input_data, index=[0])
        predicted_price = model_loaded.predict(X)

        # Returns the prediction result
        return jsonify(predicted_price.tolist()[0])

    except ValueError:
        return jsonify({'error': 'The entered data format is incorrect. Please try again.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,ssl_context=('/www/wwwroot/test/www.ksjzs.com.pem', '/www/wwwroot/test/www.ksjzs.com.key'))
