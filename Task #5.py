import datetime

def get_news():
    text = input("Enter the news text: ")
    city = input("Enter the city: ")
    date_published = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"News: {text} | City: {city} | Published on: {date_published}"

def get_privad():
    text = input("Enter the private ad text: ")
    expiration_date = input("Enter the expiration date (YYYY-MM-DD): ")
    today = datetime.datetime.now()
    expiration = datetime.datetime.strptime(expiration_date, "%Y-%m-%d")
    days_left = (expiration - today).days
    return f"Private Ad: {text} | Expires in: {days_left} days"

def get_custom_entry():
    custom_type = input("Enter custom record type: ")
    text = input(f"Enter the text for {custom_type}: ")
    additional_info = input("Enter any additional information: ")
    date_published = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"{custom_type}: {text} | Info: {additional_info} | Published on: {date_published}"

def main():
    while True:
        print("\nSelect the type of record you want to add:")
        print("1. News")
        print("2. Private Ad")
        print("3. Custom Entry")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            record = get_news()
        elif choice == '2':
            record = get_privad()
        elif choice == '3':
            record = get_custom_entry()
        elif choice == '4':
            print("Exiting the tool.")
            break
        else:
            print("Invalid choice. Please try again.")
            continue

        # Append the record to the text file
        with open("user_generated_news_feed.txt", "a") as file:
            file.write(record + "\n")

        print("Record added successfully!")

if __name__ == "__main__":
    main()