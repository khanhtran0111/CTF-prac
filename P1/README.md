# Solution

Nếu quan sát kĩ, thì ta có thể thấy xâu ban đầu được cho sẽ chỉ gồm các kí tự thường và chữ số (a->z và 0->9)
=> Khả năng lớn sẽ liên quan đến mã hóa Hex.
-> Thử in số lượng chữ cái trong mã.

Thử giải mã từ Hex, kiểm tra độ dài ta thấy số lượng có giảm đi và chuỗi kí tự trở thành mã hóa Base64.
```
data.decode()
```

Thử decode lần nữa từ Base64 chúng ta lại thu được chuỗi ở dạng mã hóa Hex

*Ý tưởng*: Chúng ta sẽ liên tục decode xen kẽ giũa Hex và Base64 cho tới plain text cuối cùng chính là Flag cần tìm.