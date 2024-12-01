from fastapi import FastAPI
from fastapi.responses import HTMLResponse

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
            <p>🎉 Site is live! 🎉</p>
        </body>
    </html>
    """