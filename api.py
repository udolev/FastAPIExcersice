from fastapi import FastAPI, HTTPException, status

from enum import Enum

from pydantic import BaseModel, Field

import logging

logging.basicConfig(filename='api.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG) 

app = FastAPI()

class Color(str, Enum):
    black = "black"
    white = "white"
    golden = "golden"

class Dog(BaseModel):
    name:str = Field(max_length=20)
    age:float = Field(gt=0)
    color:Color
    owner:str = Field(max_length=20)
        
dogs = {}
id = 0

# Create (POST)
@app.post('/dogs/', status_code=status.HTTP_201_CREATED)
async def add_dog(dog:Dog):
    global id
    logger.debug(f"dogs_dict(pre-post): {dogs}\n id = {id}")
    dogs[id] = dog
    id += 1
    logger.debug(f"dogs_dict(pro-post): {dogs}\n id = {id}")
    logger.info(f"added dog {id}")
    return {id:dog}

# Read (GET)
@app.get('/dogs/')
async def root():
    logger.debug(f"dogs_dict: {dogs}\n id = {id}")
    logger.info("getting all dogs")
    return {"dogs":dogs}

@app.get('/dogs/{dog_id}')
async def get_dog_by_id(dog_id:int):
    logger.debug(f"dogs_dict: {dogs}\n id = {id}")
    if dog_id not in dogs:
        logger.error(f"dog_id {dog_id} does not exist, status code: 404")
        raise HTTPException(status_code=404, detail=f"dog_id {dog_id} does not exist")
    logger.info(f"getting dog {id}")
    return dogs[dog_id]

# Update (PUT)
@app.put('/dogs/{dog_id}')
async def update_dog(dog_id:int, dog:Dog):
    logger.debug(f"dogs_dict(pre-update): {dogs}\n id = {id}")
    if not dog_id in dogs:
        logger.error(f"dog_id {dog_id} does not exist, status code: 404")
        raise HTTPException(status_code=404, detail=f"dog_id {dog_id} does not exist")
    dogs.update({dog_id:dog})
    logger.debug(f"dogs_dict(pro-update): {dogs}\n id = {id}")
    logger.info(f"updated dog {id}")
    return {dog_id:dog}

# Delete (DELETE)
@app.delete('/dogs/')
async def delete_all_dogs():
    logger.debug(f"dogs_dict(pre-deleteAll): {dogs}\n id = {id}")
    dogs.clear()
    logger.debug(f"dogs_dict(pro-deleteAll): {dogs}\n id = {id}")
    logger.info(f"deleted all dogs")
    return "all dogs successfuly delted"

@app.delete('/dogs/{dog_id}')
async def delete_dog_by_dog_id(dog_id:int):
    logger.debug(f"dogs_dict(pre-delete): {dogs}\n id = {id}")
    if not dog_id in dogs:
        logger.error(f"dog_id {dog_id} does not exist, status code: 404")
        raise HTTPException(status_code=404, detail=f"dog_id {dog_id} does not exist. It can't be delted...")
    del dogs[dog_id]
    logger.debug(f"dogs_dict(pro-delete): {dogs}\n id = {id}")
    logger.debug(f"deleted dog {id}")
    return f'dog_id {dog_id} successfuly delted'