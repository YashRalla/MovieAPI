from azure.cosmos import CosmosClient, PartitionKey
import json
import os
# Test comment

uri = os.getenv('URI')
primary_key = os.getenv('PRIMARY_KEY')

client = CosmosClient(uri, primary_key)

database_name = "SLMAPI"
database = client.create_database_if_not_exists(id=database_name)
database = client.get_database_client(database_name)

container_name = "SLMC1"
container = database.create_container_if_not_exists(
    id=container_name,
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)
container = database.get_container_client(container_name)

with open("movies.json", "r") as f:
    movie_data = json.load(f)

for index, item in enumerate(movie_data):
    # Generate a unique id by combining the title and index
    item['id'] = f"{item['Title'].replace(' ', '_').lower()}_{item['Year']}_{index}"
    try:
        container.create_item(body=item)
        print(f"Inserted item with id: {item['id']}")
    except Exception as e:
        print(f"Error inserting item with id {item['id']}: {e}")