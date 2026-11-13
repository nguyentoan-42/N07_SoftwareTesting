import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By # Thư viện chứa các phương thức tìm kiếm phần tử (ID, NAME, CSS_SELECTOR...)

def test_valid_login():
    # Khởi tạo trình duyệt Chrome
    driver = webdriver.Chrome()
    # Mở URL của trang đăng nhập
    driver.get("https://the-internet.herokuapp.com/login")

    # Tìm ô Username qua thuộc tính ID="username" và nhập chữ "tomsmith". Tương tự với Password
    driver.find_element(By.ID, "username").send_keys("tomsmith") # ĐÚNG
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!") # ĐÚNG
    # Tìm nút "Login" bằng CSS Selector (nút có thuộc tính type='submit') và click vào nó
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Lấy phần tử chứa thông báo (có ID là "flash") sau khi bấm đăng nhập
    element = driver.find_element(By.ID, "flash")
    # Đảm bảo rằng phần tử thông báo này thực sự xuất hiện trên giao diện
    assert element is not None
    # Kiểm tra xem dòng text trong thông báo có chứa câu thành công hay không
    assert "You logged into a secure area!" in element.text

    # Đóng trình duyệt sau khi test xong
    driver.quit()

def test_invalid_password():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/login")

    # Nhập Username ĐÚNG, Password SAI
    driver.find_element(By.ID, "username").send_keys("tomsmith") # ĐÚNG
    driver.find_element(By.ID, "password").send_keys("wrongpassword") # SAI
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    element = driver.find_element(By.ID, "flash")
    assert element is not None
    # Xác nhận nội dung lỗi chính xác là sai mật khẩu
    assert "Your password is invalid!" in element.text
    
    driver.quit()

def test_invalid_username():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/login")

    # Nhập Username SAI, Password ĐÚNG
    driver.find_element(By.ID, "username").send_keys("wrongusername") # SAI
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!") # ĐÚNG
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    element = driver.find_element(By.ID, "flash")
    assert element is not None
    # Xác nhận nội dung lỗi chính xác là sai tên đăng nhập
    assert "Your username is invalid!" in element.text
    
    driver.quit()