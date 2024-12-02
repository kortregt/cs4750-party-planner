from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routes import staff, venues, events, functions
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.include_router(staff.router)
app.include_router(venues.router)
app.include_router(events.router)
app.include_router(functions.router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})