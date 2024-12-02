from fastapi import APIRouter, Request, HTTPException, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, delete, update, text
from database import SessionLocal
from typing import Optional

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
