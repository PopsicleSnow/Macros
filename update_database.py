import sqlite3
from locations import locations
from menu import menu

for loc in locations():
    dishes = menu(loc)

    con = sqlite3.connect("menu.db")
    cur = con.cursor()

    cur.execute(f"CREATE TABLE IF NOT EXISTS {loc} (mealperiod TEXT, category TEXT, name TEXT, calories REAL, fat REAL, carbs REAL, protein REAL, sugar REAL, servingSize TEXT)")
    cur.execute(f"DELETE FROM {loc};")
    for mealperiod in dishes:
        for dish in dishes[mealperiod]:
            cur.execute("""
                INSERT INTO {} (mealperiod, category, name, calories, fat, carbs, protein, sugar, servingSize)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                """.format(loc), (
                    mealperiod, 
                    dishes[mealperiod][dish]["category"], 
                    dish, 
                    dishes[mealperiod][dish]["Calories (kcal)"], 
                    dishes[mealperiod][dish]["Total Lipid/Fat (g)"], 
                    dishes[mealperiod][dish]["Carbohydrate (g)"], 
                    dishes[mealperiod][dish]["Protein (g)"], 
                    dishes[mealperiod][dish]["Sugar (g)"],
                    dishes[mealperiod][dish]["servingSize"]
            ))
            con.commit() 