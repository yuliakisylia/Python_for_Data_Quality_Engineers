import datetime
import csv
import string
import json
import os
import xml.etree.ElementTree as ET
from collections import Counter

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

# Custom record class
class CustomEntry(Record):
    def __init__(self, custom_type, text, additional_info):
        super().__init__(text)
        self.custom_type = custom_type
        self.additional_info = additional_info

    def publish(self):
        return f"{self.custom_type}: {self.text} | Additional Info: {self.additional_info} | Published on: {self.date_published}"

# New XML-based record importer
class XMLRecordImporter:
    def __init__(self, tool, default_folder="data"):
        self.tool = tool
        self.default_folder = default_folder

    def import_from_xml(self, file_path=None):
        file_path = file_path or os.path.join(self.default_folder, "records.xml")

        if not os.path.exists(file_path):
            print("File not found.")
            return

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            for record in root.findall("record"):
                self.process_record(record)

            os.remove(file_path)
            print(f"File '{file_path}' processed and removed successfully.")
        except Exception as e:
            print(f"Error processing the XML file: {e}")

    def process_record(self, record_element):
        record_type = record_element.get("type")
        text = record_element.find("text").text if record_element.find("text") is not None else ""

        if record_type == "News":
            city = record_element.find("city").text if record_element.find("city") is not None else "Unknown"
            self.tool.publish_record(News(text, city))
        elif record_type == "PrivateAd":
            expiration_date = record_element.find("expiration_date").text
            self.tool.publish_record(PrivateAd(text, expiration_date))
        elif record_type == "CustomEntry":
            custom_type = record_element.find("custom_type").text if record_element.find("custom_type") is not None else "Custom"
            additional_info = record_element.find("additional_info").text if record_element.find("additional_info") is not None else ""
            self.tool.publish_record(CustomEntry(custom_type, text, additional_info))
        else:
            print(f"Unknown record type: {record_type}")

# Main tool class to handle user interaction, file writing, and CSV updates
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

        # Update the word and letter count CSVs after adding each record
        self.update_word_count_csv()
        self.update_letter_count_csv()

    def update_word_count_csv(self):
        with open(self.filename, "r") as file:
            text = file.read().lower()
        word_counts = Counter(text.split())

        with open("word_count.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["word", "count"])
            for word, count in word_counts.items():
                writer.writerow([word, count])

    def update_letter_count_csv(self):
        try:
            # Read text from file and remove spaces
            with open(self.filename, "r") as file:
                text = file.read().replace(" ", "")  # Remove spaces

            # Filter out only alphabetic characters
            text = ''.join(filter(str.isalpha, text))

            # Count all letters (in lowercase) and uppercase letters specifically
            letter_counts = Counter(text.lower())
            uppercase_counts = Counter(c for c in text if c.isupper())

            # Write letter counts to CSV
            with open("letter_count.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["letter", "count_all", "count_uppercase", "percentage"])  # Write header

                # Process each letter in the alphabet
                for letter in string.ascii_lowercase:
                    count_all = letter_counts.get(letter, 0)
                    count_upper = uppercase_counts.get(letter.upper(), 0)
                    percentage = (count_upper / count_all * 100) if count_all > 0 else 0
                    writer.writerow([letter, count_all, count_upper, round(percentage, 2)])

            print("Letter count CSV updated successfully.")

        except Exception as e:
            print(f"An error occurred while updating letter count CSV: {e}")

    def run(self):
        while True:
            print("\nSelect the type of record you want to add:")
            print("1. News")
            print("2. Private Ad")
            print("3. Custom Entry")
            print("4. Import from JSON")
            print("5. Import from XML")
            print("6. Exit")

            choice = input("Enter your choice (1-6): ")

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
                json_importer = JSONRecordImporter(self)
                file_path = input("Enter JSON file path or press Enter to use the default location: ")
                json_importer.import_from_json(file_path)
            elif choice == '5':
                xml_importer = XMLRecordImporter(self)
                file_path = input("Enter XML file path or press Enter to use the default location: ")
                xml_importer.import_from_xml(file_path)
            elif choice == '6':
                print("Exiting the tool.")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    tool = NewsFeedTool()
    tool.run()
