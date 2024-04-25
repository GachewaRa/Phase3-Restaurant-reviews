#review.py

from models.__init__ import CURSOR, CONN
from models.restaurant import Restaurant
from models.customer import Customer

class Review:
    all = {}

    def __init__(self, customer_id, restaurant_id, star_rating):
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id
        self.star_rating = star_rating
        self.id = None

    def __repr__(self):
        return f"<Review for {self.restaurant_id} by {self.customer_id}, Rating: {self.star_rating}>"

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                restaurant_id INTEGER,
                star_rating INTEGER,
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
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
            INSERT INTO reviews (customer_id, restaurant_id, star_rating)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.customer_id, self.restaurant_id, self.star_rating))
        CONN.commit()
        self.id = CURSOR.lastrowid
        Review.all[self.id] = self

    def update(self):
        sql = """
            UPDATE reviews
            SET customer_id = ?, restaurant_id = ?, star_rating = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.customer_id, self.restaurant_id, self.star_rating, self.id))
        CONN.commit()

    def delete(self):
        sql = """
            DELETE FROM reviews
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del Review.all[self.id]
        self.id = None

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM reviews
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM reviews
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def instance_from_db(cls, row):
        review = cls.all.get(row[0])
        if review:
            review.customer_id = row[1]
            review.restaurant_id = row[2]
            review.star_rating = row[3]
        else:
            review = cls(row[1], row[2], row[3])
            review.id = row[0]
            cls.all[review.id] = review
        return review

    @property
    def customer(self):
        return Customer.find_by_id(self.customer_id)

    @property
    def restaurant(self):
        return Restaurant.find_by_id(self.restaurant_id)
    
    def full_review(self):
        customer = self.customer
        restaurant = self.restaurant
        return f"Review for {restaurant.name} by {customer.full_name()}: {self.star_rating} stars."