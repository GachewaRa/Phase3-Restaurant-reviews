from models.__init__ import CURSOR, CONN

class Restaurant:
    all = {}

    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.id = None

    def __repr__(self):
        return f"<Restaurant {self.name}, Price: {self.price}>"

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price INTEGER
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        sql = """
            INSERT INTO restaurants (name, price)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.price))
        CONN.commit()
        self.id = CURSOR.lastrowid
        Restaurant.all[self.id] = self

    def update(self):
        sql = """
            UPDATE restaurants
            SET name = ?, price = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.price, self.id))
        CONN.commit()

    def delete(self):
        sql = """
            DELETE FROM restaurants
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del Restaurant.all[self.id]
        self.id = None

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM restaurants
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM restaurants
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def instance_from_db(cls, row):
        restaurant = cls.all.get(row[0])
        if restaurant:
            restaurant.name = row[1]
            restaurant.price = row[2]
        else:
            restaurant = cls(row[1], row[2])
            restaurant.id = row[0]
            cls.all[restaurant.id] = restaurant
        return restaurant

    def reviews(self):
        sql = """
            SELECT *
            FROM reviews
            WHERE restaurant_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        from models.review import Review
        return [Review.instance_from_db(row) for row in rows]

    def customers(self):
        sql = """
            SELECT DISTINCT c.*
            FROM customers c
            JOIN reviews r ON c.id = r.customer_id
            WHERE r.restaurant_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        from models.customer import Customer
        return [Customer.instance_from_db(row) for row in rows]