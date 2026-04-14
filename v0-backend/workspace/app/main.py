from fastapi import FastAPI
from app.routers import users

app = FastAPI(title="FastAPI CRUD API")

app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the User CRUD API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)