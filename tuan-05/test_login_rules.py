import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://the-internet.herokuapp.com/login"

# Yêu cầu giả định (trang demo không có đặc tả)
MAX_FAILED_ATTEMPTS = 5   # Sai 5 lần liên tiếp thì khoá tài khoản
USERNAME_MIN, USERNAME_MAX = 3, 20
PASSWORD_MIN, PASSWORD_MAX = 8, 30


@pytest.fixture
def driver():
    # Dùng fixture để trình duyệt luôn được đóng, kể cả khi assert thất bại
    driver = webdriver.Chrome()
    driver.get(URL)
    yield driver
    driver.quit()


def login(driver, username, password):
    # Mở lại trang mỗi lần để không đọc nhầm thông báo của lần đăng nhập trước
    driver.get(URL)
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    # Chờ trang tải xong và thông báo xuất hiện
    flash = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "flash"))
    )
    return flash.text


# ---------- Khoá đăng nhập khi nhập sai ----------

def test_not_locked_before_limit(driver):
    # Sai 4 lần (dưới ngưỡng) thì lần 5 nhập đúng vẫn phải đăng nhập được
    for i in range(MAX_FAILED_ATTEMPTS - 1):
        assert "Your password is invalid!" in login(driver, "tomsmith", f"wrong{i}")
    assert "You logged into a secure area!" in login(driver, "tomsmith", "SuperSecretPassword!")


def test_locked_after_limit(driver):
    # Sai đủ 5 lần thì tài khoản bị khoá: nhập đúng mật khẩu cũng không vào được
    for i in range(MAX_FAILED_ATTEMPTS):
        login(driver, "tomsmith", f"wrong{i}")
    message = login(driver, "tomsmith", "SuperSecretPassword!")
    assert "You logged into a secure area!" not in message


# ---------- Giới hạn tối thiểu/tối đa ký tự (phân tích giá trị biên) ----------

def is_valid(driver, element):
    # Dùng Constraint Validation API của trình duyệt (minlength/maxlength/required)
    return driver.execute_script("return arguments[0].checkValidity();", element)


@pytest.mark.parametrize("field_id, max_len", [
    ("username", USERNAME_MAX),
    ("password", PASSWORD_MAX),
])
def test_max_length(driver, field_id, max_len):
    # Nhập max + 1 ký tự: ô nhập chỉ được giữ lại tối đa max ký tự
    element = driver.find_element(By.ID, field_id)
    element.send_keys("a" * (max_len + 1))
    assert len(element.get_attribute("value")) == max_len


@pytest.mark.parametrize("field_id, length, expected_valid", [
    ("username", USERNAME_MIN - 1, False),
    ("username", USERNAME_MIN, True),
    ("username", USERNAME_MAX, True),
    ("password", PASSWORD_MIN - 1, False),
    ("password", PASSWORD_MIN, True),
    ("password", PASSWORD_MAX, True),
])
def test_length_boundaries(driver, field_id, length, expected_valid):
    element = driver.find_element(By.ID, field_id)
    element.send_keys("a" * length)
    assert is_valid(driver, element) == expected_valid


@pytest.mark.parametrize("field_id", ["username", "password"])
def test_empty_field_rejected(driver, field_id):
    # Bỏ trống thì trình duyệt phải chặn, không gửi form
    element = driver.find_element(By.ID, field_id)
    assert not is_valid(driver, element)
