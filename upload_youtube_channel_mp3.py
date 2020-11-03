#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    parent_id = drive.ListFile(
        {
            'q': "title = '{}'".format("youtube_channel")
        }
    ).GetList()[0]['id']
    google_drive_file_list = drive.ListFile(
        {
            'q': '"{}" in parents and trashed = false'.format(parent_id)
        }
    ).GetList()
    google_drive_file_name_list = [file.get("originalFilename") for file in google_drive_file_list]
    local_file_list = glob.glob("*.mp3")
    for file in local_file_list:
        file_name = os.path.basename(file)
        if file_name in google_drive_file_name_list:
            print(file_name + " already exists")
        else:
            print(file_name + " will be uploaded")
            f = drive.CreateFile(
                {
                    'parents': [{
                        'id': parent_id
                        }],
                    'title': file_name
                }
            )
            f.SetContentFile(file)
            f.Upload()

main()
