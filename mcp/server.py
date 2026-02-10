from fastmcp import FastMCP
from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_URL = os.environ.get("API_URL")

mcp = FastMCP("MCP Server 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool
def opendoor(houseId: str, doorId: str):
   

    """
    Abrir una puerta de una casa
    
    Args:
        houseId: Id de la casa
        doorId: Id de la puerta
    
    Returns:
        Confirmación de la puerta abierta
    """

    json_payload = {"houseId":houseId,"doorId":doorId,"accion":"OPEN"}
    headers = {
            'Content-Type': 'application/json; charset=UTF-8',
        }
    response = requests.post(API_URL, json=json_payload,headers=headers)
    response.raise_for_status()
    data = response.json()
    
    return data

@mcp.tool
def closedoor(houseId: str, doorId: str):
   

    """
    Cierra una puerta de una casa
    
    Args:
        houseId: Id de la casa
        doorId: Id de la puerta
    
    Returns:
        Confirmación de la puerta abierta
    """

    json_payload = {"houseId":houseId,"doorId":doorId,"accion":"CLOSE"}
    headers = {
            'Content-Type': 'application/json; charset=UTF-8',
        }
    response = requests.post(API_URL, json=json_payload,headers=headers)
    response.raise_for_status()
    data = response.json()
    
    return data

if __name__ == "__main__":
    mcp.run(transport="http",host="0.0.0.0",port=9000,path="/mcp")