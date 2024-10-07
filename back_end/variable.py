from fastapi.templating import Jinja2Templates

UPLOADPATH = "data"
BUFFERPATH = 'buffer'
CONFIGJSONPATH = "config/config.json"
DATAJSONPATH = "config/datainfo.json"
SHAREPATH = "share"
templates = Jinja2Templates(directory="front_end")
