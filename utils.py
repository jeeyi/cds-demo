from flask import jsonify

from config import ROOT_FOLDER_ID
import cds as cds


def create_folder(data):
    is_demo = True if data["is_demo"] == "true" else False
    folder_name = data["folder_name"]
    parent_folder_id = data["parent_folder_id"]

    if is_demo or parent_folder_id.isdigit():
        return jsonify({"name": folder_name})

    cds_data = {"label": folder_name, "parent": parent_folder_id}
    cds_folder = cds.create_folder(cds_data)
    return jsonify({"id": cds_folder["id"], "name": cds_folder["label"]})


def get_folder(folder_id):
    if folder_id and folder_id.isdigit():
        return get_demo(folder_id)

    cds_folder = cds.get_folder(folder_id)

    folder_name = cds_folder["label"]
    ancestors = [ancestor["label"] for ancestor in cds_folder["ancestors"]]
    folders = [
        {"id": folder["id"], "name": folder["label"]}
        for folder in cds_folder["children"]
    ]
    file_names = [file["label"] for file in cds_folder["documents"]]
    files = get_files(file_names)

    folder_data = {
        "current_folder_id": folder_id,
        "ancestors": ancestors,
        "ancestors_len": len(ancestors),
        "files": files,
        "files_len": len(files),
        "folders": folders,
        "folders_len": len(folders),
        "folder_name": folder_name,
    }
    return folder_data


def get_file_icon(file_name):
    ext = file_name.split(".")[-1]
    ext_to_icon = {
        "docx": "fa fa-file-word-o",
        "jpeg": "fa fa-file-image-o",
        "mov": "fa fa-file-movie-o",
        "pdf": "fa fa-file-pdf-o",
        "pptx": "fa fa-file-powerpoint-o",
        "txt": "fa fa-file-text-o",
        "xlsx": "fa fa-file-excel-o",
        "zip": "fa fa-file-zip-o",
    }
    return ext_to_icon.get(ext, "fa fa-file-o")


def get_files(file_names):
    return [
        {"name": file_name, "icon": get_file_icon(file_name)}
        for file_name in file_names
    ]


def get_demo(folder_id=None):
    folder_name = f"Folder{folder_id}" if folder_id else "Demo Folder"
    ancestors = [
        "Meetings",
        "Weekly",
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
    files = get_files(
        [
            "File1.mov",
            "File2.docx",
            "File3.pptx",
            "File4.pdf",
            "File5.jpeg",
            "File6.xlsx",
            "File7.zip",
            "File8.txt",
        ]
    )
    demo_data = {
        "current_folder_id": 0,
        "ancestors": ancestors,
        "ancestors_len": len(ancestors),
        "files": files,
        "files_len": len(files),
        "folders": folders,
        "folders_len": len(folders),
        "folder_name": folder_name,
    }
    return demo_data
