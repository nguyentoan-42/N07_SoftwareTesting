import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


# BÀI 1: COOKIE PHIÊN ĐĂNG NHẬP (Lưu và xóa trạng thái)
# current_url, get_cookies, get_cookie, add_cookie, delete_all_cookies, refresh
def test_login_and_cookies():
    driver = webdriver.Chrome()
    
    # Truy cập trang đăng nhập
    driver.get("https://the-internet.herokuapp.com/login")

    # Đăng nhập chuẩn (nhập Username, Password rồi bấm nút Login)
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # 3.6 History and location - current_url
    # Kiểm tra xem đã nhảy sang trang "/secure" chưa
    assert "secure" in driver.current_url

    # 3.7 Cookies - get_cookies()
    # Lấy toàn bộ Cookie mà trang web vừa cấp sau khi đăng nhập thành công
    all_cookies = driver.get_cookies()
    assert len(all_cookies) > 0

    # 3.7 Cookies - get_cookie()
    # Lấy một Cookie cụ thể mang tên "rack.session"
    session_cookie = driver.get_cookie("rack.session")
    assert session_cookie is not None

    # 3.7 Cookies - add_cookie
    # Nhét một cookie tự chế vào trình duyệt
    driver.add_cookie({"name": "Heisenberg", "value": "99.1%"})

    # 3.7 Cookies - delete_all_cookies()
    # Xóa toàn bộ Cookies (đồng nghĩa với Đăng xuất)
    driver.delete_all_cookies()

    # 3.6 History and location - refresh()
    # Tải lại trang. Do đã bị xóa hết Cookie, web sẽ đẩy về lại trang /login
    driver.refresh()
    assert "login" in driver.current_url

    driver.quit()


# BÀI 2: LỊCH SỬ DUYỆT WEB VÀ LINK TEXT
# By.LINK_TEXT, back, forward, current_url
def test_history_and_link_text():
    driver = webdriver.Chrome()
    
    # Truy cập trang the-internet
    driver.get("https://the-internet.herokuapp.com")
    
    # Truy cập sang trang Status Codes
    driver.get("https://the-internet.herokuapp.com/status_codes")

    # 4.4 By Link Text - By.LINK_TEXT
    # Tìm đường link có chữ "200" trên màn hình rồi Click vào nó
    driver.find_element(By.LINK_TEXT, "200").click()

    # 3.6 History and location - current_url
    # Đảm bảo ta đã sang đúng trang có đuôi là 200
    assert "200" in driver.current_url

    # 3.6 History and location - back
    # Bấm nút Lùi Lại (về trang Status Codes)
    driver.back()
    assert "status_codes" in driver.current_url

    # 3.6 History and location - forward
    # Bấm nút Tiến Lên (về lại trang 200)
    driver.forward()
    assert "200" in driver.current_url

    # Bấm Lùi Lại 2 lần để về tận trang chủ the-internet ban đầu
    driver.back() # Lùi về Status Codes
    driver.back() # Lùi về trang chủ the-internet
    assert driver.current_url == "https://the-internet.herokuapp.com/"

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
