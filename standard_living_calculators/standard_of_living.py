import inflect
import matplotlib.pyplot as plt
import base64
from io import BytesIO

from standard_living_calculators.utils.inflation_calculator import calculate_standard_of_living

def convert_to_words(amount):
    p = inflect.engine()
    if amount == 0:
        return "zero rupees"
    amount = round(amount, 2)
    int_part = int(amount)
    decimal_part = int(round((amount - int_part) * 100))
    words = p.number_to_words(int_part)
    if decimal_part > 0:
        words += " point " + p.number_to_words(decimal_part)
    return words + " rupees"

def generate_chart(data):
    years = [item["year"] for item in data]
    expenses = [item["expense_numeric"] for item in data]

    plt.figure(figsize=(10, 6))
    plt.plot(years, expenses, marker='o', color='#2b8dbd')
    plt.title("Projected Yearly Expenses")
    plt.xlabel("Year")
    plt.ylabel("Expense (INR)")
    plt.grid(True)

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    plt.close()
    return img_base64

def calculate_standard_of_living_response(
    initial_expense,
    inflation_rate,
    years,
    dependability_cost=None,
    dependability_from_year=None,
    life_event_cost=None,
    life_event_year=None,
):
    try:
        projection = calculate_standard_of_living(
            initial_expense,
            inflation_rate,
            years,
            dependability_cost,
            dependability_from_year,
            life_event_cost,
            life_event_year,
        )
        result = []
        for year, expense in enumerate(projection, start=1):
            result.append({
                "year": year,
                "expense_numeric": round(expense, 2),
                "expense_words": convert_to_words(expense)
            })
        chart_base64 = generate_chart(result)
        return {
            "expenses": result,
            "chart_base64": chart_base64,
        }
    except Exception as e:
        return {"error": str(e)}
