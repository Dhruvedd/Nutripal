import requests
from flask import Flask, redirect, url_for, render_template, jsonify, request
import json

app = Flask(__name__)

@app.route("/")
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

@app.route("/logsub", methods=["POST"])
def set_curr():
    uname = request.form["username"],
    passw = request.form["password"]
    
    truth = login(uname,passw)
    
    if(truth):
        current_user["username"] = uname
        current_user["password"] = passw
        return render_template("login.html", bool=True)
    
    else: return render_template("login.html", bool=True)



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
    
   #  prompt = str('''
   #  You are a professional nutritionist and dietician. 
   #  I will tell you my daily nutrition goals and my end of day progress. 
   #  Reccomend me meals to eat more based on them. 
   #  My Calories Goal for the day was " ''' + str(aim_data["Calories"]) + ''' and my progress at the 
   #  end of the was "''' + str(goal_data["Calories"]) + ". My Protein Goal for the day was " + str(aim_data["Protein"]) + '''
   #  " and my progress at the end of the was "''' + str(goal_data["Protein"]) + '''". My Fats Goal for 
   #  the day was "''' + str(aim_data["Fats"]) + '''" and my progress at the end of the was "''' + str(goal_data["Fats"]) + '''
   #  ". My Sugar Goal for the day was "''' + str(aim_data["Sugar"]) + '''" 
   #  and my progress at the end of the was "''' + str(goal_data["Sugar"]) + '''
   #  ". My Fiber Goal for the day was "''' + str(aim_data["Fiber"]) + '''
   #  " and my progress at the end of the was "''' + str(goal_data["Fiber"]) + '''
   #  ". My Carbs Goal for the day was "''' + str(aim_data["Carbs"]) + '''
   #  " and my progress at the end of the was "''' + str(goal_data["Carbs"]) + '''". 
   #  use this data to reccomend me what I should eat. Keep your response very short and concise" 
   #  ''')
    
     prompt="write 2 words"
     
     return render_template("Web.html", content = get_responses(prompt))

if __name__ == "__main__":
    app.run(debug=True)
