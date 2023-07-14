import uvicorn
from starlette.applications import Starlette

from src.routes import routes

app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    uvicorn.run("app:app", port=8888)
