from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from database import engine
from sqlalchemy import text

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Party Planning System</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px auto;
                    max-width: 800px;
                    padding: 20px;
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <h1>Party Planning System</h1>
            <p>Welcome to our party planning service!</p>
            <p>Site is live!</p>
        </body>
    </html>
    """

@app.get("/test-db")
async def test_db():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.scalar()
            return {"status": "success", "version": version}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.get("/venues", response_class=HTMLResponse)
async def list_venues():
    try:
        query = "SELECT name, location, cost, max_capacity FROM venue ORDER BY name;"
        with engine.connect() as conn:
            result = conn.execute(text(query))
            venues = result.fetchall()

        # Build simple HTML table
        venue_rows = ""
        for venue in venues:
            venue_rows += f"<tr><td>{venue.name}</td><td>{venue.location}</td><td>${venue.cost}</td><td>{venue.max_capacity}</td></tr>"

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
                    </tr>
                    {venue_rows}
                </table>
                <p><a href="/">Back to Home</a></p>
            </body>
        </html>
        """
    except Exception as e:
        return f"<html><body><h1>Error</h1><p>{str(e)}</p></body></html>"

@app.get("/events", response_class=HTMLResponse)
async def list_events():
    try:
        query = """
            SELECT r.date, v.name as venue, p.type as event_type
            FROM reservation r
            JOIN venue v ON r.venue_id = v.venue_id
            LEFT JOIN party p ON r.booking_id = p.booking_id
            ORDER BY r.date;
        """
        with engine.connect() as conn:
            result = conn.execute(text(query))
            events = result.fetchall()

        # Build simple HTML table
        event_rows = ""
        for event in events:
            event_rows += f"<tr><td>{event.date}</td><td>{event.venue}</td><td>{event.event_type or 'N/A'}</td></tr>"

        return f"""
        <html>
            <body>
                <h1>Events</h1>
                <table border="1">
                    <tr>
                        <th>Date</th>
                        <th>Venue</th>
                        <th>Event Type</th>
                    </tr>
                    {event_rows}
                </table>
                <p><a href="/">Back to Home</a></p>
            </body>
        </html>
        """
    except Exception as e:
        return f"<html><body><h1>Error</h1><p>{str(e)}</p></body></html>"