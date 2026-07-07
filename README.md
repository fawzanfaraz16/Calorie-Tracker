# Calorie Tracker

A command-line calorie and macro tracker built in Python. Log foods, build a personal food database, and track daily nutritional intake — all stored locally in CSV files.

## How It Works

The tracker runs in a loop with five commands:

- **Log** — Enter a food and how many grams you ate. If the food isn't in your database, you'll be prompted to add its nutritional values per 100g. Macros are then calculated proportionally to your serving size.
- **View** — Display everything logged today with a running total of all macros.
- **Database** — List all saved foods.
- **Reset** — Archive the current day's totals to an all-time history log and clear the daily log.
- **Exit** — Quit the program.

## Tracked Macros

Calories, protein, and carbs are required when adding a new food. The rest are optional:

Sugars · Fat · Saturates · Fibre · Salt

## Files

| File | Purpose |
|---|---|
| `project.py` | Main application logic |
| `test_project.py` | Unit tests (pytest) |
| `food_database.csv` | Persistent food database (generated at runtime) |
| `daily_log.csv` | Current day's food log (generated at runtime) |
| `alltime_log.csv` | Archived daily totals (generated at runtime) |

## Usage

```bash
python project.py
```

## Running Tests

```bash
pytest test_project.py
```

## Requirements

Python 3 — no external dependencies. Only `pytest` is needed to run tests:

```bash
pip install pytest
```
