import os
import datetime
import csv
from collections import Counter
import re
import json
import xml.etree.ElementTree as ET
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


class XMLRecordProcessor:
    def __init__(self):
        pass

    def process_xml_file(self):
        file_path = input("Enter the XML file path (or press Enter to use default): ").strip()
        if not file_path:
            file_path = "./records.xml"

        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"\nError: No XML file found at {file_path}. Please check the file path and try again.\n")
            return

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            print(f"Successfully loaded XML from {file_path}.")  # Debugging line
        except ET.ParseError as e:
            print(f"\nError: Invalid XML format. Details: {str(e)}\n")
            return
        except Exception as e:
            print(f"\nError: Unable to read the file. Details: {str(e)}\n")
            return

        records = root.findall("record")  # Assuming each record is enclosed in <record> tags
        for record in records:
            try:
                record_type = record.find("type").text.lower()
                if record_type == "news":
                    text = record.find("text").text
                    city = record.find("city").text
                    new_record = News(text, city)
                elif record_type == "private_ad":
                    text = record.find("text").text
                    expiration_date = record.find("expiration_date").text
                    new_record = PrivateAd(text, expiration_date)
                elif record_type == "dating_ad":
                    text = record.find("text").text
                    age = record.find("age").text
                    interests = record.find("interests").text
                    contact_info = record.find("contact_info").text
                    new_record = DatingAd(text, age, interests, contact_info)
                else:
                    print(f"Warning: Unknown record type '{record_type}'. Skipping.")
                    continue

                self.publish_record(new_record)
            except AttributeError as e:
                print(f"Warning: Missing field {e} in record: {record}. Skipping.")
            except Exception as e:
                print(f"Error: Unable to process record: {record}. Reason: {e}. Skipping.")

        print(f"\nAll records from {file_path} have been processed successfully.")
        os.remove(file_path)
        print(f"File {file_path} has been removed.\n")

    def publish_record(self, record):
        # Write the record to a file with UTF-8 encoding
        with open("user_generated_news_feed.txt", "a", encoding="utf-8") as file:
            file.write(record.publish() + "\n")
        print("Record added successfully!")


class NewsFeedTool:
    def __init__(self, filename="user_generated_news_feed.txt"):
        self.filename = filename
        self.xml_processor = XMLRecordProcessor()  # Instance of XMLRecordProcessor

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

    def process_json_file(self):
        file_path = input("Enter the JSON file path (or press Enter to use default): ").strip()
        if not file_path:
            file_path = "./records.json"

        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"\nError: No JSON file found at {file_path}. Please check the file path and try again.\n")
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                records = json.load(file)
                print(f"Successfully loaded JSON from {file_path}.")  # Debugging line
        except json.JSONDecodeError as e:
            print(f"\nError: Invalid JSON format. Details: {str(e)}\n")
            return
        except Exception as e:
            print(f"\nError: Unable to read the file. Details: {str(e)}\n")
            return

        if not isinstance(records, list):
            records = [records]

        for record in records:
            try:
                record_type = record.get("type", "").lower()
                if record_type == "news":
                    new_record = News(record["text"], record["city"])
                elif record_type == "private_ad":
                    new_record = PrivateAd(record["text"], record["expiration_date"])
                elif record_type == "dating_ad":
                    new_record = DatingAd(record["text"], record["age"], record["interests"], record["contact_info"])
                else:
                    print(f"Warning: Unknown record type '{record_type}'. Skipping.")
                    continue

                self.publish_record(new_record)
            except KeyError as e:
                print(f"Warning: Missing field {e} in record: {record}. Skipping.")
            except Exception as e:
                print(f"Error: Unable to process record: {record}. Reason: {e}. Skipping.")

        print(f"\nAll records from {file_path} have been processed successfully.")
        os.remove(file_path)
        print(f"File {file_path} has been removed.\n")

    def run(self):
        while True:
            print("\nSelect the type of record you want to add:")
            print("1. News")
            print("2. Private Ad")
            print("3. Dating Ad")
            print("4. Process JSON File")
            print("5. Process XML File")
            print("6. Exit")

            try:
                choice = input("Enter your choice (1-6): ")
            except KeyboardInterrupt:
                print("\nProcess interrupted by user. Exiting...")
                break

            if choice == '1':
                record = self.get_news()
            elif choice == '2':
                record = self.get_private_ad()
            elif choice == '3':
                record = self.get_dating_ad()
            elif choice == '4':
                self.process_json_file()
                continue  # Skip the publish_record step for JSON processing
            elif choice == '5':
                self.xml_processor.process_xml_file()  # Use the XML processor
                continue  # Skip the publish_record step for XML processing
            elif choice == '6':
                print("Exiting the tool.")
                break
            else:
                print("Invalid choice. Please try again.")
                continue

            self.publish_record(record)

            # Update CSV files after adding a new record
            self.update_word_count_csv()
            self.update_letter_stats_csv()


if __name__ == "__main__":
    tool = NewsFeedTool()
    tool.run()

