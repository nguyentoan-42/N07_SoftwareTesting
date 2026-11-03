from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pytest


# Hàm hỗ trợ khởi tạo driver cho Cốc Cốc
def get_coccoc_driver():
  options = Options()
  # Đường dẫn tới file chạy của Cốc Cốc (Thay đổi nếu máy bạn cài ở thư mục khác)
  options.binary_location = (
      r"C:\Users\MCOM\AppData\Local\CocCoc\Browser\Application"
  )

  # Khởi tạo ChromeDriver với options của Cốc Cốc
  driver = webdriver.Chrome(options=options)
  return driver


# BÀI 1: COOKIE PHIÊN ĐĂNG NHẬP (Lưu và xóa trạng thái)
def test_login_and_cookies():
  driver = get_coccoc_driver()

  # Truy cập trang đăng nhập
  driver.get("https://the-internet.herokuapp.com/login")

  # Đăng nhập chuẩn
  driver.find_element(By.ID, "username").send_keys("tomsmith")
  driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
  driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

  # Đợi tối đa 10 giây để URL chuyển hướng sang trang secure
  WebDriverWait(driver, 10).until(EC.url_contains("secure"))
  assert "secure" in driver.current_url

  all_cookies = driver.get_cookies()
  assert len(all_cookies) > 0

  session_cookie = driver.get_cookie("rack.session")
  assert session_cookie is not None

  driver.add_cookie({"name": "Heisenberg", "value": "99.1%"})
  driver.delete_all_cookies()

  driver.refresh()
  assert "login" in driver.current_url

  driver.quit()


# BÀI 2: LỊCH SỬ DUYỆT WEB VÀ LINK TEXT
def test_history_and_link_text():
  driver = get_coccoc_driver()

  driver.get("https://the-internet.herokuapp.com")
  driver.get("https://the-internet.herokuapp.com/status_codes")

  driver.find_element(By.LINK_TEXT, "200").click()
  assert "200" in driver.current_url

  driver.back()
  assert "status_codes" in driver.current_url

  driver.forward()
  assert "200" in driver.current_url

  driver.back()  # Lùi về Status Codes
  driver.back()  # Lùi về trang chủ ban đầu

  # Kiểm tra lại URL trang chủ
  assert driver.current_url == "https://the-internet.herokuapp.com/"

  driver.quit()