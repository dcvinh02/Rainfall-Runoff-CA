### tính f_i, tổng lượng nước chảy sang từng hàng xóm ###
import numpy as np

def Flow_to_neighbor(H_0_BC, i, j, direct_opt, AVE, NB, dX, dt, n_man, h_0_BC, flag):
    H_NB = np.zeros(8)
    
    H_NB[0] = H_0_BC[i-1, j]
    H_NB[1] = H_0_BC[i, j+1]
    H_NB[2] = H_0_BC[i+1, j]
    H_NB[3] = H_0_BC[j, j-1]
    H_NB[4] = H_0_BC[i-1, j-1]
    H_NB[5] = H_0_BC[i-1, j+1]
    H_NB[6] = H_0_BC[i+1, j+1]
    H_NB[7] = H_0_BC[i+1, j-1]
    
    f_i = np.zeros(8)
    f_0 = 0
        
    for k in range (len(NB)):
        D = dX
        if (direct_opt != 1):
            if (NB[k] >= 5):
                D = np.sqrt(2) * dX
                
        s = (H_0_BC[i,j] - H_NB[NB[k]]) / D
        V = (h_0_BC[i,j]**(2/3) * s**0.5) / n_man
        T = D/V
        
        if (0.99*T <= dt):
            dt = dt*0.6
            flag = 1
            print(f'dt: {dt} <------- dt is changed')
            return f_i, f_0, dt, flag
    
    for k in range (len(NB)):
        f_i[NB[k]] = (AVE - H_NB[NB[k]])
    
    f_0 = np.sum(f_i)
    
    if (h_0_BC[i,j] < f_0):
        f_i[:] = f_i[:] * h_0_BC[i,j] / f_0
        #f_0 = h_0_BC[i,j]
    
    for k in range (len(NB)):
        f_i[NB[k]] = dt* f_i[NB[k]]/T    
        
    f_0 = np.sum(f_i)
    
    return f_i, f_0, dt, flag
    