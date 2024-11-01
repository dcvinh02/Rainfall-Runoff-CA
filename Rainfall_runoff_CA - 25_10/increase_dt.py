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
    
    if (Tmin > 10*dt):
        dt = dt*2
        flag = 1
        print(f'dt: {dt} <------ dt is changed')
        return dt, flag
    
    return dt, flag