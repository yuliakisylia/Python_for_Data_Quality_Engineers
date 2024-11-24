import os
import datetime
from Task_4 import normalize_case  # Import the normalize_case function from module 4


class Record:
    def __init__(self, text):
        self.text = normalize_case([text])[0]  # Apply normalize_case to the text
        self.date_published = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def publish(self):
        raise NotImplementedError("Subclasses must implement the publish method.")


class News(Record):
    def __init__(self, text, city):
        super().__init__(text)
        self.city = normalize_case([city])[0]  # Normalize the city name

    def publish(self):
        return f"News: {self.text} | City: {self.city} | Published on: {self.date_published}"


class PrivateAd(Record):
    def __init__(self, text, expiration_date):
        super().__init__(text)
        self.expiration_date = datetime.datetime.strptime(expiration_date, "%Y-%m-%d")
        self.days_left = (self.expiration_date - datetime.datetime.now()).days

    def publish(self):
        return f"Private Ad: {self.text} | Expires in: {self.days_left} days | Published on: {self.date_published}"


class DatingAd(Record):
    def __init__(self, text, age, interests, contact_info):
        super().__init__(text)
        self.age = normalize_case([age])[0]  # Normalize the age (if needed in text format)
        self.interests = normalize_case([interests])[0]  # Normalize the interests
        self.contact_info = normalize_case([contact_info])[0]  # Normalize the contact information

    def publish(self):
        return f"Dating Ad: {self.text} | Age: {self.age} | Interests: {self.interests} | Contact: {self.contact_info} | Published on: {self.date_published}"


class NewsFeedTool:
    def __init__(self, filename="user_generated_news_feed.txt"):
        self.filename = filename

    def get_news(self):
        text = input("Enter the news text: ")
        city = input("Enter the city: ")
        return News(text, city)

    def get_private_ad(self):
        text = input("Enter the private ad text: ")
        while True:
            expiration_date = input("Enter the expiration date (YYYY-MM-DD): ")
            try:
                exp_date = datetime.datetime.strptime(expiration_date, "%Y-%m-%d")
                if exp_date <= datetime.datetime.now():
                    print("Error: Expiration date must be a future date. Please try again.")
                else:
                    break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
        return PrivateAd(text, expiration_date)

    def get_dating_ad(self):
        text = input("Enter the text for the dating ad: ")
        age = input("Enter the age: ")
        interests = input("Enter interests: ")
        contact_info = input("Enter contact info: ")
        return DatingAd(text, age, interests, contact_info)

    def publish_record(self, record):
        # Write the record to a file with UTF-8 encoding
        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(record.publish() + "\n")
        print("Record added successfully!")

    def process_and_remove_file(self):
        # Check if the file exists
        if os.path.exists(self.filename):
            print(f"\nProcessing file: {self.filename}")
            with open(self.filename, "r", encoding="utf-8") as file:
                for line in file:
                    print("Processed:", line.strip())

            # Remove the file after processing
            os.remove(self.filename)
            print(f"File {self.filename} has been successfully processed and removed.")
        else:
            print(f"No file found with the name {self.filename}.")

    def run(self):
        while True:
            print("\nSelect the type of record you want to add:")
            print("1. News")
            print("2. Private Ad")
            print("3. Dating Ad")
            print("4. Process and Remove File")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                record = self.get_news()
            elif choice == '2':
                record = self.get_private_ad()
            elif choice == '3':
                record = self.get_dating_ad()
            elif choice == '4':
                self.process_and_remove_file()
            elif choice == '5':
                print("Exiting the tool.")
                break
            else:
                print("Invalid choice. Please try again.")
                continue

            self.publish_record(record)


if __name__ == "__main__":
    tool = NewsFeedTool()
    tool.run()








