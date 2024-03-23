import requests
from flask import Flask, redirect, url_for, render_template, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("Web.html")



all_data = {
    
    "Calories": 0,
    "Protein": 0,
    "Sugar": 0,
    "Fats": 0,
    "Fiber": 0
}

@app.route("/parse")
def parse(file):
    
    
    
    
    
    
    return render_template("Web.html", content=file)



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