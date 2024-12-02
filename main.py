from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routes import staff, venues, events, functions

app = FastAPI()

app.include_router(staff.router)
app.include_router(venues.router)
app.include_router(events.router)
app.include_router(functions.router)

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <body>
            <h1>Party Planning System</h1>
            <ul>
                <li><a href="/venues">View Venues</a></li>
                <li><a href="/events">View Events</a></li>
                <li><a href="/staff">View Staff</a></li>
            </ul>
        </body>
    </html>
    """

@app.get("/venues", response_class=HTMLResponse)
async def list_venues():
    try:
        query = "SELECT name, location, cost, max_capacity FROM venue ORDER BY name;"
        with engine.connect() as conn:
            result = conn.execute(text(query))
            venues = result.fetchall()

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