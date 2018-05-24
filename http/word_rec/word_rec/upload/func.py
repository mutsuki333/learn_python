#!/usr/bin/python3
from __future__ import print_function
import httplib2
import os
import io

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from word_rec.settings import GOOGLE_AUTH_FILE

try:
  import argparse
  flags = tools.argparser.parse_args([])
except ImportError:
  flags = None

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = GOOGLE_AUTH_FILE+'client_id.json'
APPLICATION_NAME = 'IIM_Project'

class IIM_G:

    def get_credentials(self):
        """取得有效的憑證
        若沒有憑證，或是已儲存的憑證無效，就會自動取得新憑證

        傳回值：取得的憑證
        """
        credential_path = GOOGLE_AUTH_FILE + 'google-ocr-credential.json'
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('憑證儲存於：' + credential_path)
        return credentials


    def rec(self, filename):
        # 取得憑證、認證、建立 Google 雲端硬碟 API 服務物件
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('drive', 'v3', http=http)

        # 包含文字內容的圖片檔案（png、jpg、bmp、gif、pdf）
        imgfile = filename

        # 上傳成 Google 文件檔，讓 Google 雲端硬碟自動辨識文字
        mime = 'application/vnd.google-apps.document'
        res = service.files().create(
        body={
            'name': imgfile,
            'mimeType': mime
        },
        media_body=MediaFileUpload('image/'+imgfile, mimetype=mime, resumable=True)
        ).execute()
        txtfile = filename[:-4]+'.txt'
        result = list()

        # 下載辨識結果，儲存為文字檔案
        downloader = MediaIoBaseDownload(
            io.FileIO(txtfile, 'wb'),
            service.files().export_media(fileId=res['id'], mimeType="text/plain")
        )
        done = False
        while done is False:
            status, done = downloader.next_chunk()

        # 刪除剛剛上傳的 Google 文件檔案
        service.files().delete(fileId=res['id']).execute()
        with open(txtfile, 'r') as f:
            for line in f:
                result.append(line)
        os.remove(txtfile)
        return result

if __name__ == '__main__':
    g = IIM_G()
    g.rec("sample.jpg")
