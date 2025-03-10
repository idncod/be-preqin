from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from models import User
from api_helper import ApiHelper

app = FastAPI()
api_helper = ApiHelper()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_api_helper():
    return ApiHelper()

@app.get("/users")
async def get_users(
    limit: int = Query(5, description="Number of users to fetch"),
    last_evaluated_key: dict = None,
    api: ApiHelper = Depends(get_api_helper)
):
    result = api.get_users(limit=limit, last_evaluated_key=last_evaluated_key)
    return result

@app.post("/users", response_model=User)
async def add_user(user: User, api: ApiHelper = Depends(get_api_helper)):
    return api.add_user(user)

@app.put("/users/{uuid}", response_model=User)
async def update_user(uuid: str, user: User, api: ApiHelper = Depends(get_api_helper)):
    return api.update_user(uuid, user)

handler = Mangum(app)


