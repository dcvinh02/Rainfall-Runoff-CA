### Thiết lập điều kiện biên cho mô hình ###
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
    out = round(cols*gate)
    #Heights = heights_cell[0 , (round(cols/2)-round(out/2))+1:(round(cols/2)+round(out/2)+1)] - delta_H_out
    #H_BC[0, (1+(round(cols/2)-round(out/2))):((round(cols/2)+round(out/2)))] = Heights
    fix_col = round(cols/2)
    fix_out = round(out/2)
    H_BC[0, (1+(fix_col - fix_out)+1) : (fix_col + fix_out)+1] = heights_cell[0, (fix_col - fix_out)+1 : (fix_col + fix_out)] - delta_H_out
    
    return H_BC, Ri_BC