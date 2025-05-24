"""Lọc danh sách các ô lân cận dựa trên giá trị so với ô trung tâm.

    Hàm này xác định và loại bỏ các ô lân cận của một ô trung tâm tại vị trí (i, j) trong mảng `H_0_BC`
    dựa trên việc giá trị của chúng có nhỏ hơn giá trị của ô trung tâm hay không. Quá trình này được thực hiện
    lặp đi lặp lại cho đến khi không còn ô lân cận nào bị loại bỏ.

    Args:
        H_0_BC (numpy.ndarray): Mảng 2D chứa các giá trị.
        i (int): Chỉ số hàng của ô trung tâm đang xét.
        j (int): Chỉ số cột của ô trung tâm đang xét.
        direct_opt (int): Một tùy chọn điều khiển việc xem xét các loại ô lân cận ban đầu.
                          - Nếu là 1 hoặc 3, chỉ xem xét các ô lân cận trực tiếp (Bắc, Đông, Nam, Tây).
                          - Nếu là 2, xem xét tất cả 8 ô lân cận.

    Returns:
        tuple: Một tuple chứa ba giá trị:
            - AVE (float): Giá trị trung bình của ô trung tâm và các ô lân cận còn lại sau quá trình lọc.
            - n_neighbor (int): Số lượng ô lân cận còn lại sau quá trình lọc.
            - NB (list): Một danh sách chứa các chỉ số của các ô lân cận còn lại. Các chỉ số tương ứng với:
            0 (Bắc), 1 (Đông), 2 (Nam), 3 (Tây), 4 (Tây-Bắc), 5 (Đông-Bắc), 6 (Đông-Nam), 7 (Tây-Nam).
"""
"""
1. Khởi tạo:

temp_AVE được gán giá trị của ô trung tâm tại (i, j) từ mảng H_0_BC.
Mảng H_NB được tạo để lưu trữ giá trị của 8 ô lân cận của ô trung tâm.
Dựa vào giá trị của direct_opt:
	Nếu direct_opt là 1 hoặc 3, danh sách các chỉ số lân cận ban đầu NB chỉ bao gồm các ô lân cận trực tiếp (0, 1, 2, 3 tương ứng với Bắc, Đông, Nam, Tây). Biến ini được đặt thành 0.
	Nếu direct_opt là 2, NB bao gồm tất cả 8 ô lân cận (0 đến 7).
NB_temp là một bản sao của NB. Đây là danh sách sẽ được sửa đổi trong quá trình lọc.
n_pre_NB được khởi tạo bằng 0, dùng để theo dõi số lượng ô lân cận còn lại từ lần lặp trước.
2. Vòng lặp lọc (while True): Vòng lặp này tiếp tục cho đến khi không còn ô lân cận nào bị loại bỏ trong một lần lặp.

NB được đặt lại bằng bản sao hiện tại của NB_temp.
n_neighbor (số lượng ô lân cận thỏa mãn điều kiện) và AVE (tổng giá trị của các ô lân cận thỏa mãn điều kiện) được đặt lại về 0.
Duyệt qua các ô lân cận hiện có trong NB:
	Với mỗi chỉ số k trong NB, giá trị của ô lân cận tương ứng (H_NB[NB[k]]) được so sánh với temp_AVE.
	Nếu giá trị của ô lân cận nhỏ hơn temp_AVE:
		n_neighbor được tăng lên.
		Giá trị của ô lân cận được cộng vào AVE.
	Nếu giá trị của ô lân cận lớn hơn hoặc bằng temp_AVE:
		Ô lân cận có chỉ số NB[k] sẽ bị loại bỏ khỏi danh sách NB_temp.
Xử lý trường hợp đặc biệt cho direct_opt == 3: Nếu direct_opt là 3 và sau khi lọc, NB_temp trở thành rỗng, và nếu ini vẫn là 0, thì NB_temp sẽ được gán lại bằng danh sách các chỉ số của các ô lân cận chéo (4, 5, 6, 7), và ini được đặt thành 1. Điều này có thể là một cơ chế dự phòng để xem xét các ô chéo nếu không có ô trực tiếp nào thỏa mãn điều kiện.
Tính toán giá trị trung bình mới (AVE): Giá trị trung bình mới được tính bằng cách lấy tổng của AVE (tổng giá trị các ô lân cận thỏa mãn điều kiện) và giá trị của ô trung tâm (H_0_BC[i,j]), sau đó chia cho số lượng các ô này cộng với 1 (ô trung tâm).
Kiểm tra điều kiện dừng: Vòng lặp sẽ kết thúc (break) nếu số lượng ô lân cận trong NB_temp không thay đổi so với lần lặp trước (len(NB_temp) - n_pre_NB == 0).
3.Cập nhật và trả về:
temp_AVE được cập nhật bằng giá trị AVE mới tính toán.
n_pre_NB được cập nhật bằng số lượng ô lân cận hiện tại trong NB_temp.
Cuối cùng, hàm trả về giá trị trung bình AVE, số lượng ô lân cận còn lại n_neighbor, và danh sách các chỉ số của các ô lân cận còn lại NB (thực chất là NB_temp).
"""
import numpy as np

def Finding_delete(H_0_BC, i, j, direct_opt):
    temp_AVE = H_0_BC[i,j] # Initial neightbor
    H_NB = np.zeros(8)
    H_NB[0] = H_0_BC[i-1, j] # Neighbor i-1, j
    H_NB[1] = H_0_BC[i, j+1] # Neighbor i, j+1
    H_NB[2] = H_0_BC[i+1, j] # Neighbor i+1, j
    H_NB[3] = H_0_BC[i, j-1] # Neighbor i, j-1
    H_NB[4] = H_0_BC[i-1, j-1] # Neighbor i-1, j-1
    H_NB[5] = H_0_BC[i-1, j+1] # Neighbor i-1, j+1
    H_NB[6] = H_0_BC[i+1, j+1] # Neighbor i+1, j+1
    H_NB[7] = H_0_BC[i+1, j-1] # Neighbor i+1, j-1
    # Neighbors condition
    if(direct_opt == 1) or (direct_opt == 3):
        NB = [0, 1, 2, 3]
        ini = 0
    elif(direct_opt == 2):
        NB = [0, 1, 2, 3, 4, 5, 6, 7]
    
    NB_temp = NB.copy()
    n_pre_NB = 0
    # Delete neightbors that do not satisfy the condition
    while True:
        NB = NB_temp.copy()
        n_neighbor = 0
        AVE = 0
        for k in range (len(NB)):
            if(H_NB[NB[k]] < temp_AVE):
                n_neighbor += 1
                AVE += H_NB[NB[k]]
            else:
                NB_temp = [n for n in NB_temp if n != NB[k]]
                #NB_temp = NB_temp.remove(NB[k])
        
        if ((direct_opt == 3) and (len(NB_temp) == 0)):
            if (ini == 0):
                NB_temp = [4, 5, 6, 7]
            ini = 1
        AVE = (AVE + H_0_BC[i,j]) / (n_neighbor + 1)
        
        if((len(NB_temp) - n_pre_NB) == 0):
            break
    
        temp_AVE = AVE
        n_pre_NB = len(NB_temp)
    
    return AVE, n_neighbor, NB