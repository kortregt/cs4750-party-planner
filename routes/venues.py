from fastapi import APIRouter, Request, HTTPException
from sqlalchemy import select, text
from database import SessionLocal, engine, table_venue
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

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
async def list_venues(request: Request):
    try:
        query = "SELECT name, location, cost, max_capacity FROM venue ORDER BY name;"
        with engine.connect() as conn:
            result = conn.execute(text(query))
            venues = result.fetchall()
        return templates.TemplateResponse("venues.html", {"request": request, "venues": venues})
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})