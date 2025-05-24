"""Tính toán lượng dòng chảy từ một ô trung tâm đến các ô lân cận.

    Hàm này tính toán lưu lượng dòng chảy từ ô lưới tại vị trí (i, j) đến các ô lân cận dựa trên sự khác biệt về cao độ,
    kích thước ô, hệ số Manning và bước thời gian. Nó cũng điều chỉnh bước thời gian nếu cần để đảm bảo tính ổn định.

    Args:
        H_0_BC (numpy.ndarray): Mảng 2D chứa giá trị cao độ (hoặc một thuộc tính tương tự) tại các ô,
                                  bao gồm cả các ô biên.
        i (int): Chỉ số hàng của ô trung tâm đang xét.
        j (int): Chỉ số cột của ô trung tâm đang xét.
        direct_opt (int): Một tùy chọn điều khiển cách tính khoảng cách đến các ô lân cận.
                          Nếu khác 1, khoảng cách đến các ô lân cận chéo sẽ là sqrt(2) * dX.
        AVE (float): Giá trị trung bình hoặc một giá trị tham chiếu khác được sử dụng để tính toán lưu lượng.
                     Ý nghĩa cụ thể của tham số này cần được làm rõ trong bối cảnh sử dụng hàm.
        NB (list): Một danh sách các chỉ số (từ 0 đến 7) xác định thứ tự của các ô lân cận được xem xét.
                   Các chỉ số tương ứng với: 0 (trên), 1 (phải), 2 (dưới), 3 (trái), 4 (trên-trái), 5 (trên-phải), 6 (dưới-phải), 7 (dưới-trái).
        dX (float): Kích thước của một ô trong lưới theo cả chiều ngang và chiều dọc.
        dt (float): Bước thời gian hiện tại. Giá trị này có thể được điều chỉnh bởi hàm.
        n_man (float): Hệ số Manning, đại diện cho độ nhám bề mặt.
        h_0_BC (numpy.ndarray): Một mảng 2D chứa độ sâu dòng chảy (hoặc một biến số liên quan khác) tại các ô,
                                  bao gồm cả các ô biên.
        flag (int): Một cờ trạng thái. Nó sẽ được đặt thành 1 nếu bước thời gian được điều chỉnh.

    Returns:
        tuple: Một tuple chứa bốn giá trị:
            - f_i (numpy.ndarray): Mảng 1D kích thước 8 chứa lưu lượng dòng chảy đến từng ô lân cận tương ứng.
            - f_0 (float): Tổng lưu lượng dòng chảy ra khỏi ô trung tâm.
            - dt (float): Bước thời gian đã được điều chỉnh (nếu cần).
            - flag (int): Cờ trạng thái, sẽ là 1 nếu bước thời gian đã được thay đổi, và giữ nguyên giá trị ban đầu nếu không.
"""
import numpy as np

def Flow_to_neighbor(H_0_BC, i, j, direct_opt, AVE, NB, dX, dt, n_man, h_0_BC, flag):
    H_NB = np.zeros(8) # Initial neighbors
    H_NB[0] = H_0_BC[i-1, j]
    H_NB[1] = H_0_BC[i, j+1]
    H_NB[2] = H_0_BC[i+1, j]
    H_NB[3] = H_0_BC[i, j-1]
    H_NB[4] = H_0_BC[i-1, j-1]
    H_NB[5] = H_0_BC[i-1, j+1]
    H_NB[6] = H_0_BC[i+1, j+1]
    H_NB[7] = H_0_BC[i+1, j-1]
    
    f_i = np.zeros(8)
    f_0 = 0
    # Flow calculator
    for k in range (len(NB)):
        D = dX
        if (direct_opt != 1):
            if (NB[k] >= 5):
                D = np.sqrt(2) * dX
        # Flow index
        s = (H_0_BC[i,j] - H_NB[NB[k]]) / D
        V = (h_0_BC[i,j]**(2/3) * s**0.5) / n_man
        T = D/V
        # If the condition dt>T is satisfied
        if (0.99*T <= dt):
            dt = dt*0.6
            flag = 1
            print(f'dt: {dt} <------- dt is changed')
            return f_i, f_0, dt, flag
    # Neighbors total flow
    for k in range (len(NB)):
        f_i[NB[k]] = (AVE - H_NB[NB[k]])
    # Central total flow
    f_0 = np.sum(f_i)
    # Case the outflow is greater than the available flow
    if (h_0_BC[i,j] < f_0):
        f_i[:] = f_i[:] * h_0_BC[i,j] / f_0
        #f_0 = h_0_BC[i,j]
    # Balance flow
    for k in range (len(NB)):
        f_i[NB[k]] = dt* f_i[NB[k]]/T    
        
    f_0 = np.sum(f_i) # Total outflow
    
    return f_i, f_0, dt, flag
    