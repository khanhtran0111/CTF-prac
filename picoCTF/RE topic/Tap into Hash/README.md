# Solution

## Phân tích block_chain.py
- XOR là phép khả nghịch: để giải chỉ cần XOR lại với cùng khối key_hash[:16].
- Mã hoá không thay đổi thứ tự byte, chỉ nhúng thêm inner_txt (flag) vào chính giữa chuỗi gốc.
- Phần pad là PKCS#7: giá trị padding (k) lặp lại k lần ở cuối.

## Phân tích enc_flag sau khi thu đươc
File này bao gồm 2 dòng Plain-text:
-Key: literal bytes (32 bytes)
- Encrypted Blockchain: literal bytes của ciphertext