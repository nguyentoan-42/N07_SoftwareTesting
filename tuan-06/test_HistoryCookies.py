"""
testHistoryCookies.py - Test History/Navigation (3.6) và Cookies (3.7)
Nhóm W4 - Tuần 6: Selenium Python
Tổng: 5 test case
"""
import pytest
from selenium.webdriver.common.by import By
from helpers import add_test_cookie, get_all_cookie_names


class TestHistoryNavigation:
    """Test suite cho History & Navigation (3.6)."""

    BASE_URL = "https://the-internet.herokuapp.com"

    # ── TC-H01: Điều hướng bằng driver.get() ──
    def test_navigate_with_get(self, driver):
        """Kiểm tra driver.get() truy cập đúng URL."""
        driver.get(self.BASE_URL)
        assert "the-internet" in driver.current_url
        assert "Welcome" in driver.title or "The Internet" in driver.title
        print(f"✅ Đã truy cập: {driver.current_url}")

    # ── TC-H02: Quay lại trang trước bằng back() ──
    def test_navigate_back(self, driver):
        """Kiểm tra driver.back() quay lại trang trước."""
        driver.get(self.BASE_URL)
        original_url = driver.current_url

        # Truy cập trang con
        driver.get(f"{self.BASE_URL}/login")
        assert "login" in driver.current_url

        # Quay lại
        driver.back()
        assert driver.current_url == original_url
        print("✅ driver.back() hoạt động đúng")

    # ── TC-H03: Tiến tới bằng forward() ──
    def test_navigate_forward(self, driver):
        """Kiểm tra driver.forward() tiến lại trang đã back."""
        driver.get(self.BASE_URL)
        driver.get(f"{self.BASE_URL}/login")
        login_url = driver.current_url

        driver.back()  # Quay lại trang chính
        driver.forward()  # Tiến lại trang login

        assert driver.current_url == login_url
        print("✅ driver.forward() hoạt động đúng")


class TestCookies:
    """Test suite cho quản lý Cookies (3.7)."""

    BASE_URL = "https://the-internet.herokuapp.com"

    # ── TC-C01: Thêm và đọc cookie ──
    def test_add_and_get_cookie(self, driver):
        """Kiểm tra thêm cookie và đọc lại đúng giá trị."""
        driver.get(self.BASE_URL)

        # Thêm cookie
        add_test_cookie(driver, "user_session", "xyz789")

        # Đọc lại cookie
        cookie = driver.get_cookie("user_session")
        assert cookie is not None
        assert cookie["name"] == "user_session"
        assert cookie["value"] == "xyz789"
        print(f"✅ Cookie: {cookie['name']} = {cookie['value']}")

    # ── TC-C02: Xóa cookie cụ thể và xóa tất cả ──
    def test_delete_cookies(self, driver):
        """Kiểm tra xóa cookie đơn lẻ và xóa tất cả."""
        driver.get(self.BASE_URL)

        # Thêm 2 cookies
        add_test_cookie(driver, "cookie_a", "value_a")
        add_test_cookie(driver, "cookie_b", "value_b")
        assert "cookie_a" in get_all_cookie_names(driver)
        assert "cookie_b" in get_all_cookie_names(driver)

        # Xóa 1 cookie
        driver.delete_cookie("cookie_a")
        assert "cookie_a" not in get_all_cookie_names(driver)
        assert "cookie_b" in get_all_cookie_names(driver)
        print("✅ Xóa cookie_a thành công")

        # Xóa tất cả
        driver.delete_all_cookies()
        assert len(driver.get_cookies()) == 0
        print("✅ Xóa tất cả cookies thành công")
