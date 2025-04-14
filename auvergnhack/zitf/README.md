Đề bài: là cho một chuỗi, và 1 cái đèn để hiện các chữ (ảnh minh hoạ)
Để hiện các chữ, cần phải bật các bit tương ứng để hiện đúng chữ đó
=> Mã hoá chữ đó theo dạng bật/tắt các bit 

Theo như ảnh, ta có:

Chữ cái || bit 
A       || 0
B       || 1
C       || 2
D       || 3
E       || 4
F       || 5
G       || 6
H       || 7
I       || 8
J       || 9
K       || 10
L       || 11
M       || 12
N       || 13

ví dụ:
chữ Z: cần phải bật các bit: A, L, M, D <=> bật các bit 0, 11, 12, 3

Ta có: 
13 12 11 10 9 8 7 6 5 4 3 2 1 0
 0  1  1  0 0 0 0 0 0 0 1 0 0 1

=> Z có dạng mã hoá là : 01100000000001

Tương tự, ta có chữ I: cần phải bật các bit: A, I, J, D <=> bật các bit 0, 8, 9, 3
Ta có: 
13 12 11 10 9 8 7 6 5 4 3 2 1 0
 0  0  0  0 1 1 0 0 0 0 1 0 0 1

=> I có dạng mã hoá là: 00001100001001
