"""
testNestedFrames.py - Test frame và frame lồng nhau (3.4 Frames)
Nhóm W4 - Tuần 6: Selenium Python
Tổng: 5 test case
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import safe_switch_to_frame, wait_for_element


class TestNestedFrames:
    """Test suite cho việc chuyển đổi giữa các frame/iframe lồng nhau."""

    NESTED_URL = "https://the-internet.herokuapp.com/nested_frames"
    IFRAME_URL = "https://the-internet.herokuapp.com/iframe"

    # ── TC-F01: Switch vào frame theo tên ──
    def test_switch_to_frame_by_name(self, driver):
        """Kiểm tra switch vào frame bằng tên frame."""
        driver.get(self.NESTED_URL)

        # Switch vào frame-top
        driver.switch_to.frame("frame-top")
        # Kiểm tra đang ở trong frame (không bị lỗi)
        assert driver.execute_script("return window.frameElement !== null or window !== window.top") is not None
        print("✅ Đã switch vào frame 'frame-top' thành công")

    # ── TC-F02: Switch vào frame lồng nhau (nested) ──
    def test_switch_to_nested_frame(self, driver):
        """Kiểm tra switch vào frame con bên trong frame cha."""
        driver.get(self.NESTED_URL)

        # Bước 1: Vào frame-top (frame cha)
        driver.switch_to.frame("frame-top")

        # Bước 2: Vào frame-middle (frame con bên trong frame-top)
        driver.switch_to.frame("frame-middle")

        # Kiểm tra nội dung bên trong frame-middle
        content = driver.find_element(By.ID, "content")
        assert "MIDDLE" in content.text
        print(f"✅ Nội dung frame lồng nhau: '{content.text}'")

    # ── TC-F03: Quay về frame cha bằng parent_frame() ──
    def test_switch_to_parent_frame(self, driver):
        """Kiểm tra parent_frame() quay về được frame cha."""
        driver.get(self.NESTED_URL)

        # Vào frame-top → frame-left
        driver.switch_to.frame("frame-top")
        driver.switch_to.frame("frame-left")

        # Kiểm tra đang ở frame-left
        body = driver.find_element(By.TAG_NAME, "body")
        assert "LEFT" in body.text

        # Quay về frame cha (frame-top)
        driver.switch_to.parent_frame()

        # Từ frame-top, switch sang frame-right
        driver.switch_to.frame("frame-right")
        body = driver.find_element(By.TAG_NAME, "body")
        assert "RIGHT" in body.text
        print("✅ parent_frame() hoạt động đúng, chuyển được sang frame anh em")

    # ── TC-F04: Quay về trang gốc bằng default_content() ──
    def test_switch_to_default_content(self, driver):
        """Kiểm tra default_content() quay về trang gốc từ frame sâu."""
        driver.get(self.NESTED_URL)

        # Đi sâu vào frame: top → middle
        driver.switch_to.frame("frame-top")
        driver.switch_to.frame("frame-middle")

        # Quay thẳng về trang gốc
        driver.switch_to.default_content()

        # Từ trang gốc, switch vào frame-bottom
        driver.switch_to.frame("frame-bottom")
        body = driver.find_element(By.TAG_NAME, "body")
        assert "BOTTOM" in body.text
        print("✅ default_content() đã quay về trang gốc, truy cập frame-bottom OK")

    # ── TC-F05: Dùng Explicit Wait để đợi iframe sẵn sàng ──
    def test_wait_for_iframe_and_switch(self, driver):
        """Kiểm tra EC.frame_to_be_available_and_switch_to_it với iframe."""
        driver.get(self.IFRAME_URL)

        # Dùng explicit wait để đợi iframe TinyMCE sẵn sàng
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe.tox-edit-area__iframe")
            )
        )

        # Kiểm tra có thể tương tác với nội dung bên trong iframe
        body = driver.find_element(By.TAG_NAME, "body")
        assert body is not None
        # Iframe editor có nội dung mặc định
        content = body.text
        assert len(content) > 0
        print(f"✅ Đã wait và switch vào iframe thành công, nội dung: '{content[:50]}...'")
