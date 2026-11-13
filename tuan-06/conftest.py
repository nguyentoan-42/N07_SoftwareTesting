"""
Conftest.py - Cấu hình chung cho toàn bộ test suite
Nhóm W4 - Tuần 6: Selenium Python
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="function")
def driver():
    """Khởi tạo Chrome WebDriver cho mỗi test function."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-popup-blocking")
    # Bỏ comment dòng dưới nếu muốn chạy headless
    # chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)

    yield driver

    # Teardown: đóng tất cả cửa sổ và thoát driver
    driver.quit()


@pytest.fixture(scope="function")
def driver_with_base_url(driver):
    """Driver đã truy cập trang test mặc định."""
    driver.get("https://the-internet.herokuapp.com")
    return driver
