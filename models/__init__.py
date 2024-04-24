import sqlite3

CONN = sqlite3.connect('restaurant_reviews.db')
CURSOR = CONN.cursor()