"""Tính toán thời gian di chuyển tối thiểu và điều chỉnh bước thời gian (dt) nếu cần.

    Hàm này duyệt qua một lưới 2D và tính toán thời gian di chuyển từ mỗi ô trung tâm đến các ô lân cận của nó.
    Thời gian di chuyển tối thiểu được xác định và nếu nó lớn hơn một ngưỡng nhất định (10 lần bước thời gian hiện tại),
    bước thời gian sẽ được tăng gấp đôi và một cờ (flag) sẽ được đặt để báo hiệu sự thay đổi này.

    Args:
        H_0_BC (numpy.ndarray): Mảng 2D chứa giá trị tại các ô, có thể đại diện cho độ cao hoặc một thuộc tính tương tự.
                                  Kích thước dự kiến là (n+2, m+2) để xử lý các ô biên.
        n (int): Số lượng hàng trong vùng tính toán (không bao gồm các hàng biên).
        m (int): Số lượng cột trong vùng tính toán (không bao gồm các cột biên).
        direct_opt (int): Một tùy chọn điều khiển cách tính khoảng cách đến các ô lân cận.
                          Nếu khác 1, khoảng cách đến các ô lân cận chéo sẽ là sqrt(2) * dX.
        NB (list): Một danh sách các chỉ số (từ 0 đến 7) xác định thứ tự của các ô lân cận được xem xét.
                   Các chỉ số tương ứng với: 0 (trên), 1 (phải), 2 (dưới), 3 (trái), 4 (trên-trái), 5 (trên-phải), 6 (dưới-phải), 7 (dưới-trái).
        dX (float): Kích thước của một ô trong lưới theo cả chiều ngang và chiều dọc.
        dt (float): Bước thời gian hiện tại. Giá trị này có thể được điều chỉnh bởi hàm.
        n_man (float): Hệ số Manning, đại diện cho độ nhám bề mặt.
        h_0_BC (numpy.ndarray): Một mảng 2D khác chứa độ sâu dòng chảy hoặc một biến số liên quan khác tại các ô.
                                  Kích thước dự kiến là (n+2, m+2).
        flag (int): Một cờ trạng thái. Nó sẽ được đặt thành 1 nếu bước thời gian được điều chỉnh.

    Returns:
        tuple: Một tuple chứa hai giá trị:
            - dt (float): Bước thời gian đã được điều chỉnh (nếu cần).
            - flag (int): Cờ trạng thái, sẽ là 1 nếu bước thời gian đã được thay đổi, và giữ nguyên giá trị ban đầu nếu không.
"""

import numpy as np

def increase(H_0_BC, n, m, direct_opt, NB, dX, dt, n_man, h_0_BC, flag):
    Tmin = 1000;
    H_NB = np.zeros(8)
    rows = n
    cols = m
    for i in range (1, (rows+1)):
        for j in range (1, (cols+1)):
            H_NB[0] = H_0_BC[i-1, j]
            H_NB[1] = H_0_BC[i, j+1]
            H_NB[2] = H_0_BC[i+1, j]
            H_NB[3] = H_0_BC[i, j-1]
            H_NB[4] = H_0_BC[i-1, j-1]
            H_NB[5] = H_0_BC[i-1, j+1]
            H_NB[6] = H_0_BC[i+1, j+1]
            H_NB[7] = H_0_BC[i+1, j-1]
            
            # Flow from central to neighbor
            for k in range (len(NB)):
                D = dX
                if (direct_opt != 1):
                    if (NB[k] >= 5):
                        D =  np.sqrt(2)*dX
                
                s = (H_0_BC[i,j] - H_NB[NB[k]]) / D
                V = (h_0_BC[i,j]**(2/3) * s**0.5) / n_man
                T = D/V
                
                if (Tmin > T):
                    Tmin = T
                    
    # Readjust timestep
    if (Tmin > 10*dt):
        dt = dt*2
        flag = 1
        print(f'dt: {dt} <------ dt is changed')
        return dt, flag
    
    return dt, flag