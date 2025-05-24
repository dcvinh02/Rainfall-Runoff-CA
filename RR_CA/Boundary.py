"""Thiết lập các điều kiện biên cho mảng độ cao và mảng Ri.

    Hàm này tạo ra các mảng mới lớn hơn mảng đầu vào 2 hàng và 2 cột ở mỗi chiều,
    và thiết lập các điều kiện biên xung quanh mảng độ cao. Điều kiện biên bao gồm
    các "bức tường" ở các cạnh và một "cổng thoát nước" ở phía trên của mô hình.

    Args:
        heights_cell (numpy.ndarray): Mảng 2D chứa giá trị độ cao của các ô bên trong mô hình.
        Ri (numpy.ndarray): Mảng 2D chứa giá trị Ri (có thể là hệ số thấm hoặc một thuộc tính tương tự)
                            của các ô bên trong mô hình.
        wall (float): Giá trị độ cao cộng thêm vào các ô biên để mô phỏng bức tường.
        gate (float): Một giá trị từ 0 đến 1 biểu thị tỷ lệ chiều rộng của cổng thoát nước so với
                      chiều rộng của mô hình (số cột).
        delta_H_out (float): Giá trị độ cao bị trừ đi tại cổng thoát nước để tạo sự chênh lệch độ cao cho dòng chảy.

    Returns:
        tuple: Một tuple chứa hai mảng NumPy:
            - H_BC (numpy.ndarray): Mảng 2D mới chứa giá trị độ cao với các điều kiện biên đã được thiết lập.
                                     Kích thước của mảng này là (rows+2, cols+2), trong đó rows và cols
                                     là số hàng và số cột của `heights_cell`.
            - Ri_BC (numpy.ndarray): Mảng 2D mới chứa giá trị Ri với các giá trị từ mảng `Ri` được đặt
                                     ở phần bên trong. Kích thước của mảng này cũng là (rows+2, cols+2).
"""
"""
1. Xác định kích thước:

Lấy số hàng (rows) và số cột (cols) từ mảng heights_cell.

2. Khởi tạo mảng biên:

Tạo hai mảng NumPy mới là Ri_BC và H_BC với kích thước lớn hơn heights_cell và Ri hai đơn vị ở mỗi chiều.

Điều này tạo ra một lớp biên bao quanh dữ liệu bên trong.

Cả hai mảng được khởi tạo với các giá trị bằng 0.

3. Đặt giá trị bên trong:

Sao chép dữ liệu từ mảng Ri vào phần bên trong của Ri_BC (từ hàng 1 đến rows và cột 1 đến cols).

Tương tự, sao chép dữ liệu từ heights_cell vào phần bên trong của H_BC.

4. Thiết lập biên dạng tường:

Góc:

Đặt giá trị của bốn góc của H_BC bằng giá trị của các ô góc tương ứng trong heights_cell cộng với giá trị wall.

Điều này tạo ra các "góc tường".

Cạnh:

Đặt giá trị của các ô trên bốn cạnh của H_BC (trừ các góc) bằng giá trị của các ô tương ứng ở cạnh của heights_cell cộng với wall.

Cụ thể:

Cạnh trái (H_BC[1:rows+1, 0]): Dựa trên cột đầu tiên của heights_cell.

Cạnh phải (H_BC[1:rows+1, cols+1]): Dựa trên cột cuối cùng của heights_cell.

Cạnh trên (H_BC[0, 1:cols+1]): Dựa trên hàng đầu tiên của heights_cell.

Cạnh dưới (H_BC[rows+1, 1:cols+1]): Dựa trên hàng cuối cùng của heights_cell.

5. Tạo cổng thoát nước (Out gate):

Tính toán chiều rộng của cổng thoát nước (out) dựa trên tổng số cột (cols) và tỷ lệ gate.

Xác định cột trung tâm (fix_col) và nửa chiều rộng của cổng (fix_out).

Lấy một phần của hàng đầu tiên trong heights_cell tương ứng với vị trí và chiều rộng của cổng.

Giảm giá trị độ cao trong phần này đi một lượng delta_H_out để tạo ra sự chênh lệch độ cao, cho phép dòng chảy thoát ra.

Gán các giá trị độ cao đã điều chỉnh này cho các ô tương ứng trên cạnh trên của mảng H_BC.

6. Trả về kết quả:

Hàm trả về hai mảng:

H_BC chứa độ cao với các điều kiện biên đã được thiết lập.

Ri_BC chứa giá trị Ri với dữ liệu bên trong được sao chép.
"""
import numpy as np

def Boudary_conditions(heights_cell, Ri, wall, gate, delta_H_out):
    rows, cols = heights_cell.shape
    # số hàng và số cột của dữ liệu
    
    Ri_BC = np.zeros((rows+2, cols+2))
    H_BC = np.zeros((rows+2, cols+2))
    # khởi tạo ma trận rỗng với kích thước rows+2 và cols+2, công 2 giá trị biên
    # -> giả lập biên xung quanh lưới
    
    Ri_BC[1:rows+1, 1:cols+1] = Ri[:,:] # Ri inside
    H_BC[1:rows+1, 1:cols+1] = heights_cell[:,:] # height inside
    
    # Configuration boundary
    H_BC[0, 0] = heights_cell[0, 0] + wall #left lower corner
    H_BC[0, cols+1] = heights_cell[0, cols-1] + wall #right lower corner
    H_BC[rows+1, 0] = heights_cell[rows-1, 0] + wall #left upper corner
    H_BC[rows+1, cols+1] = heights_cell[rows-1, cols-1] + wall #right upper corner
    
    H_BC[1:rows+1, 0] = heights_cell[:, 0] + wall #left side
    H_BC[1:rows+1, cols+1] = heights_cell[:, cols-1] + wall #right side
    H_BC[0, 1:cols+1] = heights_cell[0, :] + wall #upper side
    H_BC[rows+1, 1:cols+1] = heights_cell[rows-1, :] + wall #lower side   
    
    # Out gate
    out = int(cols*gate)
    #Heights = heights_cell[0 , (round(cols/2)-round(out/2))+1:(round(cols/2)+round(out/2)+1)] - delta_H_out
    #H_BC[0, (1+(round(cols/2)-round(out/2))):((round(cols/2)+round(out/2)))] = Heights
    fix_col = int(cols/2)
    fix_out = int(out/2)
    Height = heights_cell[0, (fix_col - fix_out)+1 : (fix_col + fix_out)] - delta_H_out
    H_BC[0, (1+(fix_col - fix_out)+1) : (fix_col + fix_out)+1] = Height
    
    return H_BC, Ri_BC