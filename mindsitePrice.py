import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from multiprocessing import Process
import config  # config.py dosyasını import ediyoruz

def take_screenshot(instance_id):
    screenshot_folder = os.path.join(os.getcwd(), 'assets')
    os.makedirs(screenshot_folder, exist_ok=True)

    # WebDriver servisini oluştur
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        email = config.EMAIL
        password = config.PASSWORD
        url = config.MIND_SITE_URL

        driver.get(url)
        time.sleep(5)

        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div[1]/div/form/div/div[1]/div[1]/div/div/div/div/input"))
        )
        email_input.send_keys(email)

        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div[1]/div/form/div/div[1]/div[2]/div/div/div/div/input"))
        )
        password_input.send_keys(password)
        time.sleep(2)

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[1]/div/form/div/div[3]/button"))
        )
        login_button.click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        screenshot_path = os.path.join(screenshot_folder, f"login_page_screenshot_{instance_id}.png")
        driver.save_screenshot(screenshot_path)
        print(f"Ekran görüntüsü alındı ve '{screenshot_path}' olarak kaydedildi.")
    finally:
        driver.quit()

def main():
    print("Mindsite screenshot işlemleri başlatılıyor...")

    num_processes = 1
    processes = []
    for i in range(num_processes):
        process = Process(target=take_screenshot, args=(i,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print("Tüm işlemler tamamlandı.")

if __name__ == '__main__':
    main()
