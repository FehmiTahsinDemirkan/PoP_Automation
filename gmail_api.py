import os
import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import config

def authenticate(account):
    """
    Belirtilen hesap için kimlik doğrulama işlemini gerçekleştirir.
    """
    creds = None
    token_file = account['token_file']
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, config.SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(config.CREDENTIALS_FILE, config.SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
            print(f"Yeni kimlik doğrulama dosyası oluşturuldu: {token_file}")
    return build('gmail', 'v1', credentials=creds)

def list_emails(service, max_results=3):
    """
    Gelen kutusundaki e-postaları listeler.
    """
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    return results.get('messages', [])

def download_email(service, msg_id, output_folder):
    """
    Belirtilen mesaj ID'sine sahip e-postayı indirir.
    """
    try:
        message = service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
        raw_data = message['raw']
        email_data = base64.urlsafe_b64decode(raw_data)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        file_name = f"{msg_id}.eml"
        file_path = os.path.join(output_folder, file_name)
        with open(file_path, 'wb') as f:
            f.write(email_data)
            print(f"E-posta indirildi: {file_path}")
        return file_path
    except Exception as e:
        print(f"E-posta indirilirken bir hata oluştu: {e}")
        return None

def process_all_accounts():
    """
    Tüm hesaplar için işlemleri gerçekleştirir.
    """
    accounts = [config.ACCOUNT_1, config.ACCOUNT_2]
    for account in accounts:
        print(f"{account['name']} için işlemler başlatılıyor...")
        service = authenticate(account)
        emails = list_emails(service)

        if not emails:
            print(f"{account['name']} için hiç e-posta bulunamadı.")
            continue

        for email in emails:
            msg_id = email['id']
            download_email(service, msg_id, account['output_folder'])

if __name__ == '__main__':
    process_all_accounts()
