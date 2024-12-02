from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from database import engine
from typing import Optional
from datetime import date, time

router = APIRouter()

@app.get("/check-conflicts")
async def check_reservation_conflicts(
    venue_id: int,
    reservation_date: date,
    start_time: time,
    end_time: time
):
    query = """
    SELECT * FROM dbo.ListOverlappingReservations(
        :venue_id, :reservation_date, :start_time, :end_time
    )
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), {
                "venue_id": venue_id,
                "reservation_date": reservation_date,
                "start_time": start_time,
                "end_time": end_time
            })
            conflicts = result.fetchall()
            return {"conflicts": [dict(row) for row in conflicts]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add-reservation")
async def add_reservation(
    venue_id: int,
    date: date,
    start_time: time,
    end_time: time,
    number_of_guests: int,
    organizer_id: int,
    customer_id: int,
    caterer_id: Optional[int] = None,
    add_party: bool = False,
    party_type: Optional[str] = None,
    party_description: Optional[str] = None
):
    query = """
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
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text(query),
                {
                    "venue_id": venue_id,
                    "date": date,
                    "start_time": start_time,
                    "end_time": end_time,
                    "number_of_guests": number_of_guests,
                    "caterer_id": caterer_id,
                    "organizer_id": organizer_id,
                    "customer_id": customer_id,
                    "add_party": add_party,
                    "party_type": party_type,
                    "party_description": party_description
                }
            )
            conn.commit()
            return {"message": "Reservation added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/caterers/{venue_id}")
async def list_caterers_for_venue(venue_id: int):
    query = "SELECT * FROM dbo.ListCaterersNearThisVenue(:venue_id)"
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), {"venue_id": venue_id})
            caterers = result.fetchall()
            return {"caterers": [dict(row) for row in caterers]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test-functions", response_class=HTMLResponse)
async def test_functions_page():
    return """
    <html>
        <body>
            <h1>Test SQL Functions</h1>
            <h2>Check Caterers for Venue</h2>
            <form action="/caterers/319" method="get">
                <button type="submit">Check Caterers for Venue 319</button>
            </form>

            <h2>Check Reservation Conflicts</h2>
            <form action="/check-conflicts" method="get">
                <input type="hidden" name="venue_id" value="319">
                <input type="date" name="reservation_date" required>
                <input type="time" name="start_time" required>
                <input type="time" name="end_time" required>
                <button type="submit">Check Conflicts</button>
            </form>
        </body>
    </html>
    """