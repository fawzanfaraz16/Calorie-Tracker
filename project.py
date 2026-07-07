import csv
import re
from datetime import datetime

food_db = "food_database.csv"
daily_log = "daily_log.csv"
alltime_log = "alltime_log.csv"

macros = ["calories", "protein","carbs", "sugars", "fat", "saturates", "fibre", "salt"]
req_macros = ["calories", "protein", "carbs"]
errorcatcher = r"(?:\d+(?:\.\d*)?|\.\d+)"

def calculating_macros(nutrition, grams):
    return {key: round((grams/100) * value, 2) for key , value in nutrition.items()}

def food_name(name):
    name = name.strip().lower()
    if name.endswith("s") and not name.endswith("us") and not name.endswith("ss"):
        name = name[:-1]
    return name

def parsing(value, blank=False):
    value = value.strip()

    if value == "" and blank:
        return None
    if value == "":
        raise ValueError("Input Cannot be Blank")
    if not re.fullmatch(errorcatcher, value):
        raise ValueError("Input Cannot have Special Characters")

    return float(value)

def load_csv(file):
    try:
        with open(file, "r", newline="") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []

def save_csv(file, fieldnames, rows, append=False):
    header = True

    if append:
        try:
            with open(file, "r", newline="") as file:
                header = file.read(1) == ""
        except FileNotFoundError:
            header = True

    mode = "a" if append else "w"

    with open(file, mode, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if header:
            writer.writeheader()

        writer.writerows(rows)

def main():
    foods = load_csv(food_db)
    daily_entries = load_csv(daily_log)

    print("CALORIE TRACKER")

    while True:
        print("\nOptions: [LOG], [VIEW], [DATABASE], [RESET], [EXIT]")
        choice = input("Select an input: ").strip().lower()

        if choice == "exit":
            print("See you next time!")
            break

        elif choice == "database":
            if not foods:
                print("\nFood Database is empty.")
            else:
                print("\nSaved Foods:")
                for food in sorted(foods, key=lambda row: row["name"].lower()):
                    print(f"-{food['name']}")

        elif choice == "view":
            if not daily_entries:
                print("\nNo food logged today.")
                continue
            totals = {key: 0.0 for key in macros}
            print("\nToday's Food Log")

            for index, entry in enumerate(daily_entries, 1):
                print(f"{index}, {entry['food']} - {entry['grams']}g")
                print(f"Calories: {entry['calories']} |" f"Protein: {entry['protein']}g | " f"Carbs: {entry['carbs']}g")

                for key in macros:
                    totals[key] += float(entry.get(key, 0) or 0)

            totals = {key: round(value,2) for key, value in totals.items()}
            print("Daily Totals")
            print(f"Calories: {totals['calories']}")
            print(f"Protein: {totals['protein']}g")
            print(f"Carbs: {totals['carbs']}g")
            print(f"Fat: {totals['fat']}g")
            print(f"Sugars: {totals['sugars']}g")
            print(f"Fibre: {totals['fibre']}g")
            print(f"Salt: {totals['salt']}g")

        elif choice == "reset":
            totals = {key: 0.0 for key in macros}

            for entry in daily_entries:
                for key in macros:
                    totals[key] += float(entry.get(key, 0) or 0)

            totals = {key: round(value, 2) for key, value in totals.items()}
            if any(value > 0 for value in totals.values()):
                history_row = {"timestamp" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), **totals}

                save_csv(alltime_log, ["timestamp"] + macros, [history_row], append=True)
                print("Daily totals saved into history")
            else:
                print("Nothing to save")

            daily_entries = []
            save_csv(daily_log, ["food", "grams"] + macros, daily_entries)
            print("Daily Log Reset")

        elif choice == "log":
            f_name = input("\nWhat is the food? ").strip()

            if not f_name:
                print("Food name cannot be empty.")
                continue

            normal_input = food_name(f_name)
            existing_food = None

            for food in foods:
                if food_name(food["name"]) == normal_input:
                    existing_food = food
                    break

            if existing_food:
                print(f"Found {existing_food['name']} in database.")

                nutrition = {key: float(existing_food.get(key, 0) or 0) for key in macros}

            else:
                print(f"'{f_name}' not found. Add Nutritional values per 100g")

                nutrition = {}

                for key in macros:
                    while True:
                        try:
                            if key in req_macros:
                                value = input(f"{key.capitalize()}: ")
                                nutrition[key] = parsing(value)

                            else:
                                value = input(f"{key.capitalize()} optional, press Enter to skip: ")
                                result = parsing(value, blank = True)
                                nutrition[key] = 0.0 if result is None else result
                            break
                        except ValueError as error:
                            print(error)

                new_food = {"name": f_name, **nutrition}
                foods.append(new_food)
                save_csv(food_db, ["name"] + macros, foods)
                print(f"'{f_name}' saved to database")

            while True:
                try:
                    grams = parsing(input("How many grams did you eat? "))

                    if grams <= 0:
                        print("Grams must be greater than 0")
                        continue
                    break
                except ValueError as error:
                    print(error)

            calculated = calculating_macros(nutrition, grams)

            log_entry = {
                "food": existing_food["name"] if existing_food else f_name,
                "grams": grams,
                **calculated
            }

            daily_entries.append(log_entry)
            save_csv(daily_log, ["food", "grams"] + macros, daily_entries)

            print(f"Logged {grams}g of {log_entry['food']}:")
            print(
                f"Calories: {calculated['calories']} | "
                f"Protein: {calculated['protein']}g | "
                f"Carbs: {calculated['carbs']}g"
            )
        else:
            print("Invalid option. Choose Log, View, Database, Reset or Exit.")

if __name__ == "__main__":
    main()


