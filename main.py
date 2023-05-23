import os
import json
import spot
import spotipy
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
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
        data = ['', '', '', False]
    else:
        spot_data = json.loads(json.dumps(spot_response))

        data = [spot_data["item"]["name"], spot_data["item"]["album"]["name"], spot_data["item"]["artists"][0]["name"],
                True, spot_data["item"]["external_urls"]["spotify"],
                spot_data["item"]["album"]["external_urls"]["spotify"],
                spot_data["item"]["artists"][0]["external_urls"]["spotify"]]
    files = os.listdir("data/posts")
    files.sort(key=lambda x: os.path.getmtime(os.path.join("data/posts", x)), reverse=True)
    match action:
        case 'Latest':
            return templates.TemplateResponse("new_index.html", {"request": request, "post": files[0].replace(".md", ""), "data": data}, )
        case 'v1':
            return templates.TemplateResponse("old_index.html", {"request": request, "post": files[0].replace(".md", ""), "data": data}, )
        case 'v2':
            return templates.TemplateResponse("old_old_index.html", {"request": request, "post": files[0].replace(".md", ""), "data": data}, )
        case 'v3':
            return templates.TemplateResponse("index.html", {"request": request, "post": files[0].replace(".md", ""), "data": data}, )

@app.get("/posts")
async def posts(request: Request):
    post_list = []
    for filename in os.listdir("data/posts"):
        post_list.append(filename)

    print(post_list)
    return templates.TemplateResponse("posts.html", {"request": request, "posts": post_list})


# @app.get("/about")
# async def about(request: Request):
#    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/legal")
@limiter.limit("60/minute")
async def legal(request: Request):
    return templates.TemplateResponse("legal.html", {"request": request})


@app.get("/space")
@limiter.limit("60/minute")
async def space(request: Request):
    return templates.TemplateResponse("space.html", {"request": request})


@app.exception_handler(404)
async def except_404(request: Request):
    return templates.TemplateResponse("404.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
