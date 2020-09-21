import requests
from config import CDS_URL, CDS_KEY, CARTA_USER_ID


CDS_HEADERS = {"X-API-KEY": CDS_KEY, "X-USER-ID": str(CARTA_USER_ID)}


def create_folder(data):
    url = f"{CDS_URL}/folders/"
    res = requests.post(url, data=data, headers=CDS_HEADERS)
    if res.status_code != requests.codes.created:
        raise Exception("Failed to create folder in CDS", status_code=500)
    return res.json() if res.status_code == requests.codes.created else {}


def get_folder(folder_id):
    url = f"{CDS_URL}/folders/{folder_id}"
    res = requests.get(url, headers=CDS_HEADERS)
    return res.json() if res.status_code == requests.codes.ok else {}
