#helpers.py

from models.restaurant import Restaurant
from models.customer import Customer
from models.review import Review

def list_restaurants():
    restaurants = Restaurant.get_all()
    for restaurant in restaurants:
        print(restaurant)

def create_restaurant():
    name = input("Enter the restaurant name: ")
    price = int(input("Enter the restaurant price: "))
    restaurant = Restaurant(name, price)
    restaurant.save()
    print(f"Restaurant created: {restaurant}")

def update_restaurant():
    restaurant_id = int(input("Enter the restaurant ID: "))
    restaurant = Restaurant.find_by_id(restaurant_id)
    if restaurant:
        name = input("Enter the new restaurant name: ")
        price = int(input("Enter the new restaurant price: "))
        restaurant.name = name
        restaurant.price = price
        restaurant.update()
        print(f"Restaurant updated: {restaurant}")
    else:
        print(f"Restaurant with ID {restaurant_id} not found.")

def delete_restaurant():
    restaurant_id = int(input("Enter the restaurant ID: "))
    restaurant = Restaurant.find_by_id(restaurant_id)
    if restaurant:
        restaurant.delete()
        print(f"Restaurant with ID {restaurant_id} deleted.")
    else:
        print(f"Restaurant with ID {restaurant_id} not found.")

def list_customers():
    customers = Customer.get_all()
    for customer in customers:
        print(customer)

def create_customer():
    first_name = input("Enter the customer's first name: ")
    last_name = input("Enter the customer's last name: ")
    customer = Customer(first_name, last_name)
    customer.save()
    print(f"Customer created: {customer}")

def update_customer():
    customer_id = int(input("Enter the customer ID: "))
    customer = Customer.find_by_id(customer_id)
    if customer:
        first_name = input("Enter the new first name: ")
        last_name = input("Enter the new last name: ")
        customer.first_name = first_name
        customer.last_name = last_name
        customer.update()
        print(f"Customer updated: {customer}")
    else:
        print(f"Customer with ID {customer_id} not found.")

def delete_customer():
    customer_id = int(input("Enter the customer ID: "))
    customer = Customer.find_by_id(customer_id)
    if customer:
        customer.delete()
        print(f"Customer with ID {customer_id} deleted.")
    else:
        print(f"Customer with ID {customer_id} not found.")

def create_review():
    customer_id = int(input("Enter the customer ID: "))
    restaurant_id = int(input("Enter the restaurant ID: "))
    star_rating = int(input("Enter the star rating (1-5): "))
    customer = Customer.find_by_id(customer_id)
    restaurant = Restaurant.find_by_id(restaurant_id)
    if customer and restaurant:
        review = Review(customer_id, restaurant_id, star_rating)
        review.save()
        print(f"Review created: {review}")
    else:
        print("Invalid customer or restaurant ID.")

def list_restaurant_reviews():
    restaurant_id = int(input("Enter the restaurant ID: "))
    restaurant = Restaurant.find_by_id(restaurant_id)
    if restaurant:
        reviews = restaurant.reviews()
        if reviews:
            print(f"Reviews for {restaurant.name}:")
            for review in reviews:
                print(review)
        else:
            print(f"No reviews found for {restaurant.name}.")
    else:
        print(f"Restaurant with ID {restaurant_id} not found.")

def list_customer_reviews():
    customer_id = int(input("Enter the customer ID: "))
    customer = Customer.find_by_id(customer_id)
    if customer:
        reviews = customer.reviews()
        if reviews:
            print(f"Reviews by {customer.first_name} {customer.last_name}:")
            for review in reviews:
                print(review)
        else:
            print(f"No reviews found for {customer.first_name} {customer.last_name}.")
    else:
        print(f"Customer with ID {customer_id} not found.")

def return_customer_fullname():
    customer_id = int(input("Enter the customer ID: "))
    customer = Customer.find_by_id(customer_id)
    if customer:
        print(f"{customer.first_name} {customer.last_name}")
    else:
        print(f"Customer with ID {customer_id} not found.")

def get_customers_favourite_restaurant():
    customer_id = int(input("Enter the customer ID: "))
    customer = Customer.find_by_id(customer_id)
    if customer:
        favourite = customer.favourite_restaurant()
        if favourite:
            print(f"{customer.full_name()}'s favorite restaurant is {favourite.name}.")
        else:
            print(f"{customer.full_name()} has not reviewed any restaurants yet.")
    else:
        print(f"Customer with ID {customer_id} not found.")

def customer_delete_reviews():
    customer_id = int(input("Enter the customer ID: "))
    restaurant_id = int(input("Enter the restaurant ID to delete reviews for: "))
    customer = Customer.find_by_id(customer_id)
    restaurant = Restaurant.find_by_id(restaurant_id)
    if customer and restaurant:
        customer.delete_reviews(restaurant)
        print(f"Reviews by {customer.full_name()} for {restaurant.name} deleted successfully.")
    else:
        print("Invalid customer or restaurant ID.")
