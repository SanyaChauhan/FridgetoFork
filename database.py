import sqlite3

DB_NAME = "recipe_agent.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Pantry table - stores user's ingredients
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pantry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredient TEXT NOT NULL UNIQUE,
            quantity TEXT,
            added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Preferences table - stores user's dietary preferences
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            preference_type TEXT NOT NULL,
            value TEXT NOT NULL
        )
    ''')

    # History table - stores past recipes viewed
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_name TEXT NOT NULL,
            ingredients_used TEXT,
            viewed_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def add_ingredient(ingredient, quantity=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT OR REPLACE INTO pantry (ingredient, quantity) VALUES (?, ?)",
            (ingredient.lower().strip(), quantity)
        )
        conn.commit()
        return True
    except Exception as e:
        return False
    finally:
        conn.close()

def get_pantry():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT ingredient, quantity FROM pantry")
    items = cursor.fetchall()
    conn.close()
    return items

def remove_ingredient(ingredient):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pantry WHERE ingredient = ?", (ingredient.lower().strip(),))
    conn.commit()
    conn.close()

def clear_pantry():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pantry")
    conn.commit()
    conn.close()

def save_preference(preference_type, value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO preferences (preference_type, value) VALUES (?, ?)",
        (preference_type, value)
    )
    conn.commit()
    conn.close()

def get_preferences():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT preference_type, value FROM preferences")
    prefs = cursor.fetchall()
    conn.close()
    return prefs

def save_to_history(recipe_name, ingredients_used):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO history (recipe_name, ingredients_used) VALUES (?, ?)",
        (recipe_name, ingredients_used)
    )
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT recipe_name, ingredients_used, viewed_on FROM history ORDER BY viewed_on DESC LIMIT 10")
    history = cursor.fetchall()
    conn.close()
    return history

def clear_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()