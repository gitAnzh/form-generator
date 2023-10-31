from typing import Union

import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from config import settings
from routers.users.app import appd as order_app
#
app = FastAPI(title="Portal Api Gateway",
              version="0.0.1",
              docs_url="/docs" if settings.DEBUG_MODE else None,
              )

# --------------------------------------------- Mount Services Here ------------------------------------------------- #


app.mount(path="/users/api/v1", app=order_app)
app.mount("/gallery_files/", StaticFiles(directory="static_files"), name="gallery_files")


# ------------------------------------------------ Logging features -------------------------------------------------- #

#
#
@app.get("/")
def main():
    if settings.DEBUG_MODE:
        a = [{"path": f"http://127.0.0.1:8099{route.path}/docs/"} for route in app.routes][4:-1]
        return a
    return {
        "detail": "Not Found"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.UVICORN_HOST, port=settings.UVICORN_PORT, reload=True, workers=10)
