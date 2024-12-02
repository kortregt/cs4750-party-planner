from fastapi import APIRouter, Request, HTTPException, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, delete, update, text
from database import SessionLocal, engine, table_reservation
from datetime import datetime
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/events", response_class=HTMLResponse)
async def events_list(request: Request):
    session = SessionLocal()
    try:
        query = text("""
            SELECT 
                r.booking_id,
                to_char(r.date, 'YYYY-MM-DD') as date,
                to_char(r.start_time, 'HH24:MI') as start_time,
                to_char(r.end_time, 'HH24:MI') as end_time,
                v.name as venue_name,
                p.type as event_type,
                c.name as customer_name,
                r.number_of_guests
            FROM reservation r
            JOIN venue v ON r.venue_id = v.venue_id
            LEFT JOIN party p ON r.booking_id = p.booking_id
            JOIN customer c ON r.customer_id = c.customer_id
            ORDER BY r.date, r.start_time
        """)
        result = session.execute(query)
        events = result.fetchall()
        return templates.TemplateResponse(
            "events/index.html",
            {"request": request, "events": events}
        )
    finally:
        session.close()

@router.get("/events/add", response_class=HTMLResponse)
async def events_add_form(request: Request):
    session = SessionLocal()
    try:
        # Get venues for dropdown
        venues_query = text("SELECT venue_id, name FROM venue ORDER BY name")
        venues = session.execute(venues_query).fetchall()
        
        # Get customers for dropdown
        customers_query = text("SELECT customer_id, name FROM customer ORDER BY name")
        customers = session.execute(customers_query).fetchall()
        
        return templates.TemplateResponse(
            "events/add.html",
            {
                "request": request,
                "venues": venues,
                "customers": customers
            }
        )
    finally:
        session.close()

@router.post("/events/add")
async def events_add(
    request: Request,
    venue_id: int = Form(...),
    date: str = Form(...),
    start_time: str = Form(...),
    end_time: str = Form(...),
    number_of_guests: int = Form(...),
    customer_id: int = Form(...),
    event_type: str = Form(...)
):
    session = SessionLocal()
    try:
        query = text("""
            INSERT INTO reservation (venue_id, date, start_time, end_time, number_of_guests, customer_id)
            VALUES (:venue_id, :date, :start_time, :end_time, :number_of_guests, :customer_id)
            RETURNING booking_id
        """)
        
        result = session.execute(
            query,
            {
                "venue_id": venue_id,
                "date": date,
                "start_time": start_time,
                "end_time": end_time,
                "number_of_guests": number_of_guests,
                "customer_id": customer_id
            }
        )
        booking_id = result.scalar()
        
        if event_type:
            party_query = text("""
                INSERT INTO party (booking_id, type)
                VALUES (:booking_id, :type)
            """)
            session.execute(party_query, {"booking_id": booking_id, "type": event_type})
        
        session.commit()
        return RedirectResponse(url="/events", status_code=303)
    except Exception as e:
        session.rollback()
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=400
        )
    finally:
        session.close()

@router.get("/events/{booking_id}/edit", response_class=HTMLResponse)
async def events_edit_form(request: Request, booking_id: int):
    session = SessionLocal()
    try:
        query = text("""
            SELECT 
                r.booking_id,
                r.venue_id,
                r.customer_id,
                to_char(r.date, 'YYYY-MM-DD') as date,
                to_char(r.start_time, 'HH24:MI') as start_time,
                to_char(r.end_time, 'HH24:MI') as end_time,
                r.number_of_guests,
                p.type as event_type
            FROM reservation r
            LEFT JOIN party p ON r.booking_id = p.booking_id
            WHERE r.booking_id = :booking_id
        """)
        result = session.execute(query, {"booking_id": booking_id})
        event = result.fetchone()
        
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Get venues and customers for dropdowns
        venues_query = text("SELECT venue_id, name FROM venue ORDER BY name")
        venues = session.execute(venues_query).fetchall()
        
        customers_query = text("SELECT customer_id, name FROM customer ORDER BY name")
        customers = session.execute(customers_query).fetchall()
        
        return templates.TemplateResponse(
            "events/edit.html",
            {
                "request": request,
                "event": event,
                "venues": venues,
                "customers": customers
            }
        )
    finally:
        session.close()

@router.post("/events/{booking_id}/edit")
async def events_edit(
    request: Request,
    booking_id: int,
    venue_id: int = Form(...),
    date: str = Form(...),
    start_time: str = Form(...),
    end_time: str = Form(...),
    number_of_guests: int = Form(...),
    customer_id: int = Form(...),
    event_type: str = Form(...)
):
    session = SessionLocal()
    try:
        # Update reservation
        query = text("""
            UPDATE reservation
            SET venue_id = :venue_id,
                date = :date,
                start_time = :start_time,
                end_time = :end_time,
                number_of_guests = :number_of_guests,
                customer_id = :customer_id
            WHERE booking_id = :booking_id
        """)
        
        session.execute(
            query,
            {
                "booking_id": booking_id,
                "venue_id": venue_id,
                "date": date,
                "start_time": start_time,
                "end_time": end_time,
                "number_of_guests": number_of_guests,
                "customer_id": customer_id
            }
        )
        
        # Update or insert party type
        if event_type:
            party_query = text("""
                INSERT INTO party (booking_id, type)
                VALUES (:booking_id, :type)
                ON CONFLICT (booking_id) DO UPDATE
                SET type = :type
            """)
            session.execute(party_query, {"booking_id": booking_id, "type": event_type})
        
        session.commit()
        return RedirectResponse(url="/events", status_code=303)
    except Exception as e:
        session.rollback()
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=400
        )
    finally:
        session.close()

@router.post("/events/{booking_id}/delete")
async def events_delete(request: Request, booking_id: int):
    session = SessionLocal()
    try:
        # Delete party first (if exists) due to foreign key constraint
        party_query = text("DELETE FROM party WHERE booking_id = :booking_id")
        session.execute(party_query, {"booking_id": booking_id})
        
        # Then delete reservation
        query = text("DELETE FROM reservation WHERE booking_id = :booking_id")
        result = session.execute(query, {"booking_id": booking_id})
        
        session.commit()
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Event not found")
        return RedirectResponse(url="/events", status_code=303)
    except Exception as e:
        session.rollback()
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=400
        )
    finally:
        session.close()
