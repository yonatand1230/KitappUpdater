from dotenv import load_dotenv
from os import getenv

from Upload import Upload
from Shachaf import GetChanges


load_dotenv()
token = getenv('token')


print("## SHACHAF ##")
shacahf = GetChanges.main()

Upload.upload_json(
    shacahf,
    file_path = "shachaf.json",
    repository = "KitappContent",
    username = "yonatand1230",
    msg = "Update Contents",
    token = token
    )