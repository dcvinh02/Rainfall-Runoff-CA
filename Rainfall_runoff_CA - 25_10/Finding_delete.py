### Xóa những hàng xóm không cần thiết ###
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
        NB = np.array([0, 1, 2, 3])
        ini = 0
    elif(direct_opt == 2):
        NB = np.array([0, 1, 2, 3, 4, 5, 6, 7])
    
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