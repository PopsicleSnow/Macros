import sqlite3

def query(mealperiod, location):
    con = sqlite3.connect("menu.db")
    cur = con.cursor()
    cur.execute(f"SELECT mealperiod, category, name, calories, fat, carbs, protein, sugar, servingSize FROM {location} WHERE mealperiod = ?;", (mealperiod,))
    result = cur.fetchall()
    cur.close()
    con.close()
    return result

#print(query("Breakfast - Spring", "Foothill"))