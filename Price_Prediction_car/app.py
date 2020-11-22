from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
import sqlalchemy
import os
from model import Result
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists 
from config import Config
from connection import db
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))


app.config.from_object(Config)
db.init_app(app)
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI) 
if not database_exists(engine.url): 
    create_database(engine.url) 

with app.app_context():
    from model import *
    db.create_all()


@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
                fueltype= "petrol"
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
            fueltype= "diesel"
        Year=2020-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
            sellertype = "individual"
        else:
            Seller_Type_Individual=0
            sellertype = "dealer"	
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            transmission = "mannual"
            Transmission_Mannual=1
        else:
            transmission = "automatic"
            Transmission_Mannual=0
        prediction=model.predict([[Present_Price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            result_obj = Result(Year = str(Year),ShowroomPrice = str(Present_Price), Kilometers = str(Kms_Driven),FuelType = str(fueltype), Owners = str(Owner), SellerType = str(sellertype), TransmissionType = str(transmission), PredictedPrice = str(output))
            db.session.add(result_obj)
            db.session.commit()
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))       
    else:
        return render_template('index.html')


@app.route("/stored_data", methods=['GET'])
def stored_data():
    return None

@app.route("/introduction")
def introduction():
    return render_template('introduction.html')
if __name__=="__main__":
    app.run(host='0.0.0.0')
