import pandas as pd

def read_coefficients_from_csv(file_path):
    df = pd.read_csv(file_path)
    df['Area'] = df['Area'].astype(float)
    df['Coefficient'] = df['Coefficient'].astype(float)
    return df.set_index('Area')['Coefficient'].to_dict()

def calculate_pricing(areas, first_price_per_sqm, coefficients_dict):
    details_df = pd.DataFrame({'Area': areas})
    details_df['Coefficient'] = details_df['Area'].map(coefficients_dict).fillna(1)
    details_df['Price per Sqm'] = first_price_per_sqm - (details_df['Coefficient'].diff().fillna(0) * 100000)
    details_df['SCO'] = (details_df['Price per Sqm'] / 1000).round()
    details_df['Check'] = details_df['SCO'] * details_df['Area'] * 1000
    return details_df

def calculate_pricing(areas, first_price_per_sqm, coefficients_dict):
    details = []
    prices_per_sqm = []

    prev_price_per_sqm = first_price_per_sqm

    for index, area in enumerate(areas):
        current_coefficient = coefficients_dict.get(area, 1)
        
        if index == 0:
            new_price_per_sqm = prev_price_per_sqm
        else:
            prev_coefficient = coefficients_dict[areas[index - 1]]
            new_price_per_sqm = prev_price_per_sqm - (prev_coefficient - current_coefficient) * 100000

        prices_per_sqm.append(new_price_per_sqm)

        sco = round(new_price_per_sqm / 1000)
        check = sco * area * 1000
        area_detail = {
            "Area": area,
            "Coefficient": current_coefficient,
            "Price per Sqm": new_price_per_sqm,
            "SCO": sco,
            "Check": check
        }
        details.append(area_detail)

        prev_price_per_sqm = new_price_per_sqm

    return details

# кф табличные значения с листа 2
coefficients_file_path = 'coef.csv'

coefficients_dict = read_coefficients_from_csv(coefficients_file_path)

# вводные данные для расчета
areas = [41, 71, 102, 130]
first_price_per_sqm = 323000

details_df = calculate_pricing(areas, first_price_per_sqm, coefficients_dict)

print(details_df)

details_df = pd.DataFrame(details_df)
details_df.to_csv('detailed_prices_checks.csv', index=False)