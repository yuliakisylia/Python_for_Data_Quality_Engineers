import sqlite3
import math


# Haversine formula to calculate the distance between two points on the Earth
def haversine(lat1, lon1, lat2, lon2):
    # Radius of Earth in kilometers
    R = 6371.0

    # Convert degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Differences between the points
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calculate distance
    distance = R * c
    return distance


# Database handler class
class DatabaseHandler:
    def __init__(self, db_name="city_coordinates.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        # Create table to store city coordinates if it doesn't exist
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS cities (
            city_name TEXT PRIMARY KEY,
            latitude REAL,
            longitude REAL
        )
        """)
        self.connection.commit()

    def get_coordinates(self, city_name):
        # Fetch coordinates from the database
        self.cursor.execute("SELECT latitude, longitude FROM cities WHERE city_name = ?", (city_name,))
        result = self.cursor.fetchone()
        return result

    def insert_coordinates(self, city_name, latitude, longitude):
        # Insert city coordinates into the database
        self.cursor.execute("INSERT INTO cities (city_name, latitude, longitude) VALUES (?, ?, ?)",
                            (city_name, latitude, longitude))
        self.connection.commit()


# Function to get city coordinates from the user
def get_coordinates_from_user(city_name):
    print(f"Coordinates for {city_name} not found. Please provide them.")
    latitude = float(input("Enter latitude: "))
    longitude = float(input("Enter longitude: "))
    return latitude, longitude


# Main function to calculate the distance
def calculate_distance():
    db_handler = DatabaseHandler()

    # Get city names from the user
    city1 = input("Enter the first city: ").strip()
    city2 = input("Enter the second city: ").strip()

    # Fetch coordinates from the database
    coords1 = db_handler.get_coordinates(city1)
    if not coords1:
        # If coordinates not found, get them from the user and store them
        latitude1, longitude1 = get_coordinates_from_user(city1)
        db_handler.insert_coordinates(city1, latitude1, longitude1)
    else:
        latitude1, longitude1 = coords1

    coords2 = db_handler.get_coordinates(city2)
    if not coords2:
        # If coordinates not found, get them from the user and store them
        latitude2, longitude2 = get_coordinates_from_user(city2)
        db_handler.insert_coordinates(city2, latitude2, longitude2)
    else:
        latitude2, longitude2 = coords2

    # Calculate the distance using Haversine formula
    distance = haversine(latitude1, longitude1, latitude2, longitude2)

    # Return the calculated distance
    print(f"The straight-line distance between {city1} and {city2} is: {distance:.2f} kilometers.")


if __name__ == "__main__":
    calculate_distance()
