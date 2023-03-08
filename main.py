import os
import json
import uvicorn
import requests
from fastapi import FastAPI, Request, Response, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

app = FastAPI()
templates = Jinja2Templates(directory="templates")
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
app.mount("/res", StaticFiles(directory="res"), name="res")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    headers = {"Authorization": os.environ.get("SPOTIFY_OAUTH_KEY")}
    spot_response = requests.get(
        "https://api.spotify.com/v1/me/player/currently-playing?market=AU",
        headers=headers,
    )
    if spot_response.status_code == 204:
        data = ['', '', '', False]
    else:
        spot_data = json.loads(spot_response.content)
        data = [spot_data["item"]["name"], spot_data["item"]["album"]["name"], spot_data["item"]["artists"][0]["name"],
                True]
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "data": data
        },
    )


@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/legal")
async def legal(request: Request):
    return templates.TemplateResponse("legal.html", {"request": request})


@app.get("/interwebs")
async def web(request: Request):
    return templates.TemplateResponse("interwebs.html", {"request": request})


@app.get("/services.html")
async def web_services(request: Request):
    return templates.TemplateResponse("services.html", {"request": request})


@app.get("/space")
async def space(request: Request):
    return templates.TemplateResponse("space.html", {"request": request})


@app.exception_handler(404)
async def except_404(request, Request):
    return templates.TemplateResponse("404.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
