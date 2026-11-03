import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Xử lý Windows & Explicit waits (3.4. Windows and frames & 5.1. Explicit Waits)
def test_windows_handling():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/windows")
    
    # Khởi tạo bộ đếm thời gian chờ tối đa 10 giây
    wait = WebDriverWait(driver, 10)

    # Lưu lại ID của cửa sổ gốc
    original_window = driver.current_window_handle

    # Click mở tab mới
    driver.find_element(By.LINK_TEXT, "Click Here").click()

    # Chờ đến khi tổng số cửa sổ mở ra là 2
    wait.until(EC.number_of_windows_to_be(2))

    # Lấy danh sách toàn bộ ID của các tab đang mở
    for window in driver.window_handles:
        if window != original_window:
            # Chuyển con trỏ sang tab mới
            driver.switch_to.window(window)
            break

    element = driver.find_element(By.TAG_NAME, "h3")
    assert element.text == "New Window"

    driver.quit()

# Xử lý Frames (3.4. Windows and frames)
def test_frames_handling():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/nested_frames")

    # Chuyển vào frame frame-top
    driver.switch_to.frame("frame-top")

    # Từ frame-top, đi tiếp vào frame con của nó (frame-middle)
    driver.switch_to.frame("frame-middle")
    assert driver.find_element(By.ID, "content").text == "MIDDLE"

    # Lùi lại 1 cấp (Từ middle lùi về top)
    driver.switch_to.parent_frame()

    # Thoát ra khỏi mọi frame, về thẳng HTML gốc
    driver.switch_to.default_content()

    driver.quit()

# Kết hợp Wait và Frame (3.4. Windows and frames & 5.1. Explicit Waits)
def test_frame_wait_and_switch():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/nested_frames")
    
    # Cài đặt thời gian chờ
    wait = WebDriverWait(driver, 10)

    # Đợi frame-bottom xuất hiện, có mặt là tự động switch_to.frame
    wait.until(EC.frame_to_be_available_and_switch_to_it("frame-bottom"))

    assert "BOTTOM" in driver.page_source
    driver.quit()

# Lịch sử và điều hướng (3.6. History and location)
def test_history_and_location():
    driver = webdriver.Chrome()
    
    # Truy cập trang này, sau đó truy cập trang sau
    driver.get("https://the-internet.herokuapp.com/windows")
    driver.get("https://the-internet.herokuapp.com/")

    # Nhấn nút Back trên trình duyệt để về trang trước đó
    driver.back()
    assert "windows" in driver.current_url

    # Nhấn nút Forward để tiến tới trang sau
    driver.forward()
    assert driver.current_url == "https://the-internet.herokuapp.com/"

    driver.quit()

# Quản lý Cookies (3.7. Cookies)
def test_cookies():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/windows")

    # Thêm một cookie mới vào trình duyệt
    driver.add_cookie({'name': 'Heisenberg', 'value': '99.1%'})
    
    # Lấy toàn bộ cookies hiện có
    cookies = driver.get_cookies()

    # Kiểm tra xem cookie vừa thêm có tồn tại không
    assert any(c['name'] == 'my_test_cookie' and c['value'] == '12345' for c in cookies) # vừa duyệt dữ liệu vừa kiểm tra
    
    driver.quit()

# Bắt lỗi (7.1. Exceptions)
def test_exceptions():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/windows")
    
    wait = WebDriverWait(driver, 2)

    # Dùng try-except để chương trình không bị sập khi gặp lỗi
    try:
        # Cố tình chờ 1 element không tồn tại để ép văng lỗi
        wait.until(EC.presence_of_element_located((By.ID, "id_khong_ton_tai")))
    except TimeoutException: 
        # Bắt đúng loại lỗi TimeoutException
        print("Đã bắt được lỗi do hết thời gian chờ.")
        pass

    driver.quit()

# Remote WebDriver (7.19. Remote WebDriver)
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
