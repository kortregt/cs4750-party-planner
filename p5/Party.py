from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import MetaData, Table, select, text
from sqlalchemy.exc import SQLAlchemyError

#import from other .py files
from database import engine, SessionLocal

#Metadata setup
metadata_obj = MetaData()
metadata_obj.reflect(bind=engine)

#app setup
app = FastAPI()


#test table
table_staff = Table('Staff', metadata_obj, autoload_with=engine)

#choose 5 tables
table_venue = Table('Venue', metadata_obj, autoload_with=engine)
table_reservation = Table('Reservation', metadata_obj, autoload_with=engine)
table_customer = Table('Customer', metadata_obj, autoload_with=engine)
table_caterer = Table('Caterer', metadata_obj, autoload_with=engine)
table_organizer = Table('Organizer', metadata_obj, autoload_with=engine)


#test staff table API
@app.get("/get-all-staff")
def get_all_staff():
    session = SessionLocal()
    try:
        query = select(table_staff)
        result = session.execute(query)

        tuples = result.fetchall()  # Fetch all rows

        # Convert rows to dictionaries using column indices
        rows_dict = [
            {
                'employee_id': row[0],
                'name': row[1],
                'role': row[2],
                'wage': row[3]
            }
            for row in tuples
        ]
        return {"staff": rows_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")
    finally:
        session.close()


#Reservation Table API
@app.post("/add-reservation-and-optional-party")
def add_reservation(
    venue_id: int,
    date: str,
    start_time: str,
    end_time: str,
    number_of_guests: int,
    organizer_id: int,
    customer_id: int,
    caterer_id: int = None,
    add_party: bool = False, #optional
    party_type: str = None, #optional
    party_description: str = None #optional
):
    session = SessionLocal()
    try:
        # Prepare the SQL query for executing the stored procedure
        query = text("""
                EXEC dbo.AddReservation
                @VenueID = :venue_id,
                @Date = :date,
                @StartTime = :start_time,
                @EndTime = :end_time,
                @NumberOfGuests = :number_of_guests,
                @CatererID = :caterer_id,
                @OrganizerID = :organizer_id,
                @CustomerID = :customer_id,
                @AddParty = :add_party,
                @PartyType = :party_type,
                @PartyDescription = :party_description
        """)

        # Execute the stored procedure with the provided parameters
        session.execute(query, {
            'venue_id': venue_id,
            'date': date,
            'start_time': start_time,
            'end_time': end_time,
            'number_of_guests': number_of_guests,
            'caterer_id': caterer_id,
            'organizer_id': organizer_id,
            'customer_id': customer_id,
            'add_party': add_party,
            'party_type': party_type,
            'party_description': party_description
        })

        session.commit()
        return {"message": "Reservation added successfully."}

    except SQLAlchemyError as e:
        session.rollback()  # Rollback in case of an error
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        session.close()

