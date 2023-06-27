from dotenv import load_dotenv
from os import getenv
import sys,json,clipboard

from Shachaf import GetChanges
from Tehilim import GetTehilim
from Upload import Upload
from Limud import Limud

load_dotenv()
token = getenv('token')


final = {
    "this is a test":"abc"
}


Upload.upload_json(
    final,
    file_path = "test3.json",
    repository = "KitappContent",
    username = "yonatand1230",
    msg = "Update Contents",
    token = token,
    folder = "content"
    )