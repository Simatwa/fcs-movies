"""Builds a complete API made up of several versions"""

import re
from backend.v1 import v1_router
from backend.v2 import v2_router
from backend.database import create_tables
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

parent_path = Path(__file__).parent

project_path = parent_path.parent

frontend_path = project_path / "frontend"

readme_contents = (parent_path / "README.md").read_text()

templates = Jinja2Templates(directory=frontend_path)


def get_from_readme(target) -> str:
    """Extracts header values from README.md"""
    return re.findall(target + r":\s(.+)", readme_contents)[0]


app = FastAPI(
    title=get_from_readme("title"),
    version=get_from_readme("version"),
    summary=get_from_readme("summary"),
    description="\n".join(readme_contents.splitlines()[5:]),
    terms_of_service="",
    contact={
        "name": "Smartwa",
        "url": "https://simatwa.vercel.app",
        "email": "simatwacaleb@proton.me",
    },
    license_info={
        "name": "GPLv3",
        "url": "https://raw.githubusercontent.com/Simatwa/fcs-movies/refs/heads/main/LICENSE",
    },
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)


@app.get("/", name="index", response_class=HTMLResponse, include_in_schema=False)
def index(request: Request):
    """Serve index.html"""
    # return templates.TemplateResponse(request, name="index.html")
    return RedirectResponse("/api/docs")


app.mount("/src", StaticFiles(directory=frontend_path / "src"), name="assets")
"""Route to static contents"""

app.include_router(v1_router, prefix="/api/v1", tags=["V1"])
"""Route to v1 of the API"""

app.include_router(v2_router, prefix="/api/v2", tags=["V2"])
"""Route to v2 of the API"""

app.add_event_handler("startup", create_tables)
