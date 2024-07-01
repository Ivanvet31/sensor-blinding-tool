from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional


app = FastAPI()
address: Optional[str] = None
allowed_ips = {"ai-poly.online", "botnet.ai-poly.online", "109.71.242.119", "127.0.0.1", "localhost"}


class AddressRequest(BaseModel):
    address: str


@app.get("/address", response_model=str)
async def get_address():
    if address:
        return address
    else:
        raise HTTPException(status_code=404, detail="Address not set")


@app.post("/address", response_model=str)
async def set_address(address_req: AddressRequest, request: Request):
    client_host = request.client.host
    if client_host not in allowed_ips:
        raise HTTPException(status_code=403, detail="Access denied")
    
    global address
    address = address_req.address
    return address
