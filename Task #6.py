import datetime
import os

# Base class for all records
class Record:
    def __init__(self, text):
        self.text = text.lower()
        self.date_published = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def publish(self):
        raise NotImplementedError("Subclasses must implement the publish method.")

    def capitalize_words(self, text):
        return text.title()

# News class
class News(Record):
    def __init__(self, text, city):
        super().__init__(text)
        self.city = city.lower()

    def publish(self):
        result = f"News: {self.capitalize_words(self.text)} | City: {self.capitalize_words(self.city)} | Published on: {self.date_published}"
        return result

# Private Ad class
class PrivateAd(Record):
    def __init__(self, text, expiration_date):
        super().__init__(text)
        self.expiration_date = datetime.datetime.strptime(expiration_date, "%Y-%m-%d")
        self.days_left = (self.expiration_date - datetime.datetime.now()).days

    def publish(self):
        result = f"Private Ad: {self.capitalize_words(self.text)} | Expires in: {self.days_left} days | Published on: {self.date_published}"
        return result

# Custom record class
class CustomEntry(Record):
    def __init__(self, custom_type, text, additional_info):
        super().__init__(text)
        self.custom_type = custom_type.lower()
        self.additional_info = additional_info.lower()

    def publish(self):
        result = f"{self.capitalize_words(self.custom_type)}: {self.capitalize_words(self.text)} | Additional Info: {self.capitalize_words(self.additional_info)} | Published on: {self.date_published}"
        return result

# Main tool class to handle user interaction and file writing
class NewsFeedTool:
    def __init__(self):
        self.filename = input("Enter the file path to save records (or press Enter for default 'user_generated_news_feed.txt'): ") or "user_generated_news_feed.txt"

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

    def process_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()

            for line in lines:
                # Example: Assume each line is a simple news record formatted as "text | city"
                record_data = line.strip().split(" | ")
                if len(record_data) == 2:
                    record = News(record_data[0], record_data[1])
                    self.publish_record(record)
                else:
                    print("Invalid record format in file.")

            # If everything was processed successfully, remove the file
            os.remove(file_path)
            print(f"File '{file_path}' successfully processed and removed.")

        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred while processing the file: {e}")

    def run(self):
        while True:
            print("\nSelect the type of record you want to add:")
            print("1. News")
            print("2. Private Ad")
            print("3. Custom Entry")
            print("4. Process records from file")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                record = self.get_news()
                self.publish_record(record)
            elif choice == '2':
                record = self.get_private_ad()
                self.publish_record(record)
            elif choice == '3':
                record = self.get_custom_entry()
                self.publish_record(record)
            elif choice == '4':
                file_path = input("Enter the path to the file to process: ")
                self.process_file(file_path)
            elif choice == '5':
                print("Exiting the tool.")
                break
            else:
                print("Invalid choice. Please try again.")
                continue

            # Ask if the user wants to add another record
            add_more = input("Do you want to add another record? (y/n): ")
            if add_more.lower() != 'y':
                break

if __name__ == "__main__":
    tool = NewsFeedTool()
    tool.run()
