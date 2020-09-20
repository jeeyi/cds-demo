import requests
from config import CDS_URL, CDS_KEY, CARTA_USER_ID


CDS_HEADERS = {"X-API-KEY": CDS_KEY, "X-USER-ID": str(CARTA_USER_ID)}


def get_folder(folder_id):
    url = f"{CDS_URL}/folders/{folder_id}"
    res = requests.get(url, headers=CDS_HEADERS)
    return res.json() if res.status_code == requests.codes.ok else {}
