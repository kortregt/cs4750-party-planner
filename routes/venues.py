from fastapi import APIRouter, Request, HTTPException, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, delete, update, text
from database import SessionLocal, engine, table_venue
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/venues", response_class=HTMLResponse)
async def venues_list(request: Request):
    session = SessionLocal()
    try:
        query = text("""
            SELECT venue_id, name, location, cost, max_capacity 
            FROM venue 
            ORDER BY name
        """)
        result = session.execute(query)
        venues = result.fetchall()
        return templates.TemplateResponse(
            "venues/index.html",
            {"request": request, "venues": venues}
        )
    finally:
        session.close()

@router.get("/venues/add", response_class=HTMLResponse)
async def venues_add_form(request: Request):
    return templates.TemplateResponse(
        "venues/add.html",
        {"request": request}
    )

@router.post("/venues/add")
async def venues_add(
    request: Request,
    name: str = Form(...),
    location: str = Form(...),
    cost: float = Form(...),
    max_capacity: int = Form(...)
):
    session = SessionLocal()
    try:
        query = text("""
            INSERT INTO venue (name, location, cost, max_capacity)
            VALUES (:name, :location, :cost, :max_capacity)
        """)
        
        session.execute(
            query,
            {
                "name": name,
                "location": location,
                "cost": cost,
                "max_capacity": max_capacity
            }
        )
        session.commit()
        return RedirectResponse(url="/venues", status_code=303)
    except Exception as e:
        session.rollback()
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=400
        )
    finally:
        session.close()

@router.get("/venues/{venue_id}/edit", response_class=HTMLResponse)
async def venues_edit_form(request: Request, venue_id: int):
    session = SessionLocal()
    try:
        query = text("""
            SELECT venue_id, name, location, cost, max_capacity
            FROM venue
            WHERE venue_id = :venue_id
        """)
        result = session.execute(query, {"venue_id": venue_id})
        venue = result.fetchone()
        
        if not venue:
            raise HTTPException(status_code=404, detail="Venue not found")
            
        return templates.TemplateResponse(
            "venues/edit.html",
            {"request": request, "venue": venue}
        )
    finally:
        session.close()

@router.post("/venues/{venue_id}/edit")
async def venues_edit(
    request: Request,
    venue_id: int,
    name: str = Form(...),
    location: str = Form(...),
    cost: float = Form(...),
    max_capacity: int = Form(...)
):
    session = SessionLocal()
    try:
        query = text("""
            UPDATE venue
            SET name = :name,
                location = :location,
                cost = :cost,
                max_capacity = :max_capacity
            WHERE venue_id = :venue_id
        """)
        
        result = session.execute(
            query,
            {
                "venue_id": venue_id,
                "name": name,
                "location": location,
                "cost": cost,
                "max_capacity": max_capacity
            }
        )
        session.commit()
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Venue not found")
        return RedirectResponse(url="/venues", status_code=303)
    except Exception as e:
        session.rollback()
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=400
        )
    finally:
        session.close()

@router.post("/venues/{venue_id}/delete")
async def venues_delete(request: Request, venue_id: int):
    session = SessionLocal()
    try:
        # Check if venue has any reservations
        check_query = text("""
            SELECT COUNT(*) FROM reservation 
            WHERE venue_id = :venue_id
        """)
        result = session.execute(check_query, {"venue_id": venue_id})
        if result.scalar() > 0:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete venue with existing reservations"
            )
        
        query = text("DELETE FROM venue WHERE venue_id = :venue_id")
        result = session.execute(query, {"venue_id": venue_id})
        session.commit()
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Venue not found")
        return RedirectResponse(url="/venues", status_code=303)
    except Exception as e:
        session.rollback()
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=400
        )
    finally:
        session.close()

@router.get("/venues/{venue_id}/check-availability")
async def check_venue_availability(
    request: Request,
    venue_id: int,
    check_date: str,
    start_time: str,
    end_time: str
):
    session = SessionLocal()
    try:
        query = text("""
            SELECT 
                to_char(r.date, 'YYYY-MM-DD') as date,
                to_char(r.start_time, 'HH24:MI') as start_time,
                to_char(r.end_time, 'HH24:MI') as end_time,
                c.name as customer_name
            FROM reservation r
            JOIN customer c ON r.customer_id = c.customer_id
            WHERE r.venue_id = :venue_id
            AND r.date = :check_date::date
            AND (
                (r.start_time, r.end_time) OVERLAPS 
                (:start_time::time, :end_time::time)
            )
        """)
        
        result = session.execute(
            query,
            {
                "venue_id": venue_id,
                "check_date": check_date,
                "start_time": start_time,
                "end_time": end_time
            }
        )
        conflicts = result.fetchall()
        return templates.TemplateResponse(
            "venues/availability.html",
            {
                "request": request,
                "conflicts": conflicts,
                "check_date": check_date,
                "start_time": start_time,
                "end_time": end_time
            }
        )
    finally:
        session.close()
