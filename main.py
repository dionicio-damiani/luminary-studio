import os

import uvicorn

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
RELOAD = os.getenv("RELOAD", "true").lower() in ("1", "true", "yes")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=RELOAD)
