import uvicorn
from fastapi import FastAPI
from routers import auth_router, notes_router
from database.database import create_tables


app = FastAPI()

app.include_router(auth_router)
app.include_router(notes_router)

if __name__ == '__main__':
    create_tables()
    uvicorn.run(app, host="0.0.0.0", port=80)

