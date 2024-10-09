from fastapi.responses import JSONResponse

# async def get_background():
#     return JSONResponse(content={"url": "/background/background.jpg"})

# async def get_icon():
#     return JSONResponse(content={"url": "/icon/book.png"})


# @app.get("/favicon.icon")
# async def favicon_json():
#     with open("icon/book.png", "rb") as f:
#         favicon = f.read()
#     return Response(content=favicon, media_type="image/x-icon")