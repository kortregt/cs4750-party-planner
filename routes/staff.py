from fastapi import APIRouter, Request, HTTPException, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, delete, update, text
from database import SessionLocal, table_staff
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/staff", response_class=HTMLResponse)
async def staff_list(request: Request):
    session = SessionLocal()
    try:
        query = select(table_staff)
        result = session.execute(query)
        staff = result.fetchall()
        return templates.TemplateResponse(
            "staff/index.html",
            {"request": request, "staff": staff}
        )
    finally:
        session.close()

@router.get("/staff/add", response_class=HTMLResponse)
async def staff_add_form(request: Request):
    return templates.TemplateResponse("staff/add.html", {"request": request})

@router.post("/staff/add")
async def staff_add(
    request: Request,
    name: str = Form(...),
    role: str = Form(...),
    wage: float = Form(...)
):
    session = SessionLocal()
    try:
        if role not in ['Cleaning', 'Decorator', 'IT', 'Photography', 'Cleaner']:
            raise HTTPException(status_code=400, detail="Invalid role")
        
        result = session.execute(select(text("MAX(employee_id)")).select_from(table_staff))
        next_id = (result.scalar() or 5000) + 45
        
        query = table_staff.insert().values(
            employee_id=next_id,
            name=name,
            role=role,
            wage=wage
        )
        session.execute(query)
        session.commit()
        return RedirectResponse(url="/staff", status_code=303)
    except Exception as e:
        session.rollback()
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=400
        )
    finally:
        session.close()

@router.get("/staff/{employee_id}/edit", response_class=HTMLResponse)
async def staff_edit_form(request: Request, employee_id: int):
    session = SessionLocal()
    try:
        query = select(table_staff).where(table_staff.c.employee_id == employee_id)
        result = session.execute(query)
        staff = result.fetchone()
        if not staff:
            raise HTTPException(status_code=404, detail="Staff member not found")
        return templates.TemplateResponse(
            "staff/edit.html",
            {"request": request, "staff": staff}
        )
    finally:
        session.close()

@router.post("/staff/{employee_id}/edit")
async def staff_edit(
    request: Request,
    employee_id: int,
    name: str = Form(...),
    role: str = Form(...),
    wage: float = Form(...)
):
    session = SessionLocal()
    try:
        if role not in ['Cleaning', 'Decorator', 'IT', 'Photography', 'Cleaner']:
            raise HTTPException(status_code=400, detail="Invalid role")
            
        query = update(table_staff).where(table_staff.c.employee_id == employee_id).values(
            name=name,
            role=role,
            wage=wage
        )
        result = session.execute(query)
        session.commit()
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Staff member not found")
        return RedirectResponse(url="/staff", status_code=303)
    except Exception as e:
        session.rollback()
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=400
        )
    finally:
        session.close()

@router.post("/staff/{employee_id}/delete")
async def staff_delete(request: Request, employee_id: int):
    session = SessionLocal()
    try:
        query = delete(table_staff).where(table_staff.c.employee_id == employee_id)
        result = session.execute(query)
        session.commit()
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Staff member not found")
        return RedirectResponse(url="/staff", status_code=303)
    except Exception as e:
        session.rollback()
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=400
        )
    finally:
        session.close()