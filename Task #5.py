import datetime


# Base class for all records
class Record:
    def __init__(self, text):
        self.text = text
        self.date_published = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def publish(self):
        raise NotImplementedError("Subclasses must implement the publish method.")


# News class
class News(Record):
    def __init__(self, text, city):
        super().__init__(text)
        self.city = city

    def publish(self):
        return f"News: {self.text} | City: {self.city} | Published on: {self.date_published}"


# Private Ad class
class PrivateAd(Record):
    def __init__(self, text, expiration_date):
        super().__init__(text)
        self.expiration_date = datetime.datetime.strptime(expiration_date, "%Y-%m-%d")
        self.days_left = (self.expiration_date - datetime.datetime.now()).days

    def publish(self):
        return f"Private Ad: {self.text} | Expires in: {self.days_left} days | Published on: {self.date_published}"


# Custom record class (you can customize the rules for publishing here)
class CustomEntry(Record):
    def __init__(self, custom_type, text, additional_info):
        super().__init__(text)
        self.custom_type = custom_type
        self.additional_info = additional_info

    def publish(self):
        return f"{self.custom_type}: {self.text} | Additional Info: {self.additional_info} | Published on: {self.date_published}"


# Main tool class to handle user interaction and file writing
class NewsFeedTool:
    def __init__(self, filename="user_generated_news_feed.txt"):
        self.filename = filename

    def get_news(self):
        text = input("Enter the news text: ")
        city = input("Enter the city: ")
        return News(text, city)

    def get_private_ad(self):
        text = input("Enter the private ad text: ")
        expiration_date = input("Enter the expiration date (YYYY-MM-DD): ")
        return PrivateAd(text, expiration_date)

    def get_custom_entry(self):
        custom_type = input("Enter custom record type: ")
        text = input(f"Enter the text for {custom_type}: ")
        additional_info = input("Enter any additional information: ")
        return CustomEntry(custom_type, text, additional_info)

    def publish_record(self, record):
        with open(self.filename, "a") as file:
            file.write(record.publish() + "\n")
        print("Record added successfully!")

    def run(self):
        while True:
            print("\nSelect the type of record you want to add:")
            print("1. News")
            print("2. Private Ad")
            print("3. Custom Entry")
            print("4. Exit")

            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                record = self.get_news()
            elif choice == '2':
                record = self.get_private_ad()
            elif choice == '3':
                record = self.get_custom_entry()
            elif choice == '4':
                print("Exiting the tool.")
                break
            else:
                print("Invalid choice. Please try again.")
                continue

            self.publish_record(record)


if __name__ == "__main__":
    tool = NewsFeedTool()
    tool.run()