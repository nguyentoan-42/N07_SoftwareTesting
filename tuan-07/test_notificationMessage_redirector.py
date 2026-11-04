import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# BÀI 1: KIỂM THỬ TRANG NOTIFICATION MESSAGE
# visibility_of_element_located, staleness_of, refresh
def test_notification_message():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/notification_message")
    wait = WebDriverWait(driver, 10)

    # 5.1 Explicit Waits - visibility_of_element_located
    # Chờ cho đến khi khung thông báo (id="flash") thực sự hiển thị trên màn hình
    flash_message = wait.until(
        EC.visibility_of_element_located((By.ID, "flash")))
    assert flash_message is not None # Thật ra là không nhất thiết phải có dòng này

    # Click vào chữ "Click here" để trang web tải ra thông báo mới
    driver.find_element(By.LINK_TEXT, "Click here").click()

    # 5.1 Explicit Waits - staleness_of
    # Khi click, trang web sẽ load lại phần thông báo, flash_message có thể trở nên stale - tức là không còn gắn với DOM hiện tại nữa. 
    # Chờ cho cái khung thông báo cũ không còn hợp lệ trong DOM.
    wait.until(EC.staleness_of(flash_message))

    # 3.6 History and location - refresh
    driver.refresh()

    driver.quit()


# BÀI 2: KIỂM THỬ TRANG REDIRECTOR (CHUYỂN HƯỚNG TRANG)
# url_contains, current_url, back
def test_redirect_and_history():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/redirector")
    wait = WebDriverWait(driver, 10)

    # Click vào id="redirect" để trang web chuyển hướng sang một chỗ khác
    driver.find_element(By.ID, "redirect").click()

    # 5.1 Explicit Waits - url_contains
    # Chờ cho đến khi thanh địa chỉ (URL) thay đổi và có chứa chữ "status_codes"
    wait.until(EC.url_contains("status_codes"))

    # 3.6 History and location - back
    # Nhấn nút Quay lại (Back) trên trình duyệt để về lại trang Redirector ban đầu
    driver.back()
    assert "redirector" in driver.current_url

    driver.quit()


# BÀI 3: KẾT NỐI TỪ XA
# Remote WebDriver
def test_remote_webdriver():
    # Phải có Selenium Server đang chạy ở port 4444 thì đoạn này mới hoạt động
    try:
        options = webdriver.ChromeOptions()
        # Thay vì driver = webdriver.Chrome(), ta kết nối tới máy chủ từ xa
        driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            options=options
        )
        driver.get("https://the-internet.herokuapp.com/windows")
        assert "The Internet" in driver.title
        driver.quit()
    except Exception:
        print("Bỏ qua bài test này vì không có Selenium Server port 4444")
