import os
import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import config
import logging

# === Loglama Ayarları ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("process_log.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

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
            logging.info(f"Yeni kimlik doğrulama dosyası oluşturuldu: {token_file}")
    return build('gmail', 'v1', credentials=creds)

def list_sent_emails(service, max_results=3):
    """
    Gönderilen kutusundaki e-postaları listeler.
    """
    try:
        results = service.users().messages().list(userId='me', labelIds=['SENT'], maxResults=max_results).execute()
        return results.get('messages', [])
    except Exception as e:
        logging.error(f"Gönderilen e-postalar listelenirken bir hata oluştu: {e}")
        return []

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
            logging.info(f"E-posta indirildi: {file_path}")
        return file_path
    except Exception as e:
        logging.error(f"E-posta indirilirken bir hata oluştu: {e}")
        return None

def process_all_accounts(output_folder="assets"):
    """
    Tüm hesaplar için işlemleri gerçekleştirir.
    """
    accounts = [config.ACCOUNT_1, config.ACCOUNT_2]
    for account in accounts:
        logging.info(f"{account['name']} için işlemler başlatılıyor...")
        service = authenticate(account)
        emails = list_sent_emails(service)

        if not emails:
            logging.info(f"{account['name']} için gönderilen kutusunda hiç e-posta bulunamadı.")
            continue

        for email in emails:
            msg_id = email['id']
            download_email(service, msg_id, output_folder)

if __name__ == '__main__':
    process_all_accounts()
