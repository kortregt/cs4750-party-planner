from fastapi import APIRouter, Request, HTTPException, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, delete, update, text
from database import SessionLocal
from typing import Optional, List

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/parties", response_class=HTMLResponse)
async def parties_list(request: Request):
    session = SessionLocal()
    try:
        query = text("""
            SELECT 
                p.booking_id,
                p.party_id,
                p.type,
                p.description,
                r.date,
                v.name as venue_name,
                c.name as customer_name,
                (
                    SELECT string_agg(name, ', ')
                    FROM party_guestofhonor
                    WHERE booking_id = p.booking_id AND party_id = p.party_id
                ) as guests_of_honor,
                (
                    SELECT string_agg(description, ', ')
                    FROM party_decorations
                    WHERE booking_id = p.booking_id AND party_id = p.party_id
                ) as decorations
            FROM party p
            JOIN reservation r ON p.booking_id = r.booking_id
            JOIN venue v ON r.venue_id = v.venue_id
            JOIN customer c ON r.customer_id = c.customer_id
            ORDER BY r.date DESC
        """)
        result = session.execute(query)
        parties = result.fetchall()
        return templates.TemplateResponse(
            "parties/index.html",
            {"request": request, "parties": parties}
        )
    finally:
        session.close()

@router.get("/parties/add", response_class=HTMLResponse)
async def parties_add_form(request: Request):
    session = SessionLocal()
    try:
        # Get venues for dropdown
        venues_query = text("SELECT venue_id, name FROM venue ORDER BY name")
        venues = session.execute(venues_query).fetchall()
        
        # Get customers for dropdown
        customers_query = text("SELECT customer_id, name FROM customer ORDER BY name")
        customers = session.execute(customers_query).fetchall()
        
        return templates.TemplateResponse(
            "parties/add.html",
            {
                "request": request,
                "venues": venues,
                "customers": customers
            }
        )
    finally:
        session.close()

@router.post("/parties/add")
async def parties_add(
    request: Request,
    venue_id: int = Form(...),
    customer_id: int = Form(...),
    date: str = Form(...),
    start_time: str = Form(...),
    end_time: str = Form(...),
    number_of_guests: int = Form(...),
    type: str = Form(...),
    description: str = Form(None),
    guest_names: str = Form(""),
    decoration_descriptions: str = Form("")
):
    session = SessionLocal()
    try:
        # Validate venue exists
        venue_check = text("SELECT 1 FROM venue WHERE venue_id = :venue_id")
        if not session.execute(venue_check, {"venue_id": venue_id}).scalar():
            raise HTTPException(status_code=400, detail="Invalid venue ID")

        # Check venue capacity
        capacity_check = text("""
            SELECT max_capacity 
            FROM venue 
            WHERE venue_id = :venue_id AND max_capacity >= :guests
        """)
        if not session.execute(capacity_check, {
            "venue_id": venue_id,
            "guests": number_of_guests
        }).scalar():
            raise HTTPException(status_code=400, detail="Number of guests exceeds venue capacity")

        # Check for scheduling conflicts
        conflict_check = text("""
            SELECT 1 
            FROM reservation 
            WHERE venue_id = :venue_id 
            AND date = :date 
            AND (start_time, end_time) OVERLAPS 
                (CAST(:start_time AS TIME), CAST(:end_time AS TIME))
        """)
        if session.execute(conflict_check, {
            "venue_id": venue_id,
            "date": date,
            "start_time": start_time,
            "end_time": end_time
        }).scalar():
            raise HTTPException(status_code=400, detail="Time slot conflicts with existing reservation")

        # Insert reservation
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
        
        # Get next party_id
        party_id_query = text("""
            SELECT COALESCE(MAX(party_id), 0) + 1 
            FROM party 
            WHERE booking_id = :booking_id
        """)
        party_id = session.execute(party_id_query, {"booking_id": booking_id}).scalar()

        # Insert party
        party_query = text("""
            INSERT INTO party (booking_id, party_id, type, description)
            VALUES (:booking_id, :party_id, :type, :description)
        """)
        session.execute(
            party_query,
            {
                "booking_id": booking_id,
                "party_id": party_id,
                "type": type,
                "description": description
            }
        )

        # Insert guests of honor
        if guest_names:
            for name in guest_names.split('\n'):
                if name.strip():
                    session.execute(
                        text("""
                            INSERT INTO party_guestofhonor (booking_id, party_id, name)
                            VALUES (:booking_id, :party_id, :name)
                        """),
                        {"booking_id": booking_id, "party_id": party_id, "name": name.strip()}
                    )

        # Insert decorations
        if decoration_descriptions:
            for desc in decoration_descriptions.split('\n'):
                if desc.strip():
                    session.execute(
                        text("""
                            INSERT INTO party_decorations (booking_id, party_id, description)
                            VALUES (:booking_id, :party_id, :description)
                        """),
                        {"booking_id": booking_id, "party_id": party_id, "description": desc.strip()}
                    )

        session.commit()
        return RedirectResponse(url="/parties", status_code=303)
    except Exception as e:
        session.rollback()
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=400
        )
    finally:
        session.close()

