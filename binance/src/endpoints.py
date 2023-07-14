from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from starlette.endpoints import HTTPEndpoint


templates = Jinja2Templates(directory="templates")

class Homepage(HTTPEndpoint):

    async def get(self, request):
        return templates.TemplateResponse("index.html", {"request": request})