## Solution

Chương trình “đọc” lời bài hát có các đoạn **verse** và **refrain** như các subroutine, nhưng phần mở đầu (hidden refrain) chứa flag lại không được in theo mặc định. Nhiệm vụ là tìm cách ép chương trình nhảy về đầu và in luôn đoạn ẩn này.

## Phân tích mã nguồn

1. **Đọc flag**

   ```python
   flag = open('flag.txt','r').read()
   secret_intro = (
     "Pico warriors rising, puzzles laid bare,\n"
     "Solving each challenge with precision and flair.\n"
     "With unity and skill, flags we deliver,\n"
     "The ether’s ours to conquer, " + flag + "\n"
   )
   ```

   Biến `secret_intro` chứa ngay dòng flag.

2. **Xây dựng lyrics**
   Toàn bộ lyrics được nối vào `song_flag_hunters = secret_intro + """…"""`, bao gồm:

   * Một block `[REFRAIN]` ẩn phía đầu (chứa lời mời “CROWD (Singalong here!);” và placeholder `RETURN`).
   * Label `[VERSE1]` rồi đến các verse và refrain tiếp theo.
   * Dòng `CROWD (Singalong here!);` sẽ kích hoạt prompt `Crowd:` trong phần refrain đầu.
   * Dòng `RETURN` là chỗ đánh dấu để sau này code sẽ ghi đè thành `RETURN <offset>`.

3. **Hàm `reader(song, '[VERSE1]')`**

   * Lần lượt quét tìm chỉ số của:

     * `startLabel = '[VERSE1]'` → `start = index + 1`
     * Mỗi lần gặp `song_lines[i] == '[REFRAIN]'` → cập nhật `refrain = i + 1`
     * Dòng placeholder `song_lines[i] == 'RETURN'` → lưu `refrain_return = i`
   * Khởi tạo con trỏ `lip = start` (bỏ qua phần intro và hidden refrain).
   * Với mỗi dòng:

     * Nếu gặp directive `REFRAIN` (tách từ dòng `REFRAIN;`), code sẽ:

       1. Ghi đè placeholder tại `refrain_return` thành `RETURN <lip+1>`
       2. Nhảy `lip = refrain` (vị trí của **cuối cùng** của `[REFRAIN]` label — do họ luôn cập nhật `refrain` thành lần cuối cùng)
     * Nếu gặp dòng match `CROWD.*`, nó sẽ prompt `Crowd: ` để bạn nhập text, và lưu lại tại chính vị trí đó trong `song_lines`.
     * Nếu gặp dòng match `RETURN [0-9]+`, nó sẽ nhảy `lip = <số>` — tức gọi “subroutine return” về chỉ số dòng tương ứng.
     * Các dòng còn lại sẽ được in rồi `lip += 1`.

**Điểm then chốt**:

* Vì `startLabel='[VERSE1]'`, chương trình **bỏ qua** toàn bộ `secret_intro` và block `[REFRAIN]` đầu (hidden refrain).
* Tuy nhiên khi chạy đến lần đầu gặp `REFRAIN;` trong verse, chương trình sẽ cập nhật placeholder `RETURN` thành `RETURN <offset>` dựa trên vị trí hiện tại.
* Nếu ta **chèn** thêm chuỗi `REFRAIN;RETURN 0` vào đúng chỗ prompt `Crowd: `, thì khi code split theo `;` sẽ thu được hai directive:

  1. `REFRAIN` → cập nhật placeholder theo lip+1 và nhảy vào block `[REFRAIN]` cuối (không in intro)
  2. `RETURN 0` → ngay lập tức nhảy con trỏ về chỉ số 0, tức in từ đầu danh sách `song_lines` — bao gồm cả `secret_intro` với flag.


## Các bước khai thác

1. **Kết nối tới service**

   ```bash
   $ nc verbal-sleep.picoctf.net 56688
   ```

2. **Chờ chương trình in xong phần verse cho đến khi xuất hiện prompt**

   ```
   Crowd:
   ```

   (Đây là prompt của lần đầu gặp `CROWD (Singalong here!);` trong hidden refrain — dù bạn không thấy refrain, prompt vẫn chờ input.)

3. **Nhập payload**

   ```
   REFRAIN;RETURN 0
   ```

   * Phần `REFRAIN` sẽ khiến chương trình thực thi subroutine của refrain (cập nhật placeholder).
   * Phần `RETURN 0` ngay lập tức bắt nó “return” về dòng 0.

4. **Nhận flag**
   Ngay sau đó, chương trình sẽ in lại từ dòng 0, gồm toàn bộ `secret_intro`:

   ```
   Pico warriors rising, puzzles laid bare,
   Solving each challenge with precision and flair.
   With unity and skill, flags we deliver,
   The ether’s ours to conquer, picoCTF{your_flag_here}
   ```

   — trong đó `picoCTF{…}` chính là flag mà bạn cần.


## Kết quả

* **Flag**: `picoCTF{…}` (xuất ra ngay trong `secret_intro`).
* **Phương pháp**: lợi dụng cơ chế subroutine-style (`REFRAIN` + `RETURN`) và chèn payload qua prompt `Crowd:` để ép chương trình quay về đầu và in phần ẩn.