@router.get("/parties/{booking_id}/{party_id}/edit", response_class=HTMLResponse)
async def parties_edit_form(request: Request, booking_id: int, party_id: int):
    session = SessionLocal()
    try:
        # Get party details including guests and decorations
        query = text("""
            SELECT 
                p.booking_id,
                p.party_id,
                p.type,
                p.description,
                r.date,
                v.name as venue_name,
                c.name as customer_name
            FROM party p
            JOIN reservation r ON p.booking_id = r.booking_id
            JOIN venue v ON r.venue_id = v.venue_id
            JOIN customer c ON r.customer_id = c.customer_id
            WHERE p.booking_id = :booking_id AND p.party_id = :party_id
        """)
        result = session.execute(query, {"booking_id": booking_id, "party_id": party_id})
        party = result.fetchone()
        
        if not party:
            raise HTTPException(status_code=404, detail="Party not found")

        # Get guests of honor
        guests_query = text("""
            SELECT guest_id, name
            FROM party_guestofhonor
            WHERE booking_id = :booking_id AND party_id = :party_id
        """)
        guests = session.execute(guests_query, {"booking_id": booking_id, "party_id": party_id}).fetchall()

        # Get decorations
        decorations_query = text("""
            SELECT decoration_id, description
            FROM party_decorations
            WHERE booking_id = :booking_id AND party_id = :party_id
        """)
        decorations = session.execute(decorations_query, {"booking_id": booking_id, "party_id": party_id}).fetchall()
        
        return templates.TemplateResponse(
            "parties/edit.html",
            {
                "request": request,
                "party": party,
                "guests": guests,
                "decorations": decorations
            }
        )
    finally:
        session.close()

@router.post("/parties/{booking_id}/{party_id}/edit")
async def parties_edit(
    request: Request,
    booking_id: int,
    party_id: int,
    type: str = Form(...),
    description: str = Form(None),
    guest_names: list[str] = Form([]),
    decoration_descriptions: list[str] = Form([])
):
    session = SessionLocal()
    try:
        # Update party
        party_query = text("""
            UPDATE party
            SET type = :type,
                description = :description
            WHERE booking_id = :booking_id AND party_id = :party_id
        """)
        session.execute(
            party_query,
            {
                "booking_id": booking_id,
                "party_id": party_id,
                "type": type,
                "description": description
            }
        )

        # Delete existing guests and decorations
        session.execute(
            text("DELETE FROM party_guestofhonor WHERE booking_id = :booking_id AND party_id = :party_id"),
            {"booking_id": booking_id, "party_id": party_id}
        )
        session.execute(
            text("DELETE FROM party_decorations WHERE booking_id = :booking_id AND party_id = :party_id"),
            {"booking_id": booking_id, "party_id": party_id}
        )

        # Insert new guests
        if guest_names:
            for name in guest_names:
                if name.strip():
                    session.execute(
                        text("""
                            INSERT INTO party_guestofhonor (booking_id, party_id, name)
                            VALUES (:booking_id, :party_id, :name)
                        """),
                        {"booking_id": booking_id, "party_id": party_id, "name": name.strip()}
                    )

        # Insert new decorations
        if decoration_descriptions:
            for description in decoration_descriptions:
                if description.strip():
                    session.execute(
                        text("""
                            INSERT INTO party_decorations (booking_id, party_id, description)
                            VALUES (:booking_id, :party_id, :description)
                        """),
                        {"booking_id": booking_id, "party_id": party_id, "description": description.strip()}
                    )

        session.commit()
        return RedirectResponse(url="/parties", status_code=303)
    except Exception as e:
        session.rollback()
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=400
        )
    finally:
        session.close()

@router.post("/parties/{booking_id}/{party_id}/delete")
async def parties_delete(request: Request, booking_id: int, party_id: int):
    session = SessionLocal()
    try:
        # Delete guests of honor and decorations first
        session.execute(
            text("DELETE FROM party_guestofhonor WHERE booking_id = :booking_id AND party_id = :party_id"),
            {"booking_id": booking_id, "party_id": party_id}
        )
        session.execute(
            text("DELETE FROM party_decorations WHERE booking_id = :booking_id AND party_id = :party_id"),
            {"booking_id": booking_id, "party_id": party_id}
        )
        
        # Delete party
        session.execute(
            text("DELETE FROM party WHERE booking_id = :booking_id AND party_id = :party_id"),
            {"booking_id": booking_id, "party_id": party_id}
        )
        
        # Delete reservation
        session.execute(
            text("DELETE FROM reservation WHERE booking_id = :booking_id"),
            {"booking_id": booking_id}
        )
        
        session.commit()
        return RedirectResponse(url="/parties", status_code=303)
    except Exception as e:
        session.rollback()
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=400
        )
    finally:
        session.close()

@router.post("/parties/{booking_id}/{party_id}/guests/add")
async def add_guest(
    request: Request,
    booking_id: int,
    party_id: int,
    name: str = Form(...)
):
    session = SessionLocal()
    try:
        query = text("""
            INSERT INTO party_guestofhonor (booking_id, party_id, name)
            VALUES (:booking_id, :party_id, :name)
        """)
        session.execute(
            query,
            {
                "booking_id": booking_id,
                "party_id": party_id,
                "name": name
            }
        )
        session.commit()
        return RedirectResponse(url=f"/parties/{booking_id}/{party_id}/edit", status_code=303)
    except Exception as e:
        session.rollback()
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=400
        )
    finally:
        session.close()

@router.post("/parties/{booking_id}/{party_id}/decorations/add")
async def add_decoration(
    request: Request,
    booking_id: int,
    party_id: int,
    description: str = Form(...)
):
    session = SessionLocal()
    try:
        query = text("""
            INSERT INTO party_decorations (booking_id, party_id, description)
            VALUES (:booking_id, :party_id, :description)
        """)
        session.execute(
            query,
            {
                "booking_id": booking_id,
                "party_id": party_id,
                "description": description
            }
        )
        session.commit()
        return RedirectResponse(url=f"/parties/{booking_id}/{party_id}/edit", status_code=303)
    except Exception as e:
        session.rollback()
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=400
        )
    finally:
        session.close()
