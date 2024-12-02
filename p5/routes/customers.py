from fastapi import APIRouter, Request, HTTPException, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, delete, update, text
from database import SessionLocal
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/customers", response_class=HTMLResponse)
async def customers_list(request: Request):
    session = SessionLocal()
    try:
        query = text("""
            SELECT customer_id, name, phone_number, email 
            FROM customer 
            ORDER BY name
        """)
        result = session.execute(query)
        customers = result.fetchall()
        return templates.TemplateResponse(
            "customers/index.html",
            {"request": request, "customers": customers}
        )
    finally:
        session.close()

@router.get("/customers/add", response_class=HTMLResponse)
async def customers_add_form(request: Request):
    return templates.TemplateResponse(
        "customers/add.html",
        {"request": request}
    )

@router.post("/customers/add")
async def customers_add(
    request: Request,
    name: str = Form(...),
    phone_number: str = Form(...),
    email: str = Form(...)
):
    session = SessionLocal()
    try:
        query = text("""
            INSERT INTO customer (name, phone_number, email)
            VALUES (:name, :phone_number, :email)
        """)
        
        session.execute(
            query,
            {
                "name": name,
                "phone_number": phone_number,
                "email": email
            }
        )
        session.commit()
        return RedirectResponse(url="/customers", status_code=303)
    except Exception as e:
        session.rollback()
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=400
        )
    finally:
        session.close()

@router.get("/customers/{customer_id}/edit", response_class=HTMLResponse)
async def customers_edit_form(request: Request, customer_id: int):
    session = SessionLocal()
    try:
        query = text("""
            SELECT customer_id, name, phone_number, email
            FROM customer
            WHERE customer_id = :customer_id
        """)
        result = session.execute(query, {"customer_id": customer_id})
        customer = result.fetchone()
        
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
            
        return templates.TemplateResponse(
            "customers/edit.html",
            {"request": request, "customer": customer}
        )
    finally:
        session.close()

@router.post("/customers/{customer_id}/edit")
async def customers_edit(
    request: Request,
    customer_id: int,
    name: str = Form(...),
    phone_number: str = Form(...),
    email: str = Form(...)
):
    session = SessionLocal()
    try:
        query = text("""
            UPDATE customer
            SET name = :name,
                phone_number = :phone_number,
                email = :email
            WHERE customer_id = :customer_id
        """)
        
        result = session.execute(
            query,
            {
                "customer_id": customer_id,
                "name": name,
                "phone_number": phone_number,
                "email": email
            }
        )
        session.commit()
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Customer not found")
        return RedirectResponse(url="/customers", status_code=303)
    except Exception as e:
        session.rollback()
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=400
        )
    finally:
        session.close()

@router.post("/customers/{customer_id}/delete")
async def customers_delete(request: Request, customer_id: int):
    session = SessionLocal()
    try:
        # Check if customer has any reservations
        check_query = text("""
            SELECT COUNT(*) FROM reservation 
            WHERE customer_id = :customer_id
        """)
        result = session.execute(check_query, {"customer_id": customer_id})
        if result.scalar() > 0:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete customer with existing reservations"
            )
        
        query = text("DELETE FROM customer WHERE customer_id = :customer_id")
        result = session.execute(query, {"customer_id": customer_id})
        session.commit()
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Customer not found")
        return RedirectResponse(url="/customers", status_code=303)
    except Exception as e:
        session.rollback()
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=400
        )
    finally:
        session.close()
