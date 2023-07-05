# @app.get("/about")
# async def about(request: Request):
#    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/legal")
@limiter.limit("60/minute")
async def legal(request: Request):
    return templates.TemplateResponse("legal.html", {"request": request})


@app.get("/posts")
async def posts(request: Request):
    post_list = []
    for filename in os.listdir("data/posts"):
        post_list.append(filename)

    print(post_list)
    return templates.TemplateResponse("posts.html", {"request": request, "posts": post_list})


@app.get("/", response_class=HTMLResponse)
@limiter.limit("40/minute")
async def root(request: Request, action: str = 'Latest'):
    spot_response = await spot.get_spotify_track()
    if spot_response is None:
        data = ['', '', '', False]
    else:
        spot_data = json.loads(json.dumps(spot_response))

    #files = os.listdir("data/posts")
    #files.sort(key=lambda x: os.path.getmtime(os.path.join("data/posts", x)), reverse=True)
    files = ['','','']
    match action:
        case 'Latest':
            return templates.TemplateResponse("new_index.html",
                                              {"request": request, "post": files[0].replace(".md", ""), "data": data}, )
        case 'v1':
            return templates.TemplateResponse("old_index.html",
                                              {"request": request, "post": files[0].replace(".md", ""), "data": data}, )
        case 'v2':
            return templates.TemplateResponse("old_old_index.html",
                                              {"request": request, "post": files[0].replace(".md", ""), "data": data}, )
        case 'v3':
            return templates.TemplateResponse("index.html",
                                              {"request": request, "post": files[0].replace(".md", ""), "data": data}, )
