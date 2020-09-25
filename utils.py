from io import BytesIO
import zipfile

from flask import jsonify, Response
from werkzeug.utils import secure_filename

import cds as cds


def create_folder(data):
    is_demo = True if data["is_demo"] == "true" else False
    folder_name = data["folder_name"]
    parent_folder_id = data["parent_folder_id"]

    if is_demo or parent_folder_id.isdigit():
        return jsonify({"name": folder_name})

    cds_folder = cds.create_folder(folder_name, parent_folder_id)
    return jsonify({"id": cds_folder["id"], "name": cds_folder["label"]})


def get_folder(folder_id):
    if folder_id and folder_id.isdigit():
        return get_demo(folder_id)

    cds_folder = cds.get_folder(folder_id)

    folder_name = cds_folder["label"]
    ancestors = [
        {"id": ancestor["uuid"], "name": ancestor["label"]}
        for ancestor in cds_folder["ancestors"]
    ]
    folders = [
        {"id": folder["id"], "name": folder["label"]}
        for folder in cds_folder["children"]
    ]
    files = [
        get_file(file["id"], file["label"]) for file in cds_folder["documents"]
    ]

    folder_data = {
        "ancestors": ancestors,
        "files": files,
        "folder_id": folder_id,
        "folder_name": folder_name,
        "folders": folders,
    }
    return folder_data


def upload_file(file, data):
    is_demo = True if data["is_demo"] == "true" else False
    parent_folder_id = data["parent_folder_id"]
    file_name = secure_filename(file.filename)

    if is_demo or parent_folder_id.isdigit():
        return jsonify({"name": file_name, "icon": get_file_icon(file_name)})

    cds_file = cds.upload_file(file, file_name, parent_folder_id)
    file_name = cds_file["label"]
    return jsonify({"name": file_name, "icon": get_file_icon(file_name)})


def download(data):
    is_demo = True if data["is_demo"] == "true" else False
    parent_folder_id = data["parent_folder_id"]
    files = data["files"].split(",")

    if is_demo or parent_folder_id.isdigit():
        zipfile = zip_demo_files([int(file_id) for file_id in files])
    else:
        zipfile = cds.download(files, parent_folder_id)
    return Response(zipfile, mimetype="application/octet-stream")


def get_file_icon(file_name):
    ext = file_name.split(".")[-1]
    ext_to_icon = {
        "docx": "fa fa-file-word-o",
        "jpg": "fa fa-file-image-o",
        "mov": "fa fa-file-movie-o",
        "pdf": "fa fa-file-pdf-o",
        "pptx": "fa fa-file-powerpoint-o",
        "txt": "fa fa-file-text-o",
        "xlsx": "fa fa-file-excel-o",
        "zip": "fa fa-file-zip-o",
    }
    return ext_to_icon.get(ext, "fa fa-file-o")


def get_file(id, file_name):
    return {"id": id, "name": file_name, "icon": get_file_icon(file_name)}


def get_demo(folder_id="0"):
    folder_name = "Demo Folder" if folder_id == "0" else f"Folder{folder_id}"
    ancestors = [
        {"id": "1", "name": "Weekly"},
        {"id": "1", "name": "Meetings"},
    ]
    folders = [
        {"id": "1", "name": "Folder1"},
        {"id": "2", "name": "Folder2"},
        {"id": "3", "name": "Folder3"},
        {"id": "4", "name": "Folder4"},
        {"id": "5", "name": "Folder5"},
        {"id": "6", "name": "Folder6"},
        {"id": "7", "name": "Folder7"},
    ]
    files = [get_file(i, get_demo_file(i)) for i in range(1, 9)]
    demo_data = {
        "ancestors": ancestors,
        "files": files,
        "folder_id": folder_id,
        "folder_name": folder_name,
        "folders": folders,
    }
    return demo_data


def get_demo_file(id):
    demo_files = {
        "1": "File1.txt",
        "2": "File2.docx",
        "3": "File3.pptx",
        "4": "File4.pdf",
        "5": "File5.jpg",
        "6": "File6.xlsx",
        "7": "File7.zip",
        "8": "File8.mov",
    }
    return demo_files.get(str(id), f"File{id}.txt")


def zip_demo_files(demo_file_ids):
    in_memory = BytesIO()
    with zipfile.ZipFile(in_memory, "w", compression=zipfile.ZIP_STORED) as zf:
        for id in demo_file_ids:
            file_name = get_demo_file(id)
            zf.write("demo/" + file_name)
    in_memory.seek(0)
    return in_memory
