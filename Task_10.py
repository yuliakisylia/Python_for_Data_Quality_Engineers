import os
import datetime
import csv
from collections import Counter
import re
import json
import xml.etree.ElementTree as ET
import sqlite3
from Task_4 import normalize_case  # Импорт функции нормализации из Task_4

# Класс для записи
class Record:
    def __init__(self, text):
        self.text = normalize_case([text])[0]  # Применение нормализации к тексту
        self.date_published = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def publish(self):
        raise NotImplementedError("Subclasses must implement the publish method.")


# Классы для различных типов записей
class News(Record):
    def __init__(self, text, city):
        super().__init__(text)
        self.city = normalize_case([city])[0]

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
        self.age = normalize_case([age])[0]
        self.interests = normalize_case([interests])[0]
        self.contact_info = normalize_case([contact_info])[0]

    def publish(self):
        return f"Dating Ad: {self.text} | Age: {self.age} | Interests: {self.interests} | Contact: {self.contact_info} | Published on: {self.date_published}"


# Класс для обработки XML
class XMLRecordProcessor:
    def __init__(self):
        pass

    def process_xml_file(self):
        file_path = input("Enter the XML file path (or press Enter to use default): ").strip()
        if not file_path:
            file_path = "./records.xml"

        if not os.path.exists(file_path):
            print(f"\nError: No XML file found at {file_path}. Please check the file path and try again.\n")
            return

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            print(f"Successfully loaded XML from {file_path}.")
        except ET.ParseError as e:
            print(f"\nError: Invalid XML format. Details: {str(e)}\n")
            return
        except Exception as e:
            print(f"\nError: Unable to read the file. Details: {str(e)}\n")
            return

        records = root.findall("record")  # Assumes each record is wrapped in <record> tags
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
        # Запись в текстовый файл
        with open("user_generated_news_feed.txt", "a", encoding="utf-8") as file:
            file.write(record.publish() + "\n")
        print("Record added successfully!")


# Класс для работы с базой данных SQLite
class DatabaseHandler:
    def __init__(self, db_name="records.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            date_published TEXT,
            record_type TEXT,
            city TEXT,
            expiration_date TEXT,
            age TEXT,
            interests TEXT,
            contact_info TEXT
        )
        """)
        self.connection.commit()

    def insert_record(self, record):
        # Проверка на дублирование
        if not isinstance(record.text, str) or not isinstance(record.date_published, str):
            print(f"Error: Invalid types for text or date_published. Received types: {type(record.text)}, {type(record.date_published)}")
            return

        self.cursor.execute("SELECT * FROM records WHERE text = ? AND date_published = ?",
                            (record.text, record.date_published))
        if self.cursor.fetchone():
            print("Error: Duplicate record found, not inserted.")
            return

        # Вставка записи в базу данных
        params = (
            record.text,
            record.date_published,
            record.__class__.__name__.lower(),  # Сохраняем тип записи (news, private_ad, dating_ad)
            record.city if hasattr(record, 'city') else None,
            record.expiration_date if hasattr(record, 'expiration_date') else None,
            record.age if hasattr(record, 'age') else None,
            record.interests if hasattr(record, 'interests') else None,
            record.contact_info if hasattr(record, 'contact_info') else None
        )

        try:
            self.cursor.execute("""
            INSERT INTO records (text, date_published, record_type, city, expiration_date, age, interests, contact_info)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, params)
            self.connection.commit()
            print("Record successfully inserted into the database.")
        except sqlite3.Error as e:
            print(f"SQLite error occurred: {e}")


# Основной класс для работы с пользовательскими вводами
class NewsFeedTool:
    def __init__(self, filename="user_generated_news_feed.txt"):
        self.filename = filename
        self.xml_processor = XMLRecordProcessor()  # Создание экземпляра для работы с XML
        self.db_handler = DatabaseHandler()  # Создание экземпляра для работы с базой данных

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
        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(record.publish() + "\n")
        print("Record added successfully!")

    def run(self):
        while True:
            print("\nSelect the type of record you want to add:")
            print("1. News")
            print("2. Private Ad")
            print("3. Dating Ad")
            print("4. Process JSON File")
            print("5. Process XML File")
            print("6. Exit")

            choice = input("Enter your choice (1-6): ")
            if choice == '1':
                record = self.get_news()
            elif choice == '2':
                record = self.get_private_ad()
            elif choice == '3':
                record = self.get_dating_ad()
            elif choice == '4':
                self.process_json_file()
                continue
            elif choice == '5':
                self.xml_processor.process_xml_file()
                continue
            elif choice == '6':
                print("Exiting the tool.")
                break
            else:
                print("Invalid choice. Please try again.")
                continue

            self.db_handler.insert_record(record)  # Вставка записи в базу данных
            self.publish_record(record)  # Публикация записи в файл


# Запуск программы
if __name__ == "__main__":
    tool = NewsFeedTool()
    tool.run()





