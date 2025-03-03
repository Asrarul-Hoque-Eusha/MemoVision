from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from api.upload import router as upload_router
from api.query import router as query_router
from api.gallery import router as gallery_router
from api.viewer import router as viewer_router
from models import PathVariables, APIVariables
from services.delete_image import delete_query_image
app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory=PathVariables.directory),
    name="static"
)
app.include_router(upload_router, tags=["upload"])
app.include_router(query_router, tags=["query"])
app.include_router(gallery_router,  tags=["gallery"])
app.include_router(viewer_router, tags=["viewer"])

delete_query_image()

@app.get("/")
async def root():
    return {APIVariables.message: APIVariables.fastapi_running_message}
