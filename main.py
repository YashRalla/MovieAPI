# Before attempting to access the API, make sure to run 'uvicorn main:app --reload' in the terminal first!
# For a documented approach, type http://127.0.0.1:8000/docs
# Else for a simple list, type http://127.0.0.1:8000/<whatever is in the GET parentheses>

import contextlib
from fastapi import FastAPI, HTTPException, Query
from azure.cosmos import CosmosClient, PartitionKey
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
import os
# Test comment

uri = os.getenv('URI')
primary_key = os.getenv('PRIMARY_KEY')

app = FastAPI()
client = CosmosClient(uri, primary_key)

database_name = "SLMAPI"
database = client.get_database_client(database_name)

container_name = "SLMC1"
container = database.get_container_client(container_name)

@app.get('/all_movies/')
def get_movies():
    query = "SELECT * FROM c" # Query to select all items, c being the container

    movies = list(container.query_items(query=query, enable_cross_partition_query=True))
    if not movies:
        raise HTTPException(status_code=404, detail="Movies not found")
    return movies

@app.get("/movies/year/{Year}")
def get_movies_year(Year: int):
    query = f"SELECT * FROM c WHERE c.Year = {Year}"  # Query to select movies for a specific year
    
    # Query the container for movies from the specified year
    movies = list(container.query_items(query=query, enable_cross_partition_query=True))

    if not movies:
        raise HTTPException(status_code=404, detail=f"No movies found for the year {Year}")
    
    return movies