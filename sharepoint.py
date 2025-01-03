import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

def take_screenshot(driver, file_name, assets_folder):

    file_path = os.path.join(assets_folder, file_name)
    driver.save_screenshot(file_path)
    print(f"Ekran görüntüsü kaydedildi: {file_path}")

def run_sharepoint():

    driver = webdriver.Chrome()

    url = config.url

    driver.get(url)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="appRoot"]/div/div[2]/div/div/div[2]/div[2]/main/div'))
        )
        print("Sayfa başarıyla yüklendi.")
    except Exception as e:
        print("Sayfa yüklenirken bir hata oluştu:", str(e))
        driver.quit()
        return

    assets_folder = "assets"


    scroll_element = driver.find_element(By.XPATH, '//*[@id="appRoot"]/div/div[2]/div/div/div[2]/div[2]/main/div')

    time.sleep(2)
    take_screenshot(driver, "screenshot_1.png", assets_folder)

    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight / 3;", scroll_element)  # Scroll öğesinin 1/3'ü kadar kaydır
    time.sleep(2)
    take_screenshot(driver, "screenshot_2.png", assets_folder)

    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scroll_element)  # Scroll öğesinin en altına git
    time.sleep(2)  
    take_screenshot(driver, "screenshot_3.png", assets_folder)

    driver.quit()

def main():

    print("SharePoint işlemleri başlatılıyor...")
    run_sharepoint()

if __name__ == '__main__':
    main()
