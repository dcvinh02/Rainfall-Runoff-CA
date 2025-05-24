"""
Đoạn mã này tạo ra một mặt nghiêng 2D trong không gian 3D bằng cách xoay một mặt phẳng ban đầu.
Sau đó, nó tính toán tọa độ trung tâm của các ô lưới trên mặt nghiêng này và lưu các thông tin liên quan
cùng với một mảng dữ liệu khác (Ri) vào các tệp DAT riêng biệt.

Các bước thực hiện chính:

1. **Thiết lập môi trường và tham số:**
   - Đóng tất cả các hình vẽ matplotlib hiện có.
   - Định nghĩa kích thước vật lý của vùng mô phỏng (`X_size`, `Y_size`).
   - Định nghĩa số lượng ô lưới theo hướng X và Y (`m`, `n`).
   - Tính toán kích thước của mỗi ô lưới (`dX`, `dY`).

2. **Tạo mặt phẳng cơ sở:**
   - Sử dụng `np.meshgrid` để tạo ma trận tọa độ X và Y cho một mặt phẳng 2D.
   - Khởi tạo ma trận tọa độ Z với các giá trị bằng 0, tạo thành một mặt phẳng nằm ngang.

3. **Tạo mặt nghiêng bằng phép xoay:**
   - Xác định độ dốc mong muốn theo phần trăm (`slope_percent`).
   - Tính toán góc nghiêng theo radian dựa trên phần trăm độ dốc.
   - Tạo một ma trận tọa độ XYZ bằng cách xếp chồng các mảng X, Y, Z.
   - Tạo một ma trận xoay để xoay mặt phẳng quanh trục X một góc bằng với góc nghiêng đã tính.
   - Thực hiện phép nhân ma trận để xoay các tọa độ XYZ, kết quả được lưu trong `xyz`.
   - Trích xuất các tọa độ x, y, z đã xoay và định hình lại chúng về kích thước lưới ban đầu.
   - Sao chép mảng z vào biến `geo_slope` để lưu trữ thông tin về độ cao của mặt nghiêng.

4. **Trực quan hóa mặt phẳng và mặt nghiêng:**
   - Vẽ mặt phẳng ban đầu (chưa xoay) bằng cách sử dụng `plt.plot` để hiển thị các đường lưới.
   - Vẽ mặt nghiêng 3D đã xoay bằng cách sử dụng `plt.plot_surface` trong một đối tượng `Axes3D`.

5. **Tính toán tọa độ trung tâm của các ô lưới:**
   - Khởi tạo các mảng để lưu trữ tọa độ trung tâm của các ô theo hướng X (`X_cell`) và Y (`Y_cell`),
     cũng như giá trị độ dốc trung bình của mỗi ô (`geo_slope_cell`).
   - Tính toán tọa độ x trung bình của mỗi ô bằng cách lấy trung bình tọa độ x của hai điểm cuối theo chiều ngang.
   - Tính toán tọa độ y trung bình của mỗi ô bằng cách lấy trung bình tọa độ y của hai điểm cuối theo chiều dọc.
   - Tính toán giá trị `geo_slope` trung bình cho mỗi ô bằng cách lấy trung bình giá trị `geo_slope` của bốn góc của ô đó.

6. **Tính toán tọa độ trung tâm (đã xoay) của các ô lưới:**
   - Khởi tạo các mảng để lưu trữ tọa độ x (`x_cell`) và y (`y_cell`) trung tâm của các ô sau khi xoay.
   - Tính toán tọa độ x trung bình của mỗi ô sau khi xoay.
   - Tính toán tọa độ y trung bình của mỗi ô sau khi xoay.
   - Gán giá trị `geo_slope_cell` cho `z_cell`, giả định rằng `geo_slope_cell` đại diện cho giá trị z tại trung tâm của mỗi ô.

7. **Lưu dữ liệu vào tệp:**
   - Lưu mảng `X_cell` vào tệp "X_cell.dat" với định dạng số thực có 6 chữ số sau dấu thập phân.
   - Lưu mảng `Y_cell` vào tệp "Y_cell.dat" với định dạng tương tự.
   - Lưu mảng `geo_slope_cell` vào tệp "geo_slope_cell.dat" với định dạng tương tự.

8. **Tạo và lưu dữ liệu Ri:**
   - Tạo một mảng `Ri` có cùng kích thước với lưới và điền tất cả các phần tử bằng giá trị 0.1 (đơn vị m/h).
   - Lưu mảng `Ri` vào tệp "Ri.dat" với định dạng tương tự.

9. **Lưu dữ liệu độ dốc (geo_slope):**
   - Lưu mảng `geo_slope` (giá trị z của các điểm trên lưới) vào tệp "geo_slope.dat" với định dạng tương tự.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

for i in plt.get_fignums():
    plt.close(i)

# Thống nhất các tham số và tạo mặt nghiêng
X_size = 100
Y_size = 500
m = 100  # số lượng ô theo hướng X
n = 500  # số lượng ô theo hướng Y
dX = X_size / m
dY = Y_size / n

# Tạo mặt phẳng dữ liệu X, Y
X, Y = np.meshgrid(np.arange(0, X_size + dX, dX), np.arange(0, Y_size + dY, dY))

# Tạo mặt nghiêng Z
Z_size = 0
slope_percent = 5  # phần trăm độ dốc
slope = np.arcsin(slope_percent / 100) * 180 / np.pi
Z = np.zeros_like(X)

# Tạo ma trận tọa độ XYZ và xoay để tạo mặt nghiêng
XYZ = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))
rotation_matrix = np.array([[1, 0, 0],
                            [0, np.cos(-np.radians(slope)), -np.sin(-np.radians(slope))],
                            [0, np.sin(-np.radians(slope)), np.cos(-np.radians(slope))]])
xyz = XYZ @ rotation_matrix.T

x = xyz[:, 0].reshape(X.shape)
y = xyz[:, 1].reshape(Y.shape)
z = xyz[:, 2].reshape(Z.shape) + Z_size  # dịch chuyển lên theo Z_size
geo_slope = z.copy()

# Vẽ mặt phẳng (mặt nghiêng chưa xoay)
plt.figure(figsize=(16, 12))
plt.plot(X, Y, 'b')
plt.plot(X.T, Y.T, 'b')
plt.axis('equal')
plt.xlabel('X')
plt.ylabel('Y')
plt.title("Mặt phẳng trước khi xoay")
plt.show()

# Vẽ mặt nghiêng 3D sau khi xoay
fig = plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='viridis', edgecolor='k')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title("Mặt nghiêng sau khi xoay")
ax.view_init(elev=25, azim=45)
plt.show()

# Lưu tọa độ các điểm giữa các ô
X_cell = np.zeros((n, m))
Y_cell = np.zeros((n, m))
geo_slope_cell = np.zeros((n, m))

for i in range(m):
    X_cell[:, i] = (X[:-1, i] + X[:-1, i + 1]) / 2

for j in range(n):
    Y_cell[j, :] = (Y[j, :-1] + Y[j + 1, :-1]) / 2

for i in range(n):
    for j in range(m):
        geo_slope_cell[i, j] = (geo_slope[i, j] + geo_slope[i + 1, j] +
                                geo_slope[i, j + 1] + geo_slope[i + 1, j + 1]) / 4

# Tính toán các tọa độ x, y, z cho các cell
x_cell = np.zeros((n, m))
y_cell = np.zeros((n, m))

for i in range(m):
    x_cell[:, i] = (x[:-1, i] + x[:-1, i + 1]) / 2

for i in range(n):
    for j in range(m):
        y_cell[i, j] = (y[i, j] + y[i + 1, j] +
                        y[i, j + 1] + y[i + 1, j + 1]) / 4

z_cell = geo_slope_cell

# Lưu dữ liệu
np.savetxt("X_cell.dat", X_cell, fmt="%.6f")
np.savetxt("Y_cell.dat", Y_cell, fmt="%.6f")
np.savetxt("geo_slope_cell.dat", geo_slope_cell, fmt="%.6f")

# Tạo dữ liệu Ri và lưu lại
Ri = np.full((n, m), 0.1)  # m/h
np.savetxt("Ri.dat", Ri, fmt="%.6f")

# Lưu geo_slope để sử dụng nếu cần
np.savetxt("geo_slope.dat", geo_slope, fmt="%.6f")