### Tổng lưu lượng nước ###

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
    