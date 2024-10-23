import sqlite3
import json
from models import Location

LOCATIONS = [
    {
        "id": 1,
        "name": "Nashville North",
        "address": "8422 Johnson Pike"
    },
    {
        "id": 2,
        "name": "Nashville South",
        "address": "209 Emory Drive"
    }
]

def get_all_locations():
    return LOCATIONS

def get_single_location(id):

    for location in LOCATIONS:
    
        if location["id"] == id:
            requested_Location = location
            
    return requested_Location

def create_location(location):
    # Get the id value of the last animal in the list
    max_id = LOCATIONS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    location["id"] = new_id

    # Add the animal dictionary to the list
    LOCATIONS.append(location)

    # Return the dictionary with `id` property added
    return location

def delete_location(id):
    # Initial -1 value for animal index, in case one isn't found
    location_index = -1

    # Iterate the ANIMALS list, but use enumerate() so that you
    # can access the index value of each item
    for index, location in enumerate(LOCATIONS):
        if location_index["id"] == id:
            # Found the animal. Store the current index.
            location_index = index

    # If the animal was found, use pop(int) to remove it from list
    if location_index >= 0:
        LOCATIONS.pop(location_index)

def update_location(id, new_location):
    # Iterate the ANIMALS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            # Found the animal. Update the value.
            LOCATIONS[index] = new_location
            break
        
def get_all_locations():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address
        FROM location a
        """)

        # Initialize an empty list to hold all animal representations
        locations = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            location = Location(row['id'], row['name'])

            locations.append(location.__dict__) # see the notes below for an explanation on this line of code.

    return locations

def get_single_locaiton(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address
        FROM location a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        location = Location(data['id'], data['name'], data['address'])

        return location.__dict__
