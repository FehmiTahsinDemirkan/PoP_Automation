import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import config  # config.py dosyasını import ediyoruz

# Tarayıcıyı başlat
driver = webdriver.Chrome()
url = "https://app.themindsite.com/login"

# Email ve şifreyi config.py'den alıyoruz
email = config.EMAIL
password = config.PASSWORD

# URL'yi aç
driver.get(url)
time.sleep(5)
# Email alanını bekle ve doldur
email_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div[1]/div/form/div/div[1]/div[1]/div/div/div/div/input"))
)
email_input.send_keys(email)

# Şifre alanını bekle ve doldur
password_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div[1]/div/form/div/div[1]/div[2]/div/div/div/div/input"))
)
password_input.send_keys(password)
time.sleep(2)
# Giriş butonunu bekle ve tıkla
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[1]/div/form/div/div[3]/button"))
)
login_button.click()
time.sleep(2)
# Sayfanın yüklenmesini bekle
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "body"))  # Sayfanın tamamen yüklendiğini doğrulamak için
)

# Ekran görüntüsünü al ve kaydet
screenshot_path = "login_page_screenshot.png"
driver.save_screenshot(screenshot_path)
print(f"Ekran görüntüsü alındı ve '{screenshot_path}' olarak kaydedildi.")

# Tarayıcıyı kapat
driver.close()