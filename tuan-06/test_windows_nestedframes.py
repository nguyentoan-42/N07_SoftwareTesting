import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# BÀI 1: KIỂM THỬ XỬ LÝ WINDOWS (CỬA SỔ VÀ TAB MỚI)
# 3.4 Windows and frames - window_handles, current_window_handle, switch_to.window
# 5.1 Explicit Waits - EC.number_of_windows_to_be
def test_windows_handling():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/windows")
    
    # Khởi tạo bộ đếm thời gian chờ tối đa 10 giây
    wait = WebDriverWait(driver, 10)

    # current_window_handle
    # Lưu lại ID của cửa sổ gốc trước khi mở tab mới
    original_window = driver.current_window_handle

    # Click vào chữ "Click Here" để mở một tab mới
    driver.find_element(By.LINK_TEXT, "Click Here").click()

    # EC.number_of_windows_to_be()
    # Chờ cho đến khi tổng số cửa sổ trình duyệt đang mở bằng 2
    wait.until(EC.number_of_windows_to_be(2))

    # 3.4 Windows and frames - window_handles
    # Lấy danh sách ID của tất cả các cửa sổ trình duyệt đang mở
    for window in driver.window_handles:
        if window != original_window:
            # switch_to.window()
            # Chuyển sang tab mới vừa được mở
            driver.switch_to.window(window)
            break
    
    # Tìm thẻ h3 trên tab mới và kiểm tra nội dung hiển thị xem có đúng là "New Window" không
    element = driver.find_element(By.TAG_NAME, "h3")
    assert element.text == "New Window"

    driver.quit()


# BÀI 2: KIỂM THỬ XỬ LÝ FRAMES (KHUNG TRANG WEB)
# 3.4 Windows and frames - switch_to.frame, switch_to.parent_frame, switch_to.default_content
def test_frames_handling():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/nested_frames")

    # switch_to.frame()
    # Chuyển vào frame có tên "frame-top" để thao tác với nội dung bên trong frame này
    driver.switch_to.frame("frame-top")

    # Tiếp tục chuyển vào frame con có tên "frame-middle" nằm bên trong frame-top
    driver.switch_to.frame("frame-middle")
    # Tìm phần tử có id="content" và kiểm tra nội dung văn bản có đúng là "MIDDLE" không
    assert driver.find_element(By.ID, "content").text == "MIDDLE"

    # switch_to.parent_frame()
    # Quay lại frame cha, tức là từ frame-middle trở về frame-top
    driver.switch_to.parent_frame()

    # switch_to.default_content()
    # Thoát khỏi tất cả các frame và quay trở lại trang HTML gốc ban đầu
    driver.switch_to.default_content()

    driver.quit()


# BÀI 3: KẾT HỢP EXPLICIT WAITS VÀ FRAMES
# 3.4 Windows and frames - EC.frame_to_be_available_and_switch_to_it
# 5.1 Explicit Waits - EC.frame_to_be_available_and_switch_to_it
def test_frame_wait_and_switch():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/nested_frames")
    
    wait = WebDriverWait(driver, 10)

    # EC.frame_to_be_available_and_switch_to_it()
    # Chờ cho đến khi frame có tên "frame-bottom" xuất hiện và sẵn sàng thao tác. Khi tìm thấy, Selenium sẽ tự động chuyển vào frame đó
    wait.until(EC.frame_to_be_available_and_switch_to_it("frame-bottom"))

    # Kiểm tra mã nguồn trang hiện tại có chứa chữ "BOTTOM" hay không
    assert "BOTTOM" in driver.page_source
    driver.quit()


# BÀI 4: KIỂM THỬ LỊCH SỬ VÀ ĐIỀU HƯỚNG TRÌNH DUYỆT
# 3.6 History and location - back, forward, current_url
def test_history_and_location():
    driver = webdriver.Chrome()
    
    # get()
    # Truy cập trang Windows trước, sau đó truy cập trang chủ
    # Việc này tạo ra lịch sử điều hướng gồm 2 trang đã truy cập
    driver.get("https://the-internet.herokuapp.com/windows")
    driver.get("https://the-internet.herokuapp.com/")

    # back()
    # Nhấn nút Back trên trình duyệt để quay lại trang đã truy cập trước đó
    driver.back()
    # current_url
    # Kiểm tra URL hiện tại có chứa chữ "windows" hay không
    assert "windows" in driver.current_url

    # forward()
    # Nhấn nút Forward trên trình duyệt để chuyển tiếp đến trang tiếp theo
    driver.forward()
    # Kiểm tra URL hiện tại có đúng bằng địa chỉ trang chủ hay không
    assert driver.current_url == "https://the-internet.herokuapp.com/"

    driver.quit()


# BÀI 5: KIỂM THỬ QUẢN LÝ COOKIES
# 3.7 Cookies - add_cookie, get_cookies
def test_cookies():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/windows")

    # add_cookie()
    # Thêm một cookie mới vào trình duyệt tên là "my_test_cookie" với giá trị là "12345"
    driver.add_cookie({'name': 'my_test_cookie', 'value': '12345'})
    
    # get_cookies()
    # Lấy danh sách toàn bộ cookies hiện có của trang web
    cookies = driver.get_cookies()

    # Kiểm tra trong danh sách cookies có cookie vừa thêm hay không
    assert any(c['name'] == 'my_test_cookie' and c['value'] == '12345' for c in cookies) # vừa duyệt dữ liệu vừa kiểm tra
    
    driver.quit()


# BÀI 6: KIỂM THỬ XỬ LÝ NGOẠI LỆ (EXCEPTIONS)
# 7.1 Exceptions - TimeoutException, try-except
# 5.1 Explicit Waits - EC.presence_of_element_located
def test_exceptions():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/windows")
    
    wait = WebDriverWait(driver, 2)

    # try-except
    # Sử dụng try-except để bắt và xử lý lỗi phát sinh trong quá trình thực thi chương trình
    try:
        # EC.presence_of_element_located()
        # Cố tình chờ một phần tử có id="id_khong_ton_tai" không tồn tại trên trang web
        # Nếu hết 2 giây mà vẫn không tìm thấy, Selenium sẽ phát sinh lỗi TimeoutException
        wait.until(EC.presence_of_element_located(By.ID, "id_khong_ton_tai"))
    except TimeoutException: 
        # TimeoutException
        # Bắt đúng loại lỗi TimeoutException khi thời gian chờ đã hết
        print("Đã bắt được lỗi do hết thời gian chờ.")
        pass

    driver.quit()


# BÀI 7: KIỂM THỬ KẾT NỐI TỪ XA (REMOTE WEBDRIVER)
# 7.19 Remote WebDriver - webdriver.Remote
def test_remote_webdriver():
    # Phải có Selenium Server đang chạy ở port 4444 thì đoạn này mới hoạt động
    try:
        options = webdriver.ChromeOptions()
        
        # webdriver.Remote()
        # Thay vì khởi tạo trình duyệt trực tiếp bằng webdriver.Chrome() thì ở đây sử dụng webdriver.Remote() để kết nối đến máy chủ Selenium từ xa
        driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            options=options
        )

        # Truy cập trang Windows thông qua trình duyệt được điều khiển từ xa
        driver.get("https://the-internet.herokuapp.com/windows")
        # Kiểm tra tiêu đề trang web có chứa chữ "The Internet" hay không
        assert "The Internet" in driver.title
        driver.quit()
    
    except Exception:
        print("Bỏ qua bài test này vì không có Selenium Server port 4444")
