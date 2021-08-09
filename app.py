from flask import Flask, render_template, request
import pickle

app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Year = 2021 - Year
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        max_p = float(request.form['Max_power'])
        # Kms_Driven2 = np.log(Kms_Driven)
        Owner = int(request.form['Owner'])
        mileage = float(request.form['mile'])
        Engine = int(request.form['engine'])
        Seats = int(request.form['seat'])
        Gear_Box = int(request.form['gear'])

        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']

        if Fuel_Type_Petrol == 'Petrol':
            Fuel_Petrol = 1
            Fuel_Diesel = 0
            Fuel_Electric = 0

        elif Fuel_Type_Petrol == 'Diesel':
            Fuel_Petrol = 0
            Fuel_Diesel = 1
            Fuel_Electric = 0
        elif Fuel_Type_Petrol == 'Electric':
            Fuel_Petrol = 0
            Fuel_Diesel = 0
            Fuel_Electric = 1
        else:
            Fuel_Petrol = 0
            Fuel_Diesel = 0
            Fuel_Electric = 0

        Seller_Type = request.form['Seller_Type_Individual']
        if Seller_Type == 'Individual':
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0

        Transmission_manual = request.form['Transmission_Manual']
        if Transmission_manual == 'Manual':
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0

        prediction = model.predict([[Year, Present_Price, Kms_Driven, max_p, Owner, mileage, Engine, Seats, Gear_Box,
                                     Fuel_Diesel, Fuel_Electric, Fuel_Petrol, Seller_Type_Individual,
                                     Transmission_Manual]])
        output = round(prediction[0], 2)
        if output < 0:
            return render_template('index.html', prediction_texts="Sorry, You can't sell this car")
        else:
            return render_template('index.html', prediction_text="You Can Sell this Car at {} Lakh INR".format(output))
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
