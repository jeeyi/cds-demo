from io import BytesIO
import requests

from config import CDS_URL, CDS_KEY, CARTA_USER_ID


CDS_HEADERS = {"X-API-KEY": CDS_KEY, "X-USER-ID": str(CARTA_USER_ID)}


def create_folder(folder_name, parent_folder_id):
    url = f"{CDS_URL}/folders/"
    data = {"label": folder_name, "parent": parent_folder_id}
    res = requests.post(url, data=data, headers=CDS_HEADERS)
    if res.status_code != requests.codes.created:
        raise Exception("Failed to create folder in CDS", status_code=500)
    return res.json()


def get_folder(folder_id):
    url = f"{CDS_URL}/folders/{folder_id}"
    res = requests.get(url, headers=CDS_HEADERS)
    if res.status_code != requests.codes.ok:
        raise Exception("Failed to get folder from CDS", status_code=500)
    return res.json()


def upload_file(file, file_name, parent_folder_id):
    url = f"{CDS_URL}/files/"
    files = {
        "label": (None, file_name),
        "folder": (None, parent_folder_id),
        "file": (file_name, file.read()),
    }
    res = requests.post(url, files=files, headers=CDS_HEADERS)
    if res.status_code != requests.codes.created:
        raise Exception("Failed to upload file to CDS", status_code=500)
    return res.json()


def download(files, parent_folder_id):
    url = f"{CDS_URL}/download/"
    data = {"resources": files, "current_folder": parent_folder_id}

    res = requests.post(url, data=data, headers=CDS_HEADERS)
    if res.status_code != requests.codes.ok:
        raise Exception("Failed to download files from CDS", status_code=500)

    in_memory = BytesIO()
    in_memory.write(res.content)
    in_memory.seek(0)
    return in_memory
