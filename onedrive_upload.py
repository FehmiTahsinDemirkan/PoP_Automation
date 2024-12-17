# onedrive_upload.py

import os
import requests
from ms_graph import generate_access_token, GRAPH_API_ENDPOINT


def upload_assets_folder_to_onedrive(app_id, folder_name='fehmimindsite', assets_folder_name='assets'):
    """
    Upload all files in the specified assets folder to a OneDrive folder.

    :param app_id: The application ID for Microsoft Graph API
    :param folder_name: The target folder name in OneDrive (default is 'fehmimindsite')
    :param assets_folder_name: The local folder containing files to upload (default is 'assets')
    """
    try:
        # Generate Access Token
        print("Access token alınıyor...")
        access_token_response = generate_access_token(app_id, ['https://graph.microsoft.com/.default'])
        if 'access_token' not in access_token_response:
            raise Exception("Access token alınamadı. Yanıt:", access_token_response)
        access_token = access_token_response['access_token']
        print("Access token başarıyla alındı.\n")

        # Headers
        headers = {
            'Authorization': 'Bearer ' + access_token,  # Ensure a space after 'Bearer'
            'Content-Type': 'application/octet-stream'
        }

        # File Selection
        project_root = os.path.dirname(os.path.abspath(__file__))
        assets_folder = os.path.join(project_root, assets_folder_name)

        # Dosya kontrolü ve seçimi
        if not os.path.exists(assets_folder):
            raise FileNotFoundError(f"'{assets_folder_name}' klasörü bulunamadı: {assets_folder}")

        # Step 1: Get the folder ID for 'folder_name'
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

        # Step 2: Upload all files in the 'assets' folder
        for file_name in os.listdir(assets_folder):
            file_path = os.path.join(assets_folder, file_name)

            if os.path.isfile(file_path):
                print(f"Dosya yükleniyor: {file_path}")

                # Upload file to OneDrive in the 'folder_name' folder
                upload_url = GRAPH_API_ENDPOINT + f'/me/drive/items/{folder_id}:/{file_name}:/content'

                with open(file_path, 'rb') as upload:
                    media_content = upload.read()
                    response = requests.put(
                        upload_url,
                        headers=headers,
                        data=media_content
                    )

                # Yanıtı kontrol et
                if response.status_code in [200, 201]:
                    print(f"Dosya başarıyla yüklendi: {file_name}")
                else:
                    print(f"Dosya yüklenirken hata oluştu: {file_name}")
                    print(f"Status Code: {response.status_code}")
                    print(f"Response: {response.text}")

    except Exception as e:
        print("Bir hata oluştu:", str(e))
