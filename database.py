import sqlite3

def init_db():
    conn = sqlite3.connect('foodwaste.db')
    cursor = conn.cursor()

    # --- Users table (both restaurants and orphanages) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            email       TEXT UNIQUE NOT NULL,
            password    TEXT NOT NULL,
            role        TEXT NOT NULL CHECK(role IN ('restaurant', 'orphanage')),
            address     TEXT,
            phone       TEXT,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # --- FoodListings table ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS food_listings (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER NOT NULL,
            item_name     TEXT NOT NULL,
            quantity       TEXT NOT NULL,
            expiry_time   DATETIME NOT NULL,
            status        TEXT NOT NULL DEFAULT 'available'
                          CHECK(status IN ('available', 'claimed', 'expired')),
            notes         TEXT,
            created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (restaurant_id) REFERENCES users(id)
        )
    ''')

    # --- Claims table ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS claims (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            food_id        INTEGER NOT NULL,
            orphanage_id   INTEGER NOT NULL,
            claimed_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
            pickup_status  TEXT NOT NULL DEFAULT 'pending'
                           CHECK(pickup_status IN ('pending', 'picked_up', 'cancelled')),
            FOREIGN KEY (food_id)      REFERENCES food_listings(id),
            FOREIGN KEY (orphanage_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database created successfully!")

if __name__ == '__main__':
    init_db()