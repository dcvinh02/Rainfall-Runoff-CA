### Lọc giá trị nhỏ hơn giá trị trung bình ###
import numpy as np

def Finding_repeat(H_0_BC, i, j, direct_opt):
    temp_AVE = H_0_BC[i,j]
    # Neighbors
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
                
            