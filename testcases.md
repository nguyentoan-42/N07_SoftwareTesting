
# Test chức năng Đăng nhập

## 1. TC-01: Đăng nhập thành công với tài khoản hợp lệ
- Các bước thực hiện:
  + Truy cập trang đăng nhập
  + Nhập Username ĐÚNG, Password ĐÚNG vào ô các tương ứng
  + Nhấn nút "Login"
- Dữ liệu đầu vào:
  + Username: tomsmith
  + Password: SuperSecretPassword!
- Kết quả mong đợi: "You logged into a secure area!"

## 2. TC-02: Đăng nhập thất bại do sai mật khẩu
- Các bước thực hiện:
  + Truy cập trang đăng nhập
  + Nhập Username ĐÚNG, Password SAI vào ô các tương ứng
  + Nhấn nút "Login"
- Dữ liệu đầu vào:
  + Username: tomsmith
  + Password: wrongpassword
- Kết quả mong đợi: "Your password is invalid!"

## 3. Đăng nhập thất bại do sai tên đăng nhập
- Các bước thực hiện:
  + Truy cập trang đăng nhập
  + Nhập Username SAI, Password ĐÚNG vào ô các tương ứng
  + Nhấn nút "Login"
- Dữ liệu đầu vào:
  + Username: wrongusername
  + Password: SuperSecretPassword!
- Kết quả mong đợi: "Your username is invalid!"
