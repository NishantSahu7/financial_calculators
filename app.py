from flask import Flask, request, jsonify
from flask_cors import CORS
from standard_living_calculators.standard_of_living import calculate_standard_of_living

app = Flask(__name__)
CORS(app)

@app.route("/calculate_standard_of_living", methods=["POST"])  # ✅ Correct route
def calculate():
    data = request.get_json()  # Ensure JSON data is received
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400  # Handle missing JSON case

    result = calculate_standard_of_living(data)
    return jsonify(result)

if __name__ == "__main__":
    print("Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(rule)  # ✅ Debugging: Check if the correct route is listed
    app.run(debug=True, port=5001)

