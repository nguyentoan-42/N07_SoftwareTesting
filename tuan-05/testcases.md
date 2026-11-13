
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

# Test Khoá đăng nhập và Giới hạn ký tự

> Trang demo không có đặc tả nên dùng yêu cầu giả định:
> - Sai mật khẩu **5 lần liên tiếp** thì khoá tài khoản
> - Username: tối thiểu **3**, tối đa **20** ký tự
> - Password: tối thiểu **8**, tối đa **30** ký tự
>
> Script: `test_login_rules.py`

## 4. TC-04: Chưa khoá khi sai dưới ngưỡng
- Các bước thực hiện:
  + Nhập Username ĐÚNG, Password SAI, nhấn "Login" 4 lần
  + Lần thứ 5 nhập Username ĐÚNG, Password ĐÚNG
- Dữ liệu đầu vào: tomsmith / wrong0..wrong3, sau đó SuperSecretPassword!
- Kết quả mong đợi: "You logged into a secure area!"

## 5. TC-05: Khoá tài khoản khi sai đủ 5 lần
- Các bước thực hiện:
  + Nhập Username ĐÚNG, Password SAI, nhấn "Login" 5 lần
  + Lần thứ 6 nhập Username ĐÚNG, Password ĐÚNG
- Dữ liệu đầu vào: tomsmith / wrong0..wrong4, sau đó SuperSecretPassword!
- Kết quả mong đợi: Không đăng nhập được, có thông báo tài khoản bị khoá

## 6. TC-06: Giới hạn ký tự (phân tích giá trị biên)
| Trường | Độ dài nhập | Kết quả mong đợi |
| --- | --- | --- |
| Username | 0 (bỏ trống) | Không hợp lệ |
| Username | 2 (min - 1) | Không hợp lệ |
| Username | 3 (min) | Hợp lệ |
| Username | 20 (max) | Hợp lệ |
| Username | 21 (max + 1) | Ô nhập chỉ giữ lại 20 ký tự |
| Password | 0 (bỏ trống) | Không hợp lệ |
| Password | 7 (min - 1) | Không hợp lệ |
| Password | 8 (min) | Hợp lệ |
| Password | 30 (max) | Hợp lệ |
| Password | 31 (max + 1) | Ô nhập chỉ giữ lại 30 ký tự |

## Kết quả thực tế (chạy `pytest tuan-05/test_login_rules.py`)
| Test case | Kết quả | Ghi chú |
| --- | --- | --- |
| TC-04 Chưa khoá khi sai 4 lần | PASS | |
| TC-05 Khoá khi sai 5 lần | **FAIL** | Sai 5 lần rồi nhập đúng vẫn vào được: trang không có cơ chế khoá |
| TC-06 Username/Password đúng min, đúng max | PASS | |
| TC-06 Bỏ trống, min - 1 | **FAIL** | Ô nhập không có `required`/`minlength`, trình duyệt không chặn |
| TC-06 max + 1 | **FAIL** | Ô nhập không có `maxlength`, nhập bao nhiêu ký tự cũng được |

=> Kết luận: trang chưa đáp ứng yêu cầu khoá đăng nhập và giới hạn độ dài ký tự (5 PASS / 7 FAIL).
