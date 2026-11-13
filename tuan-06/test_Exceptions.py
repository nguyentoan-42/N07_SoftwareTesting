"""
testExceptions.py - Test xử lý ngoại lệ (7.1 Exceptions)
Nhóm W4 - Tuần 6: Selenium Python
Tổng: 5 test case
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchWindowException,
    NoSuchFrameException,
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
)


class TestExceptions:
    """Test suite cho xử lý ngoại lệ trong Selenium."""

    BASE_URL = "https://the-internet.herokuapp.com"

    # ── TC-E01: NoSuchWindowException khi switch vào handle không hợp lệ ──
    def test_no_such_window_exception(self, driver):
        """Kiểm tra bắt NoSuchWindowException với handle sai."""
        driver.get(self.BASE_URL)

        with pytest.raises(NoSuchWindowException):
            driver.switch_to.window("invalid_handle_12345")
        print("✅ Bắt được NoSuchWindowException khi handle không hợp lệ")

    # ── TC-E02: NoSuchFrameException khi switch vào frame không tồn tại ──
    def test_no_such_frame_exception(self, driver):
        """Kiểm tra bắt NoSuchFrameException với frame không tồn tại."""
        driver.get(self.BASE_URL)

        with pytest.raises(NoSuchFrameException):
            driver.switch_to.frame("frame_khong_ton_tai")
        print("✅ Bắt được NoSuchFrameException khi frame không tồn tại")

    # ── TC-E03: TimeoutException khi WebDriverWait hết thời gian ──
    def test_timeout_exception(self, driver):
        """Kiểm tra bắt TimeoutException khi chờ quá lâu."""
        driver.get(self.BASE_URL)

        with pytest.raises(TimeoutException):
            # Đợi 2 cửa sổ nhưng chỉ có 1 → timeout sau 2 giây
            WebDriverWait(driver, 2).until(
                EC.number_of_windows_to_be(5)
            )
        print("✅ Bắt được TimeoutException khi chờ quá thời gian")

    # ── TC-E04: NoSuchElementException khi tìm element không có ──
    def test_no_such_element_exception(self, driver):
        """Kiểm tra bắt NoSuchElementException khi element không tồn tại."""
        driver.get(self.BASE_URL)
        driver.implicitly_wait(0)  # Tắt implicit wait để test nhanh

        with pytest.raises(NoSuchElementException):
            driver.find_element(By.ID, "element_khong_co_that")
        print("✅ Bắt được NoSuchElementException khi element không tồn tại")

    # ── TC-E05: StaleElementReferenceException khi element bị thay đổi DOM ──
    def test_stale_element_exception(self, driver):
        """Kiểm tra bắt StaleElementReferenceException sau khi DOM thay đổi."""
        driver.get(f"{self.BASE_URL}/add_remove_elements/")

        # Click nút "Add Element" để tạo element mới
        add_btn = driver.find_element(By.XPATH, "//button[text()='Add Element']")
        add_btn.click()

        # Lấy reference element mới tạo
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[text()='Delete']")
            )
        )

        # Xóa element khỏi DOM bằng click chính nó
        element.click()

        # Element đã bị xóa → truy cập sẽ gặp StaleElementReferenceException
        with pytest.raises(StaleElementReferenceException):
            element.click()  # Element không còn trong DOM
        print("✅ Bắt được StaleElementReferenceException sau khi DOM thay đổi")
