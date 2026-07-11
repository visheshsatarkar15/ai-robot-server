import os
from fastapi import Header, HTTPException

DEVICE_TOKEN = os.getenv("DEVICE_TOKEN")


def verify_device(x_device_token: str = Header(None)):
    if DEVICE_TOKEN is None:
        raise HTTPException(status_code=500, detail="DEVICE_TOKEN not configured")

    if x_device_token != DEVICE_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized device")
