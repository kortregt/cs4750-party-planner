from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from database import engine
from sqlalchemy import text

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Party Planning System</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px auto;
                    max-width: 800px;
                    padding: 20px;
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <h1>Party Planning System</h1>
            <p>Welcome to our party planning service!</p>
            <p>Site is live!</p>
        </body>
    </html>
    """

@app.get("/test-db")
async def test_db():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.scalar()
            return {"status": "success", "version": version}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )