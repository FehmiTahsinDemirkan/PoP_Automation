# onedrive_upload.py

import os
import requests
from ms_graph import generate_access_token, GRAPH_API_ENDPOINT


def upload_assets_folder_to_onedrive(app_id, folder_name='fehmimindsite', assets_folder_name='assets'):

    try:
        # Generate Access Token
        print("Access token alınıyor...")
        access_token_response = generate_access_token(app_id, ['https://graph.microsoft.com/.default'])
        if 'access_token' not in access_token_response:
            raise Exception("Access token alınamadı. Yanıt:", access_token_response)
        access_token = access_token_response['access_token']
        print("Access token başarıyla alındı.\n")

        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/octet-stream'
        }

        project_root = os.path.dirname(os.path.abspath(__file__))
        assets_folder = os.path.join(project_root, assets_folder_name)

        if not os.path.exists(assets_folder):
            raise FileNotFoundError(f"'{assets_folder_name}' klasörü bulunamadı: {assets_folder}")

        folder_path = f'/me/drive/root:/{folder_name}'
        folder_url = GRAPH_API_ENDPOINT + folder_path

        folder_response = requests.get(
            folder_url,
            headers=headers
        )

        if folder_response.status_code != 200:
            raise Exception(f"{folder_name} klasörü bulunamadı. Hata: {folder_response.text}")

        folder_id = folder_response.json()['id']
        print(f"Folder ID: {folder_id}")

        for file_name in os.listdir(assets_folder):
            file_path = os.path.join(assets_folder, file_name)

            if os.path.isfile(file_path):
                print(f"Dosya yükleniyor: {file_path}")

                upload_url = GRAPH_API_ENDPOINT + f'/me/drive/items/{folder_id}:/{file_name}:/content'

                with open(file_path, 'rb') as upload:
                    media_content = upload.read()
                    response = requests.put(
                        upload_url,
                        headers=headers,
                        data=media_content
                    )

                if response.status_code in [200, 201]:
                    print(f"Dosya başarıyla yüklendi: {file_name}")
                else:
                    print(f"Dosya yüklenirken hata oluştu: {file_name}")
                    print(f"Status Code: {response.status_code}")
                    print(f"Response: {response.text}")

    except Exception as e:
        print("Bir hata oluştu:", str(e))
