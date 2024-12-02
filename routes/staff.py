from fastapi import APIRouter, HTTPException
from sqlalchemy import select, delete, update
from database import SessionLocal, table_staff
from models import StaffCreate, StaffUpdate

router = APIRouter()

@router.get("/staff")
def get_all_staff():
    session = SessionLocal()
    try:
        query = select(table_staff)
        result = session.execute(query)
        staff = result.fetchall()
        return {
            "staff": [
                {
                    "employee_id": emp[0],
                    "name": emp[1],
                    "role": emp[2],
                    "wage": float(emp[3])
                }
                for emp in staff
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()