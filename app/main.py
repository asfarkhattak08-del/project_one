from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import users, auth
from app.db.session import Base, engine
from app import models


app = FastAPI()


Base.metadata.create_all(bind=engine)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "hello Asfar Khattak"}


app.include_router(auth.router)
app.include_router(users.router)