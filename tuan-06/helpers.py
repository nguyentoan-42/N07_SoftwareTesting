"""
helpers.py - Hàm tiện ích dùng chung cho test suite
Nhóm W4 - Tuần 6: Selenium Python
"""
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def wait_for_new_window(driver, original_handles, timeout=10):
    """Đợi cho đến khi xuất hiện cửa sổ mới và trả về handle mới."""
    WebDriverWait(driver, timeout).until(
        EC.number_of_windows_to_be(len(original_handles) + 1)
    )
    new_handles = set(driver.window_handles) - set(original_handles)
    return new_handles.pop()


def switch_to_new_window(driver, original_handle, timeout=10):
    """Chuyển sang cửa sổ mới (khác cửa sổ gốc)."""
    WebDriverWait(driver, timeout).until(
        EC.number_of_windows_to_be(2)
    )
    for handle in driver.window_handles:
        if handle != original_handle:
            driver.switch_to.window(handle)
            return handle
    return None


def safe_switch_to_frame(driver, frame_locator, timeout=10):
    """Đợi frame sẵn sàng rồi switch vào."""
    WebDriverWait(driver, timeout).until(
        EC.frame_to_be_available_and_switch_to_it(frame_locator)
    )


def wait_for_element(driver, by, value, timeout=10):
    """Đợi element xuất hiện và trả về element đó."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )


def wait_for_element_clickable(driver, by, value, timeout=10):
    """Đợi element có thể click được."""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )


def add_test_cookie(driver, name="test_cookie", value="test_value"):
    """Thêm một cookie test vào trình duyệt."""
    cookie = {"name": name, "value": value}
    driver.add_cookie(cookie)
    return cookie


def get_all_cookie_names(driver):
    """Lấy danh sách tên tất cả cookies hiện tại."""
    return [c["name"] for c in driver.get_cookies()]
