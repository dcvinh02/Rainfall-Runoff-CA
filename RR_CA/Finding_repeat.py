"""Lọc giá trị tại một ô dựa trên giá trị trung bình của các ô lân cận có giá trị nhỏ hơn.

    Hàm này kiểm tra giá trị của một ô tại vị trí (i, j) trong mảng 2D `H_0_BC` so với giá trị của các ô lân cận.
    Nó lặp đi lặp lại quá trình tính toán giá trị trung bình của ô trung tâm và các ô lân cận có giá trị nhỏ hơn giá trị trung tâm hiện tại,
    cho đến khi không có sự thay đổi nào về số lượng ô lân cận có giá trị cao hơn hoặc bằng giá trị trung tâm.

    Args:
        H_0_BC (numpy.ndarray): Mảng 2D chứa các giá trị.
        i (int): Chỉ số hàng của ô trung tâm đang xét.
        j (int): Chỉ số cột của ô trung tâm đang xét.
        direct_opt (int): Một tùy chọn điều khiển việc xem xét các ô lân cận chéo.
                          Nếu `direct_opt` là 3 và không có ô lân cận trực tiếp nào có giá trị nhỏ hơn,
                          hoặc nếu `direct_opt` là 2, thì các ô lân cận chéo cũng sẽ được xem xét.

    Returns:
        tuple: Một tuple chứa ba giá trị:
            - AVE (float): Giá trị trung bình cuối cùng được tính toán.
            - n_neighbor (int): Số lượng ô lân cận có giá trị nhỏ hơn giá trị trung tâm trong lần lặp cuối cùng.
            - NB (list): Một danh sách các số nguyên, mỗi số đại diện cho vị trí tương đối của các ô lân cận có giá trị nhỏ hơn giá trị trung tâm.
                       Các số có thể tương ứng với: 1 (Bắc), 2 (Đông), 3 (Nam), 4 (Tây), 5 (Tây-Bắc), 6 (Đông-Bắc), 7 (Đông-Nam), 8 (Tây-Nam).
"""
""" how it works
1. Khởi tạo giá trị trung bình tạm thời (temp_AVE): Giá trị của ô trung tâm tại vị trí (i, j) trong mảng H_0_BC được gán cho biến temp_AVE. Đây sẽ là giá trị ban đầu để so sánh với các ô lân cận.

2. Lấy giá trị của các ô lân cận: Giá trị của 8 ô lân cận (Bắc, Đông, Nam, Tây, Đông-Bắc, Đông-Nam, Tây-Nam, Tây-Bắc) của ô trung tâm được lấy từ mảng H_0_BC và gán cho các biến tương ứng (H_N, H_E, H_S, H_W, H_NE, H_ES, H_SW, H_WN).

3. Khởi tạo các biến take_: Các biến take_NE, take_WN, take_SW, take_ES được khởi tạo bằng 0. Chúng có thể được sử dụng để đánh dấu việc có lấy giá trị của các ô lân cận chéo hay không.

4. Khởi tạo biến pre_n_Hi: Biến pre_n_Hi (previous number of higher or equal neighbors) được khởi tạo bằng 0. Biến này sẽ được sử dụng để kiểm tra điều kiện dừng của vòng lặp while.

5. Bắt đầu vòng lặp while True: Vòng lặp này sẽ tiếp tục chạy cho đến khi có một điều kiện break được đáp ứng.

6. Khởi tạo lại các biến trong mỗi lần lặp: Trong mỗi lần lặp, các biến n_neighbor (số lượng ô lân cận có giá trị nhỏ hơn temp_AVE), AVE (tổng giá trị của các ô lân cận nhỏ hơn temp_AVE), và n_Hi (số lượng ô lân cận có giá trị lớn hơn hoặc bằng temp_AVE) được đặt lại về 0.

7. Kiểm tra các ô lân cận trực tiếp (Bắc, Đông, Nam, Tây):

Đông (H_E): Nếu giá trị của ô phía Đông nhỏ hơn temp_AVE, n_neighbor tăng lên 1, giá trị của H_E được cộng vào AVE, và take_E được gán giá trị 2. Ngược lại, n_Hi tăng lên 1 và take_E được gán giá trị 0.
Bắc (H_N): Tương tự như ô phía Đông, nhưng take_N được gán giá trị 1.
Tây (H_W): Tương tự, take_W được gán giá trị 4.
Nam (H_S): Tương tự, take_S được gán giá trị 3.

8. Kiểm tra các ô lân cận chéo (nếu cần): Điều kiện ((direct_opt == 3) and (n_neighbor == 0)) or (direct_opt == 2) quyết định xem có kiểm tra các ô lân cận chéo hay không. Điều này xảy ra nếu direct_opt là 3 và không có ô lân cận trực tiếp nào nhỏ hơn temp_AVE, hoặc nếu direct_opt là 2.

Đông-Bắc (H_NE): Nếu nhỏ hơn temp_AVE, n_neighbor tăng, AVE cộng thêm H_NE, take_NE gán 6. Ngược lại, n_Hi tăng, take_NE gán 0.
Tây-Bắc (H_WN): Tương tự, take_WN gán 5.
Tây-Nam (H_SW): Tương tự, take_SW gán 8.
Đông-Nam (H_ES): Tương tự, take_ES gán 7.

9. Tính toán giá trị trung bình mới (AVE): Giá trị trung bình mới được tính bằng cách cộng tổng giá trị của các ô lân cận nhỏ hơn temp_AVE (đã tích lũy trong biến AVE) với giá trị của ô trung tâm (H_0_BC[i,j]), sau đó chia cho tổng số các ô này (số lượng ô lân cận nhỏ hơn + 1 ô trung tâm).

10. Kiểm tra điều kiện dừng: Nếu số lượng ô lân cận có giá trị lớn hơn hoặc bằng temp_AVE (n_Hi) không thay đổi so với lần lặp trước (pre_n_Hi), vòng lặp while sẽ bị dừng (break). Điều này có nghĩa là không còn sự thay đổi đáng kể nào trong việc xác định các ô lân cận nhỏ hơn.

11. Cập nhật temp_AVE và pre_n_Hi: Nếu điều kiện dừng chưa được đáp ứng, temp_AVE được cập nhật bằng giá trị trung bình mới (AVE), và pre_n_Hi được cập nhật bằng giá trị n_Hi của lần lặp hiện tại để chuẩn bị cho lần lặp tiếp theo.

12. Tạo danh sách các ô lân cận có giá trị nhỏ hơn (NB): Sau khi vòng lặp kết thúc, một danh sách NB được tạo ra, chứa các giá trị của các biến take_WN, take_N, take_NE, take_E, take_ES, take_S, take_SW, take_W. Các giá trị 0 (tức là các ô lân cận có giá trị lớn hơn hoặc bằng temp_AVE) sẽ bị loại bỏ khỏi danh sách này. Các số còn lại trong danh sách có thể đại diện cho vị trí tương đối của các ô lân cận có giá trị nhỏ hơn.

13. Trả về kết quả: Hàm trả về một tuple chứa giá trị trung bình cuối cùng (AVE), số lượng ô lân cận có giá trị nhỏ hơn (n_neighbor của lần lặp cuối cùng), và danh sách các vị trí tương đối của các ô lân cận này (NB).
"""
    
