import os
import requests
import csv
import secrets
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_city_name(pincode):
    api_url = "https://api.postalpincode.in/pincode/"
    response = requests.get(api_url + pincode)
    
    if response.status_code == 200:
        data = response.json()
        
        if data[0]['Status'] == 'Success':
            city_name = data[0]['PostOffice'][0]['District']
            return city_name
        else:
            return "City not found"
    else:
        return "API request failed"

@app.route("/", methods=["GET", "POST"])
def index():
    random_filename = None  # Initialize to None

    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file:
            # Generate a random filename for the output CSV file
            random_filename = secrets.token_hex(16) + ".csv"
            file_path = os.path.join("static", random_filename)

            with open(file_path, "w", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["PIN Code", "City Name"])  # Write header row
                for line in uploaded_file:
                    input_pincode = line.decode("utf-8").strip()
                    city_name = get_city_name(input_pincode)
                    csv_writer.writerow([input_pincode, city_name])

    return render_template("index.html", random_filename=random_filename)

if __name__ == "__main__":
    app.run(debug=True)
