from fastapi import APIRouter, HTTPException
from sqlalchemy import select, text
from database import SessionLocal, engine, table_reservation
from fastapi.responses import HTMLResponse
from datetime import datetime

router = APIRouter()

@router.get("/events")
def get_all_events():
    session = SessionLocal()
    try:
        query = text("""
            SELECT 
                to_char(r.date, 'YYYY-MM-DD') as date,
                to_char(r.start_time, 'HH24:MI') as start_time,
                to_char(r.end_time, 'HH24:MI') as end_time,
                v.name as venue_name,
                p.type as event_type,
                c.name as customer_name
            FROM reservation r
            JOIN venue v ON r.venue_id = v.venue_id
            LEFT JOIN party p ON r.booking_id = p.booking_id
            JOIN customer c ON r.customer_id = c.customer_id
        """)
        result = session.execute(query)
        events = [dict(row._mapping) for row in result]
        return {"events": events}
    finally:
        session.close()

@router.post("/events")
async def create_event(
    venue_id: int,
    date: str,
    start_time: str,
    end_time: str,
    number_of_guests: int,
    organizer_id: int,
    customer_id: int,
    caterer_id: int = None
):
    try:
        query = """
        EXEC dbo.AddReservation 
            @VenueID = :venue_id,
            @Date = :date,
            @StartTime = :start_time,
            @EndTime = :end_time,
            @NumberOfGuests = :number_of_guests,
            @CatererID = :caterer_id,
            @OrganizerID = :organizer_id,
            @CustomerID = :customer_id
        """
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
                    "customer_id": customer_id
                }
            )
            conn.commit()
            return {"message": "Event created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/events", response_class=HTMLResponse)
async def events_page():
    session = SessionLocal()
    try:
        query = """
            SELECT r.date, r.start_time, r.end_time,
                   v.name as venue_name, p.type as event_type,
                   c.name as customer_name
            FROM reservation r
            JOIN venue v ON r.venue_id = v.venue_id
            LEFT JOIN party p ON r.booking_id = p.booking_id
            JOIN customer c ON r.customer_id = c.customer_id
            ORDER BY r.date, r.start_time
        """
        result = session.execute(text(query))
        events = result.fetchall()
        
        event_rows = "".join([
            f"<tr><td>{e.date}</td><td>{e.start_time}</td>"
            f"<td>{e.end_time}</td><td>{e.venue_name}</td>"
            f"<td>{e.event_type or 'N/A'}</td>"
            f"<td>{e.customer_name}</td></tr>"
            for e in events
        ])
        
        return f"""
        <html>
            <body>
                <h1>Events</h1>
                <table border="1">
                    <tr>
                        <th>Date</th>
                        <th>Start Time</th>
                        <th>End Time</th>
                        <th>Venue</th>
                        <th>Type</th>
                        <th>Customer</th>
                    </tr>
                    {event_rows}
                </table>
                <p><a href="/">Home</a></p>
            </body>
        </html>
        """
    finally:
        session.close()
