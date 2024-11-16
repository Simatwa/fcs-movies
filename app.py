#!/usr/bin/python3
from backend import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
