import sqlite3

def query(mealperiod, location):
    con = sqlite3.connect("menu.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM {location} WHERE mealperiod = ?;", (mealperiod,))
    result = cur.fetchall()
    cur.close()
    con.close()
    return result

#print(query("Breakfast - Spring", "Foothill"))