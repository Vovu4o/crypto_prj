from starlette.routing import Route

from .endpoints import Homepage

routes = [
    Route("/homepage", Homepage),
]