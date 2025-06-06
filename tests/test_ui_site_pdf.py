import os
import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")  # папка для загрузок

@allure.title("Клик на PDF и проверка загрузки")
def test_click_pdf_and_check_download():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True
    })
    # 🔽 ЭТО ОБЯЗАТЕЛЬНО ДЛЯ CI!
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()

    with allure.step("Открываем сайт"):
        driver.get("https://antonvolodin.github.io/visit_card_1/")
        time.sleep(2)

    with allure.step("Кликаем по ссылке PDF"):
        pdf_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "PDF"))
        )
        pdf_link.click()

    with allure.step("Ожидаем скачивание PDF"):
        file_downloaded = False
        for _ in range(10):
            if any(fname.endswith(".pdf") for fname in os.listdir(DOWNLOAD_DIR)):
                file_downloaded = True
                break
            time.sleep(1)

    driver.quit()
    assert file_downloaded, "PDF файл не был загружен"
