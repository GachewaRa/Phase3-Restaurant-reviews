#customer.py

from models.__init__ import CURSOR, CONN

class Customer:
    all = {}

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.id = None

    def __repr__(self):
        return f"<Customer {self.first_name} {self.last_name}>"

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT
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
            INSERT INTO customers (first_name, last_name)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.first_name, self.last_name))
        CONN.commit()
        self.id = CURSOR.lastrowid
        Customer.all[self.id] = self

    def update(self):
        sql = """
            UPDATE customers
            SET first_name = ?, last_name = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.first_name, self.last_name, self.id))
        CONN.commit()

    def delete(self):
        sql = """
            DELETE FROM customers
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del Customer.all[self.id]
        self.id = None

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM customers
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM customers
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def instance_from_db(cls, row):
        customer = cls.all.get(row[0])
        if customer:
            customer.first_name = row[1]
            customer.last_name = row[2]
        else:
            customer = cls(row[1], row[2])
            customer.id = row[0]
            cls.all[customer.id] = customer
        return customer
    
    def reviews(self):
        sql = """
            SELECT *
            FROM reviews
            WHERE customer_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        from models.review import Review
        return [Review.instance_from_db(row) for row in rows]

    def restaurants(self):
        sql = """
            SELECT DISTINCT r.*
            FROM restaurants r
            JOIN reviews rv ON r.id = rv.restaurant_id
            WHERE rv.customer_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        from models.restaurant import Restaurant
        return [Restaurant.instance_from_db(row) for row in rows]
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def favourite_restaurant(self):
        reviews = self.reviews()
        if not reviews:
            return None
        highest_rating = max(reviews, key=lambda review: review.star_rating)
        return highest_rating.restaurant
    
    def delete_reviews(self, restaurant):
        sql = """
            DELETE FROM reviews
            WHERE customer_id = ? AND restaurant_id = ?
        """
        CURSOR.execute(sql, (self.id, restaurant.id))
        CONN.commit()
