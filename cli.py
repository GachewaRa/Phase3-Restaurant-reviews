from helpers import (
    list_restaurants,
    create_restaurant,
    update_restaurant,
    delete_restaurant,
    list_customers,
    create_customer,
    update_customer,
    delete_customer,
    create_review,
    list_restaurant_reviews,
    list_customer_reviews,
)

def main():
    while True:
        print("\nRestaurant Reviews CLI")
        print("1. List restaurants")
        print("2. Create restaurant")
        print("3. Update restaurant")
        print("4. Delete restaurant")
        print("5. List customers")
        print("6. Create customer")
        print("7. Update customer")
        print("8. Delete customer")
        print("9. Create review")
        print("10. List restaurant reviews")
        print("11. List customer reviews")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            list_restaurants()
        elif choice == "2":
            create_restaurant()
        elif choice == "3":
            update_restaurant()
        elif choice == "4":
            delete_restaurant()
        elif choice == "5":
            list_customers()
        elif choice == "6":
            create_customer()
        elif choice == "7":
            update_customer()
        elif choice == "8":
            delete_customer()
        elif choice == "9":
            create_review()
        elif choice == "10":
            list_restaurant_reviews()
        elif choice == "11":
            list_customer_reviews()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()