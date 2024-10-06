from fastapi.responses import JSONResponse

async def get_background():
    return JSONResponse(content={"url": "/background/a.jpg"})