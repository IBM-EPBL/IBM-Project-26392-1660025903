import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import requests
 

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "nIcDWag7yja9PWWeQAzOwPuVwVPLeFld__lfNckqWrH7"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__)


#model = joblib.load('F:\Predicting-The-Energy-Output-Of-Wind-Turbine-Based-On-Weather-Condition-master\Predicting-The-Energy-Output-Of-Wind-Turbine-Based-On-Weather-Condition-master\power_prediction.sav')

@app.route('/')
def home():
    return render_template('intro.html')
@app.route('/predict')
def predict():
    return render_template('predict.html')
@app.route('/windapi',methods=['POST'])
def windapi():
    city=request.form.get('city')
    apikey="304ac14164205d26c60e89be889af461"
    url="http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+apikey
    resp = requests.get(url)
    resp=resp.json()
    temp = str((resp["main"]["temp"])-273.15) +" °C"
    humid = str(resp["main"]["humidity"])+" %"
    pressure = str(resp["main"]["pressure"])+" mmHG"
    speed = str((resp["wind"]["speed"])*3.6)+" Km/s"
    return render_template('predict.html', temp=temp, humid=humid, pressure=pressure,speed=speed)   
@app.route('/y_predict',methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    x_test = [[float(x) for x in request.form.values()]]
    print(x_test)
    payload_scoring = {"input_data": 
			[{"field": [["Theoretical_Power_Curve (KWh)", "WindSpeed(m/s)"]], 
			"values": x_test}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/bd053e0e-aaa3-43c3-a8fa-a330e347613a/predictions?version=2022-11-12', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions =response_scoring.json()
    print(predictions)
    print('Final Prediction Result',predictions['predictions'][0]['values'][0][0])


    pred =response_scoring.json()
    print(pred)
    #print('Final Prediction Result',predictions['predictions'][0]['values'][0][0])

   # prediction = model.predict(x_test)
    print(pred)
    output = pred['predictions'][0]['values'][0][0]
    return render_template('predict.html', prediction_text='The energy predicted is {:.2f} KWh'.format(output))


if __name__ == "__main__":
    app.run(debug=False)
