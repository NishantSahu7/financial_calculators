from flask import Blueprint, request, jsonify
from utils.inflation_calculator import calculate_standard_of_living
from utils.chart_generator import generate_chart

standard_of_living_bp = Blueprint('standard_of_living', __name__)

@standard_of_living_bp.route('/standard_of_living', methods=['POST'])
def standard_of_living():
    try:
        data = request.get_json(force=True)
        print("🔥 Raw Incoming Data from Frontend:", data)

        # Safely parse numeric fields
        initial_expense = float(data.get("initial_expense", 0) or 0)
        inflation_rate = float(data.get("inflation_rate", 0) or 0)
        years = int(data.get("years", 0) or 0)

        dependability_amount = float(data.get("dependability_amount", 0) or 0)
        dependability_year = int(data.get("dependability_year", 0) or 0)

        life_event_amount = float(data.get("life_event_amount", 0) or 0)
        life_event_year = int(data.get("life_event_year", 0) or 0)

        print("✅ Parsed Values:", {
            "initial_expense": initial_expense,
            "inflation_rate": inflation_rate,
            "years": years,
            "dependability_amount": dependability_amount,
            "dependability_year": dependability_year,
            "life_event_amount": life_event_amount,
            "life_event_year": life_event_year
        })

        # Perform calculation
        expenses = calculate_standard_of_living(
            initial_expense,
            inflation_rate,
            years,
            dependability_amount,
            dependability_year,
            life_event_amount,
            life_event_year
        )

        # Generate chart
        chart_base64 = generate_chart(expenses)

        return jsonify({
            "expenses": expenses,
            "chart_base64": chart_base64
        })

    except Exception as e:
        print("❌ Exception:", str(e))
        return jsonify({"error": str(e)}), 500
