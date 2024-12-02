from sqlalchemy import text
from database import engine

def create_schema():
    """Create the party planning database schema"""
    commands = [
        # Drop existing tables if they exist
        """DROP TABLE IF EXISTS Reservation_Performers CASCADE;""",
        """DROP TABLE IF EXISTS Reservation_Staff CASCADE;""",
        """DROP TABLE IF EXISTS Party_GuestOfHonor CASCADE;""",
        """DROP TABLE IF EXISTS Party_Decorations CASCADE;""",
        """DROP TABLE IF EXISTS Party CASCADE;""",
        """DROP TABLE IF EXISTS Reservation CASCADE;""",
        """DROP TABLE IF EXISTS Venue_amenities CASCADE;""",
        """DROP TABLE IF EXISTS Venue CASCADE;""",
        """DROP TABLE IF EXISTS Customer CASCADE;""",
        """DROP TABLE IF EXISTS Organizer CASCADE;""",
        """DROP TABLE IF EXISTS Staff CASCADE;""",
        """DROP TABLE IF EXISTS Caterer CASCADE;""",
        """DROP TABLE IF EXISTS Performers CASCADE;""",
        
        # Create tables in order
        """
        CREATE TABLE Venue (
            venue_id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            location VARCHAR(255),
            cost NUMERIC(10, 2),
            max_capacity INTEGER,
            open_time TIME,
            close_time TIME
        );
        """,
        
        """
        CREATE TABLE Venue_amenities (
            venue_id INTEGER,
            amenity VARCHAR(255),
            CONSTRAINT PK_Venue_amenities PRIMARY KEY (venue_id, amenity),
            CONSTRAINT FK_Venue_amenities_Venue FOREIGN KEY (venue_id) REFERENCES Venue(venue_id),
            CONSTRAINT CHK_Venue_Amenities CHECK (amenity IN ('Dressing Room', 'Kitchen', 'Projector/Screen', 'Stage'))
        );
        """,
        
        """
        CREATE TABLE Customer (
            customer_id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            phone_number VARCHAR(12),
            email VARCHAR(255)
        );
        """,
        
        """
        CREATE TABLE Organizer (
            organizer_id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            phone_number VARCHAR(12),
            commission NUMERIC(10, 2)
        );
        """,
        
        """
        CREATE TABLE Staff (
            employee_id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            role VARCHAR(255),
            wage NUMERIC(5, 2),
            CONSTRAINT CHK_Staff_Role CHECK (role IN ('Cleaning', 'Decorator', 'IT', 'Photography', 'Cleaner'))
        );
        """,
        
        """
        CREATE TABLE Caterer (
            caterer_id SERIAL PRIMARY KEY,
            business_name VARCHAR(255),
            location VARCHAR(255),
            cuisine VARCHAR(255),
            phone_number VARCHAR(12),
            price_per_order NUMERIC(5, 2),
            needs_kitchen BOOLEAN
        );
        """,
        
        """
        CREATE TABLE Reservation (
            booking_id SERIAL PRIMARY KEY,
            date DATE,
            number_of_guests INTEGER,
            start_time TIME,
            end_time TIME,
            venue_id INTEGER REFERENCES Venue(venue_id),
            organizer_id INTEGER REFERENCES Organizer(organizer_id),
            caterer_id INTEGER REFERENCES Caterer(caterer_id),
            customer_id INTEGER REFERENCES Customer(customer_id)
        );
        """,
        
        """
        CREATE TABLE Party (
            booking_id INTEGER,
            party_id INTEGER,
            type VARCHAR(255),
            description TEXT,
            CONSTRAINT PK_Party PRIMARY KEY (booking_id, party_id),
            CONSTRAINT FK_Party_Reservation FOREIGN KEY (booking_id) REFERENCES Reservation(booking_id),
            CONSTRAINT CHK_Party_Type CHECK (type IN ('Graduation', 'Wedding', 'Corporate', 'Birthday', 'Quinceañera', 'Holiday', 'Baby Shower', 'Misc', 'Anniversary'))
        );
        """,
        
        """
        CREATE TABLE Party_Decorations (
            decoration_id SERIAL PRIMARY KEY,
            booking_id INTEGER,
            party_id INTEGER,
            description TEXT,
            CONSTRAINT FK_Party_Decorations_Party FOREIGN KEY (booking_id, party_id) REFERENCES Party(booking_id, party_id)
        );
        """,
        
        """
        CREATE TABLE Party_GuestOfHonor (
            guest_id SERIAL PRIMARY KEY,
            booking_id INTEGER,
            party_id INTEGER,
            name VARCHAR(255),
            CONSTRAINT FK_Party_GuestOfHonor_Party FOREIGN KEY (booking_id, party_id) REFERENCES Party(booking_id, party_id)
        );
        """,
        
        """
        CREATE TABLE Performers (
            performer_id SERIAL PRIMARY KEY,
            cost NUMERIC(10, 2),
            name VARCHAR(255),
            email VARCHAR(255),
            type VARCHAR(255)
        );
        """,
        
        """
        CREATE TABLE Reservation_Staff (
            booking_id INTEGER,
            staff_id INTEGER,
            CONSTRAINT PK_Reservation_Staff PRIMARY KEY (booking_id, staff_id),
            CONSTRAINT FK_Reservation_Staff_Reservation FOREIGN KEY (booking_id) REFERENCES Reservation(booking_id),
            CONSTRAINT FK_Reservation_Staff_Staff FOREIGN KEY (staff_id) REFERENCES Staff(employee_id)
        );
        """,
        
        """
        CREATE TABLE Reservation_Performers (
            booking_id INTEGER,
            performer_id INTEGER,
            CONSTRAINT PK_Reservation_Performers PRIMARY KEY (booking_id, performer_id),
            CONSTRAINT FK_Reservation_Performers_Reservation FOREIGN KEY (booking_id) REFERENCES Reservation(booking_id),
            CONSTRAINT FK_Reservation_Performers_Performers FOREIGN KEY (performer_id) REFERENCES Performers(performer_id)
        );
        """
    ]
    
    with engine.connect() as conn:
        for command in commands:
            try:
                conn.execute(text(command))
                conn.commit()
                print(f"Successfully executed: {command[:50]}...")
            except Exception as e:
                print(f"Error executing: {command[:50]}...")
                print(f"Error message: {str(e)}")
                return False
        return True

if __name__ == "__main__":
    if create_schema():
        print("Schema creation completed successfully!")
    else:
        print("Schema creation failed!")