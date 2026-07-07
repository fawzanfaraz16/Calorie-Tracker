import pytest
from project import calculating_macros, food_name, parsing, load_csv

def test_calculating_macros():
    nutrition = {"calories" : 200, "protein" : 10, "carbs": 30}

    result = calculating_macros(nutrition, 50)
    assert result["calories"] == 100
    assert result["protein"] == 5
    assert result["carbs"] == 15

def test_food_name():
    assert food_name(" chicken") == "chicken"
    assert food_name("PEACH") == "peach"
    assert food_name("hummus") == "hummus"

def test_parsing():
    assert parsing("100") == 100.0
    assert parsing(".5") == 0.5

    with pytest.raises(ValueError):
        parsing("")

def test_load_csv(tmp_path):
    missing_file = tmp_path / "missing.csv"
    assert load_csv(missing_file) == []

