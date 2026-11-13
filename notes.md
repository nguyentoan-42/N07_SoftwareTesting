#GHI CHÚ - Tuần 5

## Kiến thức
- Biết cách kiểm tra cấu trúc HTML/DOM của trang web bằng Chrome DevTools. Xác định chính xác các phần tử HTML mà Selenium cần thao tác, chẳng hạn như ô nhập username, ô nhập password và nút Login
- Biết cách thao tác với các phần tử sau khi đã xác định được chúng

## Trả lời câu hỏi
1. Với ô tên đăng nhập ở trang /login, nên xác định bằng cách nào là ổn định nhất, vì sao?
- Nên ưu tiên dùng By.ID vì ID dùng để xác định một phần tử cụ thể trên trang

2. Muốn nhập chữ vào một ô thì dùng lệnh gì?
- Muốn nhập chữ vào một ô, ta dùng phương thức send_keys() của Selenium

3. Làm thế nào để biết id của một ô nhập trên trang?
- Sử dụng Chrome DevTools để xác định:
  + Inspect (kiểm tra) ô nhập
  + Tại vùng HTML được bôi đen trong tab Elements (thuộc tính) có thể xác định được `id` của thẻ `<input>`

## Sử dụng AI
- Làm rõ hơn các kiến thức Selenium – Locator strategies & Interacting with elements => biết cách viết script hoạt động được
- Kiểm tra script => Code sạch hơn
