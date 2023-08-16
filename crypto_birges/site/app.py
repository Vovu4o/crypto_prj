import aiofiles
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles




app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/')
async def homepage():
    return {"message": "home"}

@app.get('/kucoin', response_class=HTMLResponse)
async def kucoin_view(request: Request):
    all_triangles = []
    async with aiofiles.open("../ws_server/triangles.txt") as afile:
        async for triangle in afile:
            all_triangles += [triangle]
    return templates.TemplateResponse("kucoin.html", {'request': request, "all_triangles": all_triangles})
