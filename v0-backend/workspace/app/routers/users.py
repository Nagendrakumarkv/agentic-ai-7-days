from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.user import User, UserCreate, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Mock Database
db_users = []
id_counter = 1

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate):
    global id_counter
    new_user = User(id=id_counter, **user_in.model_dump())
    db_users.append(new_user)
    id_counter += 1
    return new_user

@router.get("/", response_model=List[User])
async def read_users():
    return db_users

@router.get("/{user_id}", response_model=User)
async def read_user(user_id: int):
    user = next((u for u in db_users if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_in: UserUpdate):
    user_idx = next((i for i, u in enumerate(db_users) if u.id == user_id), None)
    if user_idx is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_user_data = db_users[user_idx].model_dump()
    update_data = user_in.model_dump(exclude_unset=True)
    
    updated_user = User(**{**current_user_data, **update_data})
    db_users[user_idx] = updated_user
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    user_idx = next((i for i, u in enumerate(db_users) if u.id == user_id), None)
    if user_idx is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_users.pop(user_idx)
    return None