import requests
from flask import Flask, redirect, url_for, render_template, jsonify, request
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")



inst_data = {
    
    "Calories": 0,
    "Protein": 0,
    "Sugar": 0,
    "Fats": 0,
    "Fiber": 0,
    "Carbs": 0
}

goal_data = {
    
    "Calories": 0,
    "Protein": 0,
    "Sugar": 0,
    "Fats": 0,
    "Fiber": 0,
    "Carbs": 0
}

aim_data = {
    
    "Calories": 0,
    "Protein": 0,
    "Sugar": 0,
    "Fats": 0,
    "Fiber": 0,
    "Carbs": 0
}

@app.route("/parse")
def parse(file):

    
    inst_data["Calories"] = int(file[0]["calories"])
    inst_data["Protein"] = int(file[0]["protein_g"])
    inst_data["Sugar"] = int(file[0]["sugar_g"])
    inst_data["Fats"] = int(file[0]["fat_total_g"])
    inst_data["Fiber"] = int(file[0]["fiber_g"])
    inst_data["Carbs"] = int(file[0]["carbohydrates_total_g"])

    goal_data["Calories"] += int(file[0]["calories"])
    goal_data["Protein"] += int(file[0]["protein_g"])
    goal_data["Sugar"] += int(file[0]["sugar_g"])
    goal_data["Fats"] += int(file[0]["fat_total_g"])
    goal_data["Fiber"] += int(file[0]["fiber_g"])
    goal_data["Carbs"] += int(file[0]["carbohydrates_total_g"])

    
    return render_template("index.html", curr_calories = goal_data["Calories"], aim_calories = aim_data["Calories"])

# "index.html", curr_calories = goal_data["Calories"], curr_protein = goal_data["Protein"], curr_fat = goal_data["Fats"], curr_carbs = goal_data["Carbs"], curr_sugar = goal_data["Sugar"], curr_fiber = goal_data["Fiber"]

@app.route("/reset", methods=["POST"])
def reset_values():
    
    goal_data["Calories"] = 0
    goal_data["Protein"] = 0
    goal_data["Sugar"] = 0
    goal_data["Fats"] = 0
    goal_data["Fiber"] = 0
    goal_data["Carbs"] = 0
    
    return render_template("index.html")


@app.route("/aimset", methods=['GET', 'POST'])
def aimset():
    
    aim_data["Calories"] = int(request.form["calorieName"])
    aim_data["Protien"] = int(request.form["proteinName"])
    aim_data["Fats"] = int(request.form["fatName"])
    aim_data["Sugar"] = int(request.form["sugarName"])
    aim_data["Fiber"] = int(request.form["fiberName"])
    aim_data["Carbs"] = int(request.form["carbsName"])
    
    return render_template("index.html", aim_calories = aim_data["Calories"], aim_protein = aim_data["Protein"], aim_fat = aim_data["Fats"], aim_carbs = aim_data["Carbs"], aim_sugar = aim_data["Sugar"], aim_fiber = aim_data["Fiber"])


@app.route('/data', methods=['POST'])
def get_api_response():
    
    url = "https://nutrition-by-api-ninjas.p.rapidapi.com/v1/nutrition"

    querystring = {"query":request.form['addFood']}

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
            return parse(response.json())
        else:
            # Return an error message if the request failed
            return jsonify({'error': 'Failed to fetch data from the API'}), response.status_code
        
    except Exception as e:
        # Handle exceptions
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)