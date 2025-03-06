import requests
from flask import Flask, redirect, url_for, render_template, jsonify, request
import json

import backend

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("login.html")

inst_data = {
    "Sugar": 0,
    "Fats": 0,
    "Fiber": 0,
    "Carbs": 0
}

goal_data = {
    "Sugar": 0,
    "Fats": 0,
    "Fiber": 0,
    "Carbs": 0
}

aim_data = {
    "Sugar": 0,
    "Fats": 0,
    "Fiber": 0,
    "Carbs": 0
}

def parse(file):
    inst_data["Sugar"] = int(file[0]["sugar_g"])
    inst_data["Fats"] = int(file[0]["fat_total_g"])
    inst_data["Fiber"] = int(file[0]["fiber_g"])
    inst_data["Carbs"] = int(file[0]["carbohydrates_total_g"])

    goal_data["Sugar"] += int(file[0]["sugar_g"])
    goal_data["Fats"] += int(file[0]["fat_total_g"])
    goal_data["Fiber"] += int(file[0]["fiber_g"])
    goal_data["Carbs"] += int(file[0]["carbohydrates_total_g"])

    return render_template("index.html",
                           curr_fat=goal_data["Fats"], 
                           curr_carbs=goal_data["Carbs"], 
                           curr_sugar=goal_data["Sugar"], 
                           curr_fiber=goal_data["Fiber"], 
                           aim_fat=aim_data["Fats"], 
                           aim_carbs=aim_data["Carbs"], 
                           aim_sugar=aim_data["Sugar"], 
                           aim_fiber=aim_data["Fiber"])

@app.route("/reset", methods=["POST"])
def reset_values():
    goal_data["Sugar"] = 0
    goal_data["Fats"] = 0
    goal_data["Fiber"] = 0
    goal_data["Carbs"] = 0

    return render_template("index.html")

@app.route("/aimset", methods=['POST'])
def aimset():
    required_fields = ["fatName", "sugarName", "fiberName", "carbsName"]
    
    for field in required_fields:
        if field not in request.form:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        aim_data["Fats"] = int(request.form["fatName"])
        aim_data["Sugar"] = int(request.form["sugarName"])
        aim_data["Fiber"] = int(request.form["fiberName"])
        aim_data["Carbs"] = int(request.form["carbsName"])
    except ValueError:
        return jsonify({"error": "Invalid input. Please enter numeric values."}), 400
    
    return render_template("index.html", 
                           aim_fat=aim_data["Fats"], 
                           aim_carbs=aim_data["Carbs"], 
                           aim_sugar=aim_data["Sugar"], 
                           aim_fiber=aim_data["Fiber"])

@app.route('/data', methods=['POST'])
def get_api_response():
    url = "https://nutrition-by-api-ninjas.p.rapidapi.com/v1/nutrition"

    querystring = {"query": request.form['addFood']}

    headers = {
        "X-RapidAPI-Key": "77b988d7b0mshe29695b4b1b70e4p143e3cjsnf8aebb0e1e9d",
        "X-RapidAPI-Host": "nutrition-by-api-ninjas.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            return parse(response.json())
        else:
            return jsonify({'error': 'Failed to fetch data from the API'}), response.status_code
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
