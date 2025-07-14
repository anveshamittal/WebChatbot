import csv

def fetch_data():
    with open("data.csv", newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader) 
        return [f"{row[0]}: {row[1]}" for row in reader]

docs = fetch_data()
