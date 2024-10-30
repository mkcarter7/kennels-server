import sqlite3
import json
from models import Location
from models.animal import Animal
from models.employee import Employee

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

        # Initialize an empty list to hold all location representations
        locations = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an location instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Location class above.
            location = Location(row['id'], row['name'],
                                row['address'])

            locations.append(location.__dict__) # see the notes below for an explanation on this line of code.

    return locations

def get_single_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        employee_db_cursor = conn.cursor()
        animal_db_cursor = conn.cursor()
        
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

        # Create an location instance from the current row
        location = Location(data['id'], data['name'], data['address'])
        
        employee_db_cursor.execute("""
        SELECT
            e.id employee_id,
            e.name employee_name,
            e.address employee_address,
            e.location_id employee_location_id
        FROM employee e
        WHERE e.location_id = ?
        """, ( id, ))
        
        employee_data = employee_db_cursor.fetchall()
        
        employees = []
        
        for row in employee_data:
            employee = Employee(row['employee_id'], row['employee_name'], row['employee_address'], row['employee_location_id'])
            
            employees.append(employee.serialized())

        location.employees = employees
        
        animal_db_cursor.execute("""
        SELECT
            a.id animal_id,
            a.name animal_name,
            a.breed animal_breed,
            a.status animal_status,
            a.location_id animal_location_id,
            a.customer_id animal_customer_id
        FROM animal a
        WHERE a.location_id = ?
        """, ( id, ))

        animal_data = animal_db_cursor.fetchall()
        
        animals = []
        
        for row in animal_data:
            animal = Animal(row['animal_id'], row['animal_name'], row['animal_breed'], row['animal_status'], row['animal_location_id'], row['animal_customer_id'])
            
            animals.append(animal.serialized())
        
        location.animals = animals

        return location.__dict__

def create_location(new_location):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Location
            ( name, address )
        VALUES
            ( ?, ?);
        """, (new_location['name'], new_location['address'] ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the employee dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_location['id'] = id

    return new_location

def delete_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM location
        WHERE id = ?
        """, (id, ))

def update_location(id, new_location):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Location
            SET
                name = ?,
                address = ?
        WHERE id = ?
        """, (new_location['name'], new_location['address'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    # return value of this function
    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
