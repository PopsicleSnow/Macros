import sqlite3
from locations import locations
from menu import menu

# Connect to the database
con = sqlite3.connect("menu.db")
cur = con.cursor()

for loc in locations():
    dishes = menu(loc)

    # Creat table if not exists and delete all records
    cur.execute(f"CREATE TABLE IF NOT EXISTS {loc} (mealperiod TEXT, category TEXT, name TEXT, calories REAL, fat REAL, carbs REAL, protein REAL, sugar REAL, servingSize TEXT)")
    cur.execute(f"DELETE FROM {loc};")

    # Prepare data for bulk insert
    data_to_insert = []
    for mealperiod in dishes:
        for dish in dishes[mealperiod]:
            data_to_insert.append((
                    mealperiod, 
                    dishes[mealperiod][dish]["category"], 
                    dish.strip(), 
                    dishes[mealperiod][dish]["Calories (kcal)"], 
                    dishes[mealperiod][dish]["Total Lipid/Fat (g)"], 
                    dishes[mealperiod][dish]["Carbohydrate (g)"], 
                    dishes[mealperiod][dish]["Protein (g)"], 
                    dishes[mealperiod][dish]["Sugar (g)"],
                    dishes[mealperiod][dish]["servingSize"]
            ))

    # Use a transaction for the insert operations
    cur.executemany(f"""
        INSERT INTO {loc} (mealperiod, category, name, calories, fat, carbs, protein, sugar, servingSize)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data_to_insert)
    
    con.commit()

con.close()