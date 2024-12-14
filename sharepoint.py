from selenium import webdriver
from selenium.webdriver.common.by import By
import  time
driver = webdriver.Chrome()

url ="https://onedrive.live.com/login/"

email= "fehmitahsindemirkan@gmail.com"
password ="2003Ftd2003!"

driver.get(url)
driver.find_element(By.XPATH,"/html/body/div[2]/div/main/div[2]/div[2]/div/input").send_keys(email)
time.sleep(2)
driver.find_element(By.XPATH,"/html/body/div[2]/div/main/div[2]/div[4]/input").click()
time.sleep(2)
driver.close()