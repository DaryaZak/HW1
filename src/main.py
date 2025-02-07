

from fastapi import FastAPI
#from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))


from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.auth import router as router_auth


app = FastAPI()

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)


#@app.get(path:'/docs', include_in_schema=False)
#async def


if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)
