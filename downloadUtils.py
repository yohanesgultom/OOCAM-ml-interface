from zipfile import ZipFile
from flask import send_file
import os

def zipAndDownload(folder):
    with ZipFile(f'{folder}.zip', 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(folder):
            for filename in filenames:
                zipObj.write(os.path.join(folderName, filename))

    return send_file(f'{folder}.zip', as_attachment = True)
