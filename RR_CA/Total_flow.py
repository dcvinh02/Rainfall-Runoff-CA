"""
    Cập nhật tổng lưu lượng nước tại một ô lưới và phân phối lưu lượng này đến các ô lân cận.

    Hàm này thực hiện phân phối lưu lượng nước từ ô trung tâm (i, j) đến 8 ô lân cận theo thứ tự
    [trên, phải, dưới, trái, trên-trái, trên-phải, dưới-phải, dưới-trái] dựa trên mảng `f_i`.
    Đồng thời, nó trừ lưu lượng tổng `f_0` khỏi ô trung tâm để đảm bảo bảo toàn nước.

    Parameters:
    -----------
    i : int
        Chỉ số hàng của ô hiện tại (ô trung tâm).
    j : int
        Chỉ số cột của ô hiện tại (ô trung tâm).
    f_i : list or array-like of float
        Mảng gồm 8 giá trị lưu lượng nước chảy đến từng ô lân cận theo thứ tự:
        [trên, phải, dưới, trái, trên-trái, trên-phải, dưới-phải, dưới-trái].
    f_0 : float
        Tổng lưu lượng nước rời khỏi ô trung tâm (i, j).
    F_BC : 2D numpy.ndarray
        Ma trận lưu lượng nước cho toàn bộ lưới, sẽ được cập nhật tại các vị trí tương ứng.

    Returns:
    --------
        Ma trận lưu lượng nước sau khi cập nhật phân phối tại ô (i, j).
    
    Ghi chú:
    --------
    Hàm không kiểm tra biên, vì vậy cần đảm bảo rằng ô (i, j) không nằm sát mép lưới để tránh lỗi chỉ số.
    """

def Total_flow(i, j, f_i, f_0, F_BC):
    F_BC[i, j] = F_BC[i, j] - f_0
    
    F_BC[i-1, j] = F_BC[i-1, j] + f_i[0]
    F_BC[i, j+1] = F_BC[i, j+1] + f_i[1]
    F_BC[i+1, j] = F_BC[i+1, j] + f_i[2]
    F_BC[i, j-1] = F_BC[i, j-1] + f_i[3]
    F_BC[i-1, j-1] = F_BC[i-1, j-1] + f_i[4]
    F_BC[i-1, j+1] = F_BC[i-1, j+1] + f_i[5]
    F_BC[i+1, j+1] = F_BC[i+1, j+1] + f_i[6]
    F_BC[i+1, j-1] = F_BC[i+1, j-1] + f_i[7]
    
    return F_BC
    