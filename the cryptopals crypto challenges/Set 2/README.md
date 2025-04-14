# Solution

## Bài 9
Giả sử bạn có một khối dữ liệu không đủ kích thước block (ví dụ: AES dùng block size 16 byte), bạn cần "đệm" thêm byte để vừa đủ block size.

PKCS#7 quy định:

Tính số byte cần thêm: `padding_len = block_size - len(data) % block_size`

Thêm `padding_len` byte, mỗi byte có giá trị là chính số `padding_len`.

