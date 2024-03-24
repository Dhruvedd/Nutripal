import requests
from flask import Flask, redirect, url_for, render_template, jsonify, request
import json

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("index.html")

import data_storing
from data_storing import *
import ai
from ai import *

import firebase
from firebase import *


current_user = {
    "username":None,
    "password":None
}

@app.route("/logload")
def load():
    return render_template("login.html")

@app.route("/loadInd/")
def loadInd():
    return render_template("index.html")

from flask import request, jsonify

@app.route("/logsub", methods=["POST"])
def set_curr():
    try:
       
        uname = request.form["username",False]
        passw = request.form["password", False]
        truth = login(uname, passw)
        if not truth:
            current_user["username"] = uname
            current_user["password"] = passw
            return render_template("login.html", bool=False)
        
        else: render_template("index.html")
           
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    

@app.route("/look/", methods=['GET', 'POST'])
def look():
    url = "https://nutrition-by-api-ninjas.p.rapidapi.com/v1/nutrition"

    querystring = {"query":request.form['inp']}

    headers = {
	"X-RapidAPI-Key": "77b988d7b0mshe29695b4b1b70e4p143e3cjsnf8aebb0e1e9d",
	"X-RapidAPI-Host": "nutrition-by-api-ninjas.p.rapidapi.com"
    }

    try:
        # Make a request to the API
        response = requests.get(url, headers=headers, params=querystring)

        # Check if the request was successful
        if response.status_code == 200:
            # Process the API response
            return parse2(response.json())
        else:
            # Return an error message if the request failed
            return jsonify({'error': 'Failed to fetch data from the API'}), response.status_code
        
    except Exception as e:
        # Handle exceptions
        return jsonify({'error': str(e)}), 500
    
    
    
    
    


def parse2(file):
    
    inst_data["Calories"] = int(file[0]["calories"])
    inst_data["Protein"] = int(file[0]["protein_g"])
    inst_data["Sugar"] = int(file[0]["sugar_g"])
    inst_data["Fats"] = int(file[0]["fat_total_g"])
    inst_data["Fiber"] = int(file[0]["fiber_g"])
    inst_data["Carbs"] = int(file[0]["carbohydrates_total_g"])
    
    input = request.form["inp"]
    
    return render_template("searchFood.html",inp = input, cal = inst_data["Calories"], pro = inst_data["Protein"], sug = inst_data["Sugar"], fat = inst_data["Fats"], fib = inst_data["Fiber"], car = inst_data["Carbs"])

@app.route("/rec/", methods=['GET', 'POST'])
def rec():
    return render_template("recommendations.html")



@app.route("/nutri/", methods=['GET', 'POST'])
def nutri():
    return render_template("searchFood.html")




@app.route("/data")
def api_run():
    return get_api_response()

@app.route("/reset")
def resethere():
    return reset_values()

@app.route("/aimset")
def aimsethere():
    return aimset()

#new functions start here

@app.route("/generate", methods=['GET', 'POST'])
def generate():
    
   prompt = str('''
   You are a professional nutritionist and dietician. 
   I will tell you my daily nutrition goals and my end of day progress. 
   Reccomend me meals to eat more based on them. 
   My Calories Goal for the day was " ''' + str(aim_data["Calories"]) + ''' and my progress at the 
   end of the was "''' + str(goal_data["Calories"]) + ". My Protein Goal for the day was " + str(aim_data["Protein"]) + '''
   " and my progress at the end of the was "''' + str(goal_data["Protein"]) + '''". My Fats Goal for 
   the day was "''' + str(aim_data["Fats"]) + '''" and my progress at the end of the was "''' + str(goal_data["Fats"]) + '''
   ". My Sugar Goal for the day was "''' + str(aim_data["Sugar"]) + '''" 
   and my progress at the end of the was "''' + str(goal_data["Sugar"]) + '''
   ". My Fiber Goal for the day was "''' + str(aim_data["Fiber"]) + '''
   " and my progress at the end of the was "''' + str(goal_data["Fiber"]) + '''
   ". My Carbs Goal for the day was "''' + str(aim_data["Carbs"]) + '''
   " and my progress at the end of the was "''' + str(goal_data["Carbs"]) + '''". 
   use this data to reccomend me what I should eat. Keep your response very short and concise" 
   ''')
    
     
     
   con = get_responses(prompt)
   return render_template("recommendations.html", content=con)

if __name__ == "__main__":
    app.run(debug=True)
