import os
import json
import uvicorn
import requests
from fastapi import FastAPI, Request, Response
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
    #if spot_response.status_code == 204:
    print(spot_response.status_code)
    spot_data = json.loads(spot_response.content)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "javascript_status": "Enabled",
            "song_name": spot_data["item"]["name"],
            "song_album": spot_data["item"]["album"]["name"],
            "song_artist": spot_data["item"]["artists"][0]["name"],
        },
    )


@app.get("/js")
async def js_trigger(response: Response, trigger: str = "Enable"):
    if trigger.lower() == 'enable':
        response.headers["X-Javascript-Disabled"] = "True"
    elif trigger.lower() == 'disable':
        response.headers["X-Javascript-Disabled"] = "False"
    else:
        response.headers["X-Javascript-Disabled"] = "Auto"
    return RedirectResponse('/')


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


@app.exception_handler(404)
async def except_404(request, Request):
    return templates.TemplateResponse("404.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