import numpy as np

def Finding_repeat(H_0_BC, i, j, direct_opt):
    temp_AVE = H_0_BC[i,j] # Initial neighbors
    H_N = H_0_BC[i-1, j] #North
    H_E = H_0_BC[i, j+1] #East
    H_S = H_0_BC[i+1, j] #South
    H_W = H_0_BC[i, j-1] #West
    H_NE = H_0_BC[i-1, j+1] #North East
    H_ES = H_0_BC[i+1, j+1] #East South
    H_SW = H_0_BC[i+1, j-1] #South West
    H_WN = H_0_BC[i-1, j-1] #West North
    
    take_NE = 0
    take_WN = 0
    take_SW = 0
    take_ES = 0
    
    pre_n_Hi = 0
    # Find neighbors and mask it
    while True:
        n_neighbor = 0
        AVE = 0
        n_Hi = 0
        if (H_E < temp_AVE):
            n_neighbor += 1
            AVE += H_E
            take_E = 2
        else:
            n_Hi = n_Hi + 1
            take_E = 0
        if (H_N < temp_AVE):
            n_neighbor += 1
            AVE += H_N
            take_N = 1
        else:
            n_Hi = n_Hi + 1
            take_N = 0
        if (H_W < temp_AVE):
            n_neighbor += 1
            AVE += H_W
            take_W = 4
        else:
            n_Hi = n_Hi + 1
            take_W = 0
        if (H_S < temp_AVE):
            n_neighbor += 1
            AVE += H_S
            take_S = 3
        else:
            n_Hi = n_Hi + 1
            take_S = 0
        
        if((direct_opt == 3) and (n_neighbor == 0)) or (direct_opt == 2):
        # Thuật toán (4+4N) hoặc thuật toán (8N) đều kiểm tra thêm các ô chéo
            if (H_NE < temp_AVE):
                n_neighbor += 1
                AVE += H_NE
                take_NE = 6
            else:
                n_Hi = n_Hi + 1
                take_NE = 0
            if (H_WN < temp_AVE):
                n_neighbor += 1
                AVE += H_WN
                take_WN = 5
            else: 
                n_Hi = n_Hi + 1
                take_WN = 0
            if (H_SW < temp_AVE):
                n_neighbor += 1
                AVE += H_SW
                take_SW = 8
            else:
                n_Hi = n_Hi + 1
                take_WN = 0
            if (H_ES < temp_AVE):
                n_neighbor += 1
                AVE += H_ES
                take_ES = 7
            else:
                n_Hi = n_Hi + 1
                take_ES = 0
                
        AVE = (AVE + H_0_BC[i,j]) / (n_neighbor + 1)
        if ((n_Hi - pre_n_Hi) == 0):
            break
        
        temp_AVE = AVE
        pre_n_Hi = n_Hi
    
    NB = [take_WN, take_N, take_NE, take_E, take_ES, take_S, take_SW, take_W]
    NB = [n for n in NB if n != 0]

    return AVE, n_neighbor, NB
                
            