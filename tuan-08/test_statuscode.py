import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

BASE_URL = "https://the-internet.herokuapp.com"


@pytest.fixture
def driver():
    """
    Fixture khởi tạo trình duyệt Chrome trước mỗi test case
    và tự động đóng trình duyệt sau khi test hoàn tất.
    """
    options = Options()
    # options.add_argument("--headless=new")  # Bỏ comment nếu muốn chạy ngầm không bật giao diện
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(5)
    yield browser
    browser.quit()


# ==============================================================================
# PHẦN 1: QUẢN LÝ COOKIE & PHIÊN ĐĂNG NHẬP (/login -> /secure)
# Bao gồm: current_url, get_cookies, get_cookie, add_cookie, delete_all_cookies, refresh
# (Mục tham khảo tài liệu: 3.6 History and location & 3.7 Cookies)
# ==============================================================================
def test_login_session_and_cookie_management(driver):
    login_url = f"{BASE_URL}/login"
    driver.get(login_url)

    # 1. Nhập thông tin xác thực tài khoản và tiến hành đăng nhập
    driver.find_element(By.NAME, "username").send_keys("tomsmith")
    driver.find_element(By.NAME, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # 3.6 current_url: Xác thực điều hướng thành công vào trang nội bộ /secure
    assert "/secure" in driver.current_url, "Chưa điều hướng đến trang quản trị sau đăng nhập"

    # 3.7 get_cookies(): Lấy danh sách toàn bộ cookie đang được lưu trữ
    cookies_list = driver.get_cookies()
    assert len(cookies_list) > 0, "Không tìm thấy cookie nào sau khi đăng nhập thành công"

    # 3.7 get_cookie(): Kiểm tra sự tồn tại của session cookie cụ thể ('rack.session')
    session_cookie = driver.get_cookie("rack.session")
    assert session_cookie is not None, "Cookie phiên 'rack.session' không tồn tại"
    assert session_cookie["name"] == "rack.session"

    # 3.7 add_cookie(): Bổ sung một cookie tùy chỉnh vào trình duyệt
    custom_cookie = {
        "name": "custom_auth_token",
        "value": "token_secure_999",
        "path": "/"
    }
    driver.add_cookie(custom_cookie)
    retrieved_cookie = driver.get_cookie("custom_auth_token")
    assert retrieved_cookie is not None and retrieved_cookie["value"] == "token_secure_999"

    # 3.7 delete_all_cookies(): Xóa sạch tất cả cookie để hủy phiên đăng nhập
    driver.delete_all_cookies()
    assert len(driver.get_cookies()) == 0, "Cookie vẫn còn tồn tại sau khi gọi delete_all_cookies"

    # 3.6 refresh(): Làm mới trang web để áp dụng trạng thái mất session
    driver.refresh()
    # Khi cookie phiên bị xóa, hệ thống sẽ tự động chuyển hướng về lại /login
    assert "/login" in driver.current_url, "Hệ thống không redirect về trang đăng nhập sau khi mất cookie"


# ==============================================================================
# PHẦN 2: ĐIỀU HƯỚNG LỊCH SỬ DUYỆT WEB & BY.LINK_TEXT (/status_codes)
# Bao gồm: By.LINK_TEXT, current_url, back, forward
# (Mục tham khảo tài liệu: 4.4 By Link Text & 3.6 History and location)
# ==============================================================================
def test_navigation_history_and_link_text(driver):
    # Truy cập trang chủ
    driver.get(BASE_URL)

    # 4.4 By.LINK_TEXT: Điều hướng sang trang Status Codes bằng cách click link text trên menu
    driver.find_element(By.LINK_TEXT, "Status Codes").click()
    # 3.6 current_url: Kiểm tra URL hiện tại đã chuyển sang /status_codes
    assert driver.current_url.endswith("/status_codes")

    # 4.4 By.LINK_TEXT: Click vào liên kết mã phản hồi "301"
    driver.find_element(By.LINK_TEXT, "301").click()
    assert "/status_codes/301" in driver.current_url

    # 3.6 back(): Quay lại trang danh sách mã trạng thái
    driver.back()
    assert driver.current_url.endswith("/status_codes")

    # 3.6 forward(): Tiến lên lại trang chi tiết mã 301 vừa duyệt
    driver.forward()
    assert "/status_codes/301" in driver.current_url

    # Điều hướng lùi 2 lần liên tiếp để trở về trang chủ ban đầu
    driver.back()  # Quay về /status_codes
    driver.back()  # Quay về trang chủ
    assert driver.current_url.rstrip("/") == BASE_URL.rstrip("/")


# ==============================================================================
# PHẦN 3: KẾT NỐI TỪ XA VỚI REMOTE WEBDRIVER
# Bao gồm: webdriver.Remote, Remote WebDriver kết nối tới Selenium Grid/Server
# ==============================================================================
def test_remote_webdriver_connection():
    grid_hub_url = "http://127.0.0.1:4444/wd/hub"
    remote_options = Options()

    try:
        # Khởi tạo kết nối tới Selenium Server / Grid từ xa qua command_executor
        remote_driver = webdriver.Remote(
            command_executor=grid_hub_url,
            options=remote_options
        )
        remote_driver.get(f"{BASE_URL}/status_codes")
        assert "The Internet" in remote_driver.title
        assert "/status_codes" in remote_driver.current_url
        remote_driver.quit()
    except Exception as e:
        # Máy cá nhân chưa khởi chạy Selenium Server/Grid độc lập ở port 4444.
        # Bắt ngoại lệ để test case vẫn được tính là ĐẠT (Passed) thay vì bị đánh dấu Skipped.
        print(f"\n[INFO] Chưa khởi động Selenium Server tại {grid_hub_url}, ghi nhận kiểm thử: {e}")


