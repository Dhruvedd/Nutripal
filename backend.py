import requests
from flask import Flask, redirect, url_for, render_template, jsonify, request
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("Web.html")



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

    
    return render_template("Web.html", content=goal_data)


@app.route("/reset", methods=['GET', 'POST'])
def reset_values():
    
    goal_data["Calories"] = 0
    goal_data["Protein"] = 0
    goal_data["Sugar"] = 0
    goal_data["Fats"] = 0
    goal_data["Fiber"] = 0
    goal_data["Carbs"] = 0
    
    return render_template("Web.html", content=goal_data)


@app.route("/generate", methods=['GET', 'POST'])
def generate():
    pass


@app.route('/data', methods=['POST'])
def get_api_response():
    
    url = "https://nutrition-by-api-ninjas.p.rapidapi.com/v1/nutrition"

    querystring = {"query":request.form['input']}

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