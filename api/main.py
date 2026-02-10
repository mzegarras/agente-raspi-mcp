# main.py

from fastapi import FastAPI
from item import DoorRequest
from client import MQClient
from dotenv import load_dotenv
import os


load_dotenv()

host = os.environ.get("MQTT_HOST")
port = int(os.environ.get("MQTT_PORT"))
client_id = os.environ.get("MQTT_CLIENTID")
userName = os.environ.get("MQTT_USERNAME")
password = os.environ.get("MQTT_PASSWORD")



# Create a FastAPI "instance"
app = FastAPI()
client = MQClient(host,port,client_id,userName,password)
client.start()
# Define a path operation decorator for a GET request to the root URL "/"
@app.get("/")
def read_root():
    """
    Handle GET requests to the root endpoint.
    """
    return {"Hello": "World"}


# 2. Crear el endpoint POST
@app.post("/doors")
async def door_action(item: DoorRequest):
    # FastAPI valida el JSON recibido y lo convierte en el objeto 'item'
    client.publish(item.houseId,item.doorId,item.accion.value)
    return {"action": item.accion.value, "house": item.houseId, "door": item.doorId}