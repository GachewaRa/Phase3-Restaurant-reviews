from models.__init__ import CONN, CURSOR
from models.restaurant import Restaurant
from models.customer import Customer
from models.review import Review

def seed_database():
    # Drop tables if they exist
    Review.drop_table()
    Customer.drop_table()
    Restaurant.drop_table()

    # Create tables
    Restaurant.create_table()
    Customer.create_table()
    Review.create_table()

    # Seed restaurants
    restaurants = [
        Restaurant("Java", 100),
        Restaurant("Galito", 150),
        Restaurant("BigFish", 180),
        Restaurant("Ashaki", 200),
        Restaurant("Serena", 250)
    ]
    for restaurant in restaurants:
        restaurant.save()

    # Seed customers
    customers = [
        Customer("Ann", "Wangu"),
        Customer("Dan", "Mill"),
        Customer("Karl", "Marx"),
        Customer("Johnny", "Bravo"),
        Customer("Nana", "Bell")
    ]
    for customer in customers:
        customer.save()

    # Seed reviews
    reviews = [
        Review(customers[0].id, restaurants[4].id, 5),  # Ann gave Serena 5 stars
        Review(customers[1].id, restaurants[3].id, 5),  # Dan gave Ashaki 5 stars
        Review(customers[2].id, restaurants[2].id, 5),  # Karl gave BigFish 5 stars
        Review(customers[3].id, restaurants[1].id, 5),  # Johnny gave Galito 5 stars
        Review(customers[4].id, restaurants[0].id, 5),  # Nana gave Java 5 stars
        Review(customers[0].id, restaurants[0].id, 3),  # Ann gave Java 3 stars
        Review(customers[0].id, restaurants[1].id, 4),  # Ann gave Galito 4 stars
        Review(customers[0].id, restaurants[2].id, 2),  # Ann gave BigFish 2 stars
        Review(customers[0].id, restaurants[3].id, 1),  # Ann gave Ashaki 1 star
        # Add more reviews as needed
    ]
    for review in reviews:
        review.save()

    print("Seeded database successfully!")

if __name__ == "__main__":
    seed_database()