"""
testWindows.py - Test chuyển đổi giữa các cửa sổ (3.4 Windows)
Nhóm W4 - Tuần 6: Selenium Python
Tổng: 5 test case
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import switch_to_new_window, wait_for_new_window


class TestWindows:
    """Test suite cho việc mở và chuyển đổi giữa các cửa sổ."""

    URL = "https://the-internet.herokuapp.com/windows"

    # ── TC-W01: Lưu được handle cửa sổ gốc ──
    def test_get_current_window_handle(self, driver):
        """Kiểm tra lấy được handle cửa sổ hiện tại."""
        driver.get(self.URL)
        original = driver.current_window_handle
        assert original is not None
        assert len(original) > 0
        print(f"✅ Handle cửa sổ gốc: {original}")

    # ── TC-W02: Click mở cửa sổ mới ──
    def test_open_new_window(self, driver):
        """Kiểm tra click link mở được cửa sổ/tab mới."""
        driver.get(self.URL)
        original_handles = driver.window_handles
        assert len(original_handles) == 1

        # Click link "Click Here" để mở tab mới
        driver.find_element(By.LINK_TEXT, "Click Here").click()

        # Đợi cửa sổ mới xuất hiện
        WebDriverWait(driver, 10).until(
            EC.number_of_windows_to_be(2)
        )
        assert len(driver.window_handles) == 2
        print("✅ Đã mở thành công cửa sổ mới")

    # ── TC-W03: Chuyển sang cửa sổ mới và kiểm tra nội dung ──
    def test_switch_to_new_window(self, driver):
        """Kiểm tra switch sang cửa sổ mới và đọc nội dung."""
        driver.get(self.URL)
        original = driver.current_window_handle

        driver.find_element(By.LINK_TEXT, "Click Here").click()

        # Dùng helper để switch sang window mới
        new_handle = switch_to_new_window(driver, original)
        assert new_handle is not None
        assert driver.current_window_handle != original

        # Kiểm tra nội dung trang mới
        heading = driver.find_element(By.TAG_NAME, "h3")
        assert "New Window" in heading.text
        print(f"✅ Đã chuyển sang cửa sổ mới: '{heading.text}'")

    # ── TC-W04: Quay lại cửa sổ gốc ──
    def test_switch_back_to_original(self, driver):
        """Kiểm tra quay về được cửa sổ gốc sau khi switch."""
        driver.get(self.URL)
        original = driver.current_window_handle

        driver.find_element(By.LINK_TEXT, "Click Here").click()
        switch_to_new_window(driver, original)

        # Quay lại cửa sổ gốc
        driver.switch_to.window(original)
        assert driver.current_window_handle == original

        heading = driver.find_element(By.TAG_NAME, "h3")
        assert "Opening a new window" in heading.text
        print("✅ Đã quay lại cửa sổ gốc thành công")

    # ── TC-W05: Đóng cửa sổ mới và kiểm tra số lượng ──
    def test_close_new_window(self, driver):
        """Kiểm tra đóng cửa sổ mới, chỉ còn cửa sổ gốc."""
        driver.get(self.URL)
        original = driver.current_window_handle

        driver.find_element(By.LINK_TEXT, "Click Here").click()
        switch_to_new_window(driver, original)

        # Đóng cửa sổ mới
        driver.close()

        # Switch về cửa sổ gốc
        driver.switch_to.window(original)
        assert len(driver.window_handles) == 1
        assert driver.current_window_handle == original
        print("✅ Đã đóng cửa sổ mới, chỉ còn cửa sổ gốc")
