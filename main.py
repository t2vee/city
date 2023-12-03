import os
import re
import json
import spot
import base64
import spotipy
import uvicorn
import requests
import sentry_sdk
from rjsmin import jsmin
from functools import lru_cache
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from jinja2htmlcompress import HTMLCompress

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
templates = Jinja2Templates(directory="templates")
templates.env.add_extension(HTMLCompress)
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
app.mount("/res", StaticFiles(directory="res"), name="res")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
scope = "user-read-currently-playing"
sentry_sdk.init(
    dsn=f"{os.environ.get('SENTRY_DSN')}",
    enable_tracing=True,
)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
results = sp.current_user_playing_track()
from datetime import datetime, timedelta

cache = {}
cache_timeout = timedelta(seconds=60)
stats_cache_timeout = timedelta(days=30)
stats_cache = {}


@app.get("/", response_class=HTMLResponse)
@limiter.limit("1/second")
async def root(request: Request):
    now = datetime.now()
    if 'spotify_payload' in cache and now - cache['timestamp'] < cache_timeout:
        spotify_payload = cache['spotify_payload']
        caching = False
    else:
        spot_response = await spot.get_spotify_track()
        print("reaching spotify api")
        caching = True
        if spot_response is None:
            spotify_payload = ['', '', 'none', None]
        else:
            spot_data = json.loads(json.dumps(spot_response))

            spotify_payload = [spot_data["item"]["name"][:19 - 3] + "..." if len(spot_data["item"]["name"]) > 19 else
                               spot_data["item"]["name"], spot_data["item"]["album"]["name"][:23 - 3] + "..." if len(
                spot_data["item"]["album"]["name"]) > 23 else spot_data["item"]["album"]["name"],
                               spot_data["item"]["artists"][0]["name"][:25 - 3] + "..." if len(
                                   spot_data["item"]["artists"][0]["name"]) > 25 else spot_data["item"]["artists"][0][
                                   "name"],
                               True, spot_data["item"]["external_urls"]["spotify"],
                               spot_data["item"]["album"]["external_urls"]["spotify"],
                               spot_data["item"]["artists"][0]["external_urls"]["spotify"],
                               base64.urlsafe_b64encode(
                                   f'{spot_data["item"]["album"]["images"][1]["url"]}'.encode()).decode(),
                               f"{int(spot_data['progress_ms'] / (1000 * 60) % 60)}:{'0' + str(int(spot_data['progress_ms'] / 1000 % 60)) if int(spot_data['progress_ms'] / 1000 % 60) < 10 else int(spot_data['progress_ms'] / 1000 % 60)}",
                               f"{int(spot_data['item']['duration_ms'] / (1000 * 60) % 60)}:{'0' + str(int(spot_data['item']['duration_ms'] / 1000 % 60)) if int(spot_data['item']['duration_ms'] / 1000 % 60) < 10 else int(spot_data['item']['duration_ms'] / 1000 % 60)}",
                               spot_data['progress_ms'],
                               spot_data['item']['duration_ms'],
                               spot_data["is_playing"]]

            cache['spotify_payload'] = spotify_payload
            cache['timestamp'] = now

    print(spotify_payload[3])
    return templates.TemplateResponse("index.html", {"request": request, "data": spotify_payload,
                                                     "cached": "Page Being Cached Server Side..." if caching else "Page Cached"}, )


def clean_spotify_stat_payload_track(data):
    simplified_data = {}

    # Extracting relevant data from 'track'
    track = data.get("track", {})
    simplified_data["track_id"] = track.get("_id")
    simplified_data["track_name"] = track.get("name")
    simplified_data["track_album_id"] = track.get("album")
    simplified_data["track_artists"] = track.get("artists")
    simplified_data["track_popularity"] = track.get("popularity")

    # Extracting relevant data from 'artist'
    artist = data.get("artist", {})
    simplified_data["artist_id"] = artist.get("_id")
    simplified_data["artist_name"] = artist.get("name")
    simplified_data["artist_genres"] = artist.get("genres")

    # Extracting relevant data from 'album'
    album = data.get("album", {})
    simplified_data["album_id"] = album.get("_id")
    simplified_data["album_name"] = album.get("name")
    simplified_data["album_popularity"] = album.get("popularity")
    best_period = data.get("bestPeriod", {})
    simplified_data["best_period"] = best_period

    # Extracting relevant data from 'firstLast'
    first_last = data.get("firstLast", {})
    simplified_data["first_played"] = first_last.get("first", {}).get("played_at")
    simplified_data["last_played"] = first_last.get("last", {}).get("played_at")

    # Extracting relevant data from 'total'
    total = data.get("total", {})
    simplified_data["total_count"] = total.get("count")

    return json.dumps(simplified_data)


