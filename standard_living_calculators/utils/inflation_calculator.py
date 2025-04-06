def calculate_standard_of_living(initial_expense, inflation_rate, years, dependability_cost=None, dependability_start_year=None, life_event_cost=None, life_event_year=None):
    result = []

    for year in range(1, years + 1):
        # Inflate the previous year's expense
        if year == 1:
            expense = initial_expense * (1 + inflation_rate)
        else:
            expense = result[-1]['expense'] * (1 + inflation_rate)

        # Add dependability cost if this year matches
        if dependability_cost is not None and dependability_start_year is not None:
            if year >= dependability_start_year:
                expense += dependability_cost

        # Add life event cost if this year matches
        if life_event_cost is not None and life_event_year is not None:
            if year == life_event_year:
                expense += life_event_cost

        result.append({
            'year': year,
            'expense': round(expense, 2)
        })

    return result
