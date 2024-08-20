import csv

def read_coefficients_from_csv(file_path):
    area_to_coefficient = {}
    with open(file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            area = float(row['Area'])
            coefficient = float(row['Coefficient'])
            area_to_coefficient[area] = coefficient
    return area_to_coefficient

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

details = calculate_pricing(areas, first_price_per_sqm, coefficients_dict)

for detail in details:
    print(f"Area: {detail['Area']} sqm, Coefficient: {detail['Coefficient']}, "
          f"Price per Sqm: {detail['Price per Sqm']:.2f} Tenge, SCO: {detail['SCO']}, "
          f"Check: {detail['Check']:.2f} Tenge")
