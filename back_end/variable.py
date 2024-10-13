from fastapi.templating import Jinja2Templates

UPLOADPATH = "data"
BUFFERPATH = 'buffer'
CONFIGJSONPATH = "config/config.json"
DATAJSONPATH = "config/datainfo.json"
SHAREPATH = "share"
DBPATH = "./config/config.db"
templates = Jinja2Templates(directory="front_end")


initial_config = {
    "filesize": 1024,
    "chunksize": 100,
    "buffertime": 1800,
    "password": "admin"
}
