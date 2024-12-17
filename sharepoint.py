import time
import os  # Klasör oluşturmak için os modülü
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config  # config.py modülünü import ediyoruz

def take_screenshot(driver, file_name, assets_folder):
    """
    Ekran görüntüsünü kaydeder.
    """
    file_path = os.path.join(assets_folder, file_name)  # Dosya yolu oluştur
    driver.save_screenshot(file_path)
    print(f"Ekran görüntüsü kaydedildi: {file_path}")

def run_sharepoint():
    """
    SharePoint işlemlerini gerçekleştirir.
    """
    # Tarayıcıyı başlat
    driver = webdriver.Chrome()

    # URL bilgisi config.py'den çekiliyor
    url = config.url

    # Sayfayı aç
    driver.get(url)

    # Sayfanın yüklenmesini bekle
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="appRoot"]/div/div[2]/div/div/div[2]/div[2]/main/div'))
        )
        print("Sayfa başarıyla yüklendi.")
    except Exception as e:
        print("Sayfa yüklenirken bir hata oluştu:", str(e))
        driver.quit()
        return

    # 'assets' klasörünü oluştur
    assets_folder = "assets"
    if not os.path.exists(assets_folder):
        os.makedirs(assets_folder)
        print(f"'{assets_folder}' klasörü oluşturuldu.")

    # Scroll işlemi için hedef öğeyi bul
    scroll_element = driver.find_element(By.XPATH, '//*[@id="appRoot"]/div/div[2]/div/div/div[2]/div[2]/main/div')

    # 1. Ekran görüntüsü: İlk açılan ekran
    time.sleep(2)  # Sayfa yüklenmesini tamamlamak için kısa bir ek bekleme
    take_screenshot(driver, "screenshot_1.png", assets_folder)

    # 2. Ekran görüntüsü: Sayfayı biraz aşağı kaydır
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight / 3;", scroll_element)  # Scroll öğesinin 1/3'ü kadar kaydır
    time.sleep(2)  # Kaydırma animasyonu için kısa bir bekleme
    take_screenshot(driver, "screenshot_2.png", assets_folder)

    # 3. Ekran görüntüsü: Sayfanın en altına git
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scroll_element)  # Scroll öğesinin en altına git
    time.sleep(2)  # Kaydırma animasyonu için kısa bir bekleme
    take_screenshot(driver, "screenshot_3.png", assets_folder)

    # Tarayıcıyı kapat
    driver.quit()

def main():
    """
    SharePoint işlemlerini başlatır.
    """
    print("SharePoint işlemleri başlatılıyor...")
    run_sharepoint()

if __name__ == '__main__':
    main()
