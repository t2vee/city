import os
import json
import spot
import spotipy
import uvicorn
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
templates = Jinja2Templates(directory="templates")
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
app.mount("/res", StaticFiles(directory="res"), name="res")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
scope = "user-read-currently-playing"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
results = sp.current_user_playing_track()


@app.get("/", response_class=HTMLResponse)
@limiter.limit("40/minute")
async def root(request: Request, action: str = 'Latest'):
    spot_response = await spot.get_spotify_track()
    if spot_response is None:
        spotify_payload = ['', '', '', False]
    else:
        spot_data = json.loads(json.dumps(spot_response))
        spotify_payload = [spot_data["item"]["name"][:24-3] + "..." if len(spot_data["item"]["name"]) > 24 else spot_data["item"]["name"], spot_data["item"]["album"]["name"][:24-3] + "..." if len(spot_data["item"]["album"]["name"]) > 24 else spot_data["item"]["album"]["name"],
                           spot_data["item"]["artists"][0]["name"][:24-3] + "..." if len(spot_data["item"]["artists"][0]["name"]) > 24 else spot_data["item"]["artists"][0]["name"],
                           True, spot_data["item"]["external_urls"]["spotify"],
                           spot_data["item"]["album"]["external_urls"]["spotify"],
                           spot_data["item"]["artists"][0]["external_urls"]["spotify"],
                           spot_data["item"]["album"]["images"][2]["url"]]

    return templates.TemplateResponse("index.html", {"request": request, "data": spotify_payload}, )


#@app.get("/stats")
#@limiter.limit("60/minute")
#async def space(request: Request):
#    return templates.TemplateResponse("stats.html", {"request": request})


@app.get("/content_proxy")
@limiter.limit("60/minute")
def proxy(request: Request, uri: str):
    response = requests.get(uri, stream=True)
    return StreamingResponse(response.iter_content(chunk_size=1024), media_type=response.headers["content-type"])


@app.exception_handler(404)
async def custom_404_handler(request, __):
    return templates.TemplateResponse("404.html", {"request": request})


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("res/imgs/favicon.ico")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
