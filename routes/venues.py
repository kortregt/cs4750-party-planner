from fastapi import APIRouter, HTTPException
from sqlalchemy import select, text
from database import SessionLocal, engine, table_venue
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/venues")
def get_all_venues():
    session = SessionLocal()
    try:
        query = select(table_venue)
        result = session.execute(query)
        venues = result.fetchall()
        return {
            "venues": [
                {
                    "venue_id": venue[0],
                    "name": venue[1],
                    "location": venue[2],
                    "cost": float(venue[3]),
                    "max_capacity": venue[4]
                }
                for venue in venues
            ]
        }
    finally:
        session.close()

@router.get("/venues/{venue_id}/check-availability")
async def check_venue_availability(
    venue_id: int,
    check_date: str,
    start_time: str,
    end_time: str
):
    try:
        query = """
        SELECT * FROM dbo.ListOverlappingReservations(
            :venue_id, :check_date, :start_time, :end_time
        )
        """
        with engine.connect() as conn:
            result = conn.execute(
                text(query),
                {
                    "venue_id": venue_id,
                    "check_date": check_date,
                    "start_time": start_time,
                    "end_time": end_time
                }
            )
            conflicts = result.fetchall()
            return {"conflicts": [dict(row) for row in conflicts]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/venues", response_class=HTMLResponse)
async def venues_page():
    session = SessionLocal()
    try:
        query = """
            SELECT v.name, v.location, v.cost, v.max_capacity,
                   string_agg(va.amenity, ', ') as amenities
            FROM venue v
            LEFT JOIN venue_amenities va ON v.venue_id = va.venue_id
            GROUP BY v.venue_id, v.name, v.location, v.cost, v.max_capacity
        """
        result = session.execute(text(query))
        venues = result.fetchall()
        
        venue_rows = "".join([
            f"<tr><td>{v.name}</td><td>{v.location}</td>"
            f"<td>${v.cost}</td><td>{v.max_capacity}</td>"
            f"<td>{v.amenities or 'None'}</td></tr>"
            for v in venues
        ])
        
        return f"""
        <html>
            <body>
                <h1>Venues</h1>
                <table border="1">
                    <tr>
                        <th>Name</th>
                        <th>Location</th>
                        <th>Cost</th>
                        <th>Capacity</th>
                        <th>Amenities</th>
                    </tr>
                    {venue_rows}
                </table>
                <p><a href="/">Home</a></p>
            </body>
        </html>
        """
    finally:
        session.close()