@app.get("/gateway/SpotifyStatsRelay/Track")
@limiter.limit("1/second")
def spotify_stats_relay(request: Request, track_id: str):
    print("reaching spotify stats api")
    request_url = f"https://api.urspoti.fi/track/{track_id}/stats?token={os.getenv('SPOTIFY_API_GUEST_TOKEN')}"
    response = requests.get(request_url)
    payload = response.json() if response.status_code == 200 else None
    cleaned_payload = clean_spotify_stat_payload_track(payload)
    return cleaned_payload


@app.get("/thumbnail/{base64_str}")
@limiter.limit("1/second")
def proxy(request: Request, base64_str: str):
    response = requests.get(base64.urlsafe_b64decode(base64_str.encode()).decode(), stream=True)
    return StreamingResponse(response.iter_content(chunk_size=1024), media_type=response.headers["content-type"])


@app.get("/spotify_thumbnail/{spotify_id}.jpeg")
@limiter.limit("5/second")
def proxy(request: Request, spotify_id: str):
    response = requests.get(f'https://i.scdn.co/image/{spotify_id}', stream=True)
    return StreamingResponse(response.iter_content(chunk_size=1024), media_type=response.headers["content-type"])


## EXPERIMENTAL
def minify_css(content: str) -> str:
    content = re.sub(r'\s+', ' ', content)
    content = re.sub(r'/\*.*?\*/', '', content)
    content = re.sub(r' ;', ';', content)
    content = re.sub(r'; ', ';', content)
    content = re.sub(r' {', '{', content)
    content = re.sub(r'{ ', '{', content)
    content = re.sub(r' }', '}', content)
    content = re.sub(r'} ', '}', content)
    return content.strip()


@lru_cache(maxsize=32)
def read_and_minify_css(css_file_name: str, minify: bool) -> str:
    css_path = f"./res/style/{css_file_name}"
    if minify:
        if not os.path.exists(css_path):
            return None

        with open(css_path, "r") as f:
            raw_css = f.read()

        return minify_css(raw_css)
    else:
        with open(css_path, "r") as f:
            raw_css = f.read()
        return raw_css


@app.get("/Styles/{css_file_name}", response_class=PlainTextResponse)
@limiter.limit("1/second")
async def get_css(request: Request, css_file_name: str, Minify: bool = False):
    css = read_and_minify_css(css_file_name, Minify)
    if css is None:
        return Response("CSS file not found.", media_type="text/plain", status_code=404)
    return Response(css, media_type="text/css")


@app.get("/JavaScript/{js_file_name}", response_class=PlainTextResponse)
@limiter.limit("1/second")
async def get_js(request: Request, js_file_name: str, Minify: bool = False):
    js = read_and_minify_js(js_file_name, Minify)
    if js is None:
        return Response("JavaScript file not found.", media_type="text/plain", status_code=404)
    return Response(js, media_type="application/javascript")


@lru_cache(maxsize=32)
def read_and_minify_js(js_file_name: str, minify: bool) -> str:
    js_path = f"./res/scripts/{js_file_name}"
    if not os.path.exists(js_path):
        return None

    with open(js_path, "r", encoding='utf-8') as f:
        raw_js = f.read()

    return jsmin(raw_js) if minify else raw_js


@app.get("/up")
@limiter.limit("1/second")
def up(request: Request):
    return Response("A-OK", status_code=200)


@app.exception_handler(404)
async def custom_404_handler(request, __):
    return templates.TemplateResponse("404.html", {"request": request})


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("res/imgs/optimized/favicon.webp")


@app.get('/robots.txt', include_in_schema=False)
async def favicon():
    return FileResponse("robots.txt")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
