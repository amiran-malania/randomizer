from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Annotated
import random

app = FastAPI()

items_db = []

class Item(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
        description="The item name" 
    )

class ItemResponse(BaseModel):
    message: str
    item: str

class ItemListResponse(BaseModel):
    original_order: list[str]
    randomized_order: list[str]
    count: int

class ItemUpdateResponse(BaseModel):
    message: str
    old_item: str
    new_item: str

class ItemDeleteResponse(BaseModel):
    message: str
    deleted_item: str
    remaining_items_count: int

@app.get("/")
async def home():
    return {"message" : "Welcome to the Randomizer API"}

@app.get("/random/{max_value}")
async def get_random_number(max_value: int):
    return {
            "max" : max_value,
            "random_number": random.randint(1, max_value)
            }

@app.post("/items", response_model=ItemResponse)
async def add_item(item: Item):
    if item.name in items_db:
        raise HTTPException(status_code=400, detail="Item already exists")

    items_db.append(item.name)
    return ItemResponse(
            message="Item added successfully",
            item=item.name
        )

@app.get("/items", response_model=ItemListResponse)
def get_randomized_items():
    randomized = items_db.copy()
    random.shuffle(randomized)
    return ItemListResponse(
            original_order=items_db,
            randomized_order=randomized,
            count=len(items_db)
        )

@app.put("/items/{update_item_name}", response_model=ItemUpdateResponse)
async def update_item(updated_item_name: str, item: Item):
    if update_item_name not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    if item.name in items_db:
        raise HTTPException(
                status_code=409,
                detail="An item with that name already exists"
        )

    index = items_db.index(update_item_name)
    items_db[index] = item.name

    return ItemUpdateRespnse(
        message="Item updated successfully",
        old_item=update_item_name,
        new_item=item.name
        ) 

@app.delete("/items/{item}", response_model=ItemDeleteResponse)
async def delete_item(item: str):
    if item not in items_db:
        raise HTTPExepction(status_code=404, detail="Item not found")

    items_db.remove(item)

    return ItemDeleteResponse(
            message="Item deleted successfully",
            deleted_item=item,
            remaining_items_count=len(items_db)
            )


@app.get("/random-between")
async def get_random_number_between(
        min_value: Annotated[int, Query(
            title="Minimum Value",
            description="The minimum random number",
            ge=1,
            le=1000
            )] = 1,
        max_value: Annotated[int, Query(
            title="Maximum Value",
            description="The maximum random number",
            ge=1,
            le=1000
            )] = 99
        ):
    if min_value > max_value:
        raise HTTPExeption(status_code=400, detail="min_value cannot be greater than max_value")

    return {
            "min": min_value,
            "max": max_value,
            "random_number": random.randint(min_value, max_value)
            }

