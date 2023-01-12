import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import random

value = str(input("Введите строку поиска: "))
s = Service(r"D:\pet-project\sel_parser\chromedriver\chromedriver.exe")
driver = webdriver.Chrome(service=s)
url = "https://www.avito.ru/"

try:
    driver.get(url=url)
    driver.maximize_window()
    search_input = driver.find_element(By.CLASS_NAME, "input-input-Zpzc1")  # Находим ввод по классу
    search_input.clear()  # Очищаем строку ввода на всякий случай если на ней что-нибудь написано
    search_input.send_keys(f"{value}")  # Вводим наш инпут в строку
    search_input.send_keys(Keys.ENTER)  # Нажмём ENTER
    soup = BeautifulSoup(driver.page_source, "lxml")
    # ------------ Парсинг всех страниц
    item_divs = soup.find_all("span", class_="pagination-item-JJq_j")
    last_elem = int(item_divs[-2].getText())  # последний элемент
    result_list = []
    for i in range(1, last_elem+1):
        time.sleep(random.randrange(2, 10))
        if i % 10 == 0:
            time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "lxml")
        items_divs0 = soup.find_all("div",
                                    class_="iva-item-content-rejJg")

        avito_url = "https://www.avito.ru"
        for item in items_divs0:
            item_url = item.find("div", class_="iva-item-titleStep-pdebR").find("a").get("href")

            item_name = item.find("div", class_="iva-item-titleStep-pdebR").find("h3",
                                                                                 {"itemprop": "name"}).text.strip()

            price = item.find("span", class_="price-text-_YGDY text-text-LurtD text-size-s-BxGpL").text.strip()

            result_list.append({"Название объявления": item_name,
                                "Ссылка": avito_url + item_url,
                                "Цена": price.replace(" ", " ")}
                               )
        print(f"В процесce : {i}/{last_elem}")
        if i != last_elem:
            driver.find_element(By.XPATH, "//span[@data-marker='pagination-button/next']").click()  # Находим по Xpath

    time.sleep(5)
    with open("result.json", "w", encoding="utf-8") as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)

    print("Данные успешно записаны в result.json! ")
finally:
    driver.close()
    driver.quit()
