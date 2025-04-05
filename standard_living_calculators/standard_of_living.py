import matplotlib.pyplot as plt
import io
import base64
import inflect

def calculate_standard_of_living(data):
    try:
        current_expense = float(data.get("current_expense", 0))
        inflation_rate = float(data.get("inflation_rate", 0))
        years = int(data.get("years", 0))
        include_dependability = data.get("include_dependability", False)
        additional_expenses = data.get("additional_expenses", [])

        p = inflect.engine()
        yearly_expenses = []

        for year in range(1, years + 1):
            adjusted_expense = current_expense * ((1 + inflation_rate / 100) ** year)

            # Add optional dependability expenses
            if include_dependability and additional_expenses:
                for item in additional_expenses:
                    if int(item.get("year", 0)) == year:
                        adjusted_expense += float(item.get("amount", 0))

            yearly_expenses.append({
                "year": year,
                "expense_numeric": round(adjusted_expense, 2),
                "expense_words": p.number_to_words(round(adjusted_expense, 2)) + " rupees"
            })

        # Plotting
        years_list = [x["year"] for x in yearly_expenses]
        values_list = [x["expense_numeric"] for x in yearly_expenses]

        plt.figure(figsize=(10, 5))
        plt.plot(years_list, values_list, marker='o', linestyle='-', color='teal')
        plt.title("Future Cost of Living Adjusted for Inflation")
        plt.xlabel("Year")
        plt.ylabel("Estimated Annual Expense (₹)")
        plt.grid(True)

        # Save plot to base64 string
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png')
        img_bytes.seek(0)
        base64_image = base64.b64encode(img_bytes.read()).decode('utf-8')
        plt.close()

        return {
            "expenses": yearly_expenses,
            "chart_base64": base64_image
        }

    except Exception as e:
        return {"error": str(e)}
