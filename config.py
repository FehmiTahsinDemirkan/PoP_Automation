import os

# Ortak ayarlar
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
OUTPUT_FOLDER = 'assets'  # E-postaların kaydedileceği klasör
CREDENTIALS_FILE = 'credentials.json'

# Hesap 1 için ayarlar
ACCOUNT_1 = {
    'name': 'Hesap 1',
    'token_file': 'token_account1.json',
    'output_folder': os.path.join(OUTPUT_FOLDER, 'account1')
}

# Hesap 2 için ayarlar
ACCOUNT_2 = {
    'name': 'Hesap 2',
    'token_file': 'token_account2.json',
    'output_folder': os.path.join(OUTPUT_FOLDER, 'account2')
}


#mindsite sifre mail
EMAIL = "fehmiMindsite@gmail.com"
PASSWORD = "password123"
MIND_SITE_URL = "https://app.themindsite.com/login"  # Mindsite login URL



url = "https://1drv.ms/f/s!AgdRQ2KZOKr8b7yzPS-Y6uZdR6g?e=8b2bgF"

