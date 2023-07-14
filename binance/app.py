import uvicorn
from starlette.applications import Starlette

app = Starlette(debug=True)

if __name__ == "__main__":
    uvicorn.run("app:app", port=8888)
