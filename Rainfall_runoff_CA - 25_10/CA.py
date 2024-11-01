import numpy as np
import Boundary
#import Finding_repeat as fr
import Finding_delete as fd
import Flow_to_neighbor as fl
import Total_flow as tf
import matplotlib.pyplot as plt
import increase_dt as inc
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d

plt.close('all')

# Geometry input
X_cell = np.loadtxt('E:\K65 - CN10 - FAT _UET _VNU\Project Cellular Automata - Rainfall Runoff\Code\Python\Rainfall_runoff_CA\X_cell.dat')
X_cell = X_cell * 1000 # đổi đơn vị từ m sang mm
Y_cell = np.loadtxt('E:\K65 - CN10 - FAT _UET _VNU\Project Cellular Automata - Rainfall Runoff\Code\Python\Rainfall_runoff_CA\Y_cell.dat')
Y_cell = Y_cell * 1000

geo_slope_cell = np.loadtxt('E:\K65 - CN10 - FAT _UET _VNU\Project Cellular Automata - Rainfall Runoff\Code\Python\Rainfall_runoff_CA\geo_slope_cell.dat')
#geo_slope_cell = np.loadtxt('E:\DEM\Bacninh_100x100.dat')

n = X_cell.shape[0]
m = X_cell.shape[1] 

Ri = np.loadtxt('E:\K65 - CN10 - FAT _UET _VNU\Project Cellular Automata - Rainfall Runoff\Code\Python\Rainfall_runoff_CA\Ri.dat')
Ri = (Ri) * 1000/3600 # đổi m/h sang mm/s

# Khởi tạo giá trị biến
n_man = 0.01 * (1000 ** (-1/3)) # m -> mm
H = geo_slope_cell * 1000 # m -> mm
wall = 500
gate = 1
delta_H_out = 50
dt = 10
direct_opt = 3
T = 40 * 60 # Time simulator, h
rain_time = 10 * 60
# Biến kích thước
dX = (X_cell[0,1] - X_cell[0,0])
dY = (Y_cell[1,0] - X_cell[1,0])

P_BC = np.zeros((n+2, m+2), dtype=np.float32)
infil_t = 20/3600
Re_BC = np.zeros((n+2, m+2), dtype=np.float32)
Rcum_BC = np.zeros((n+2, m+2), dtype=np.float32)
#Pcum_BC = np.zeros((n+2, m+2))
#del_P_BC = np.zeros((n+2, m+2))
H_0_BC = np.zeros((n+2, m+2), dtype=np.float32)
h_0_BC = np.zeros((n+2, m+2), dtype=np.float32)
h_0_BC_pre = np.zeros((n+2, m+2), dtype=np.float32)
F_BC = np.zeros((n+2, m+2), dtype=np.float32)

H_BC, Ri_BC = Boundary.Boudary_conditions(H, Ri, wall, gate, delta_H_out)
t_pre = 0
t = []
it = 1
# Khởi tạo biến mô phỏng 3d
fig = plt.figure()
#axes = plt.axes(projection="3d")
plt.ion()
x_data = np.zeros((n,m))
y_data = np.zeros((n,m))
z_data = np.zeros((n,m))

with open('output','w+') as fileID:
    fileID.write(f"{'t(min)' :>6} {'runoff_rate(mm/h)' :>12}\n")

    runoff_rate = []
    while (t_pre < T):
        print(f"iteration: {it}")
        #t.append(t_pre + dt)
        t_current = t_pre + dt
        F_BC.fill(0)
        flag = 0
        #if (t[it-1] > rain_time):
        if (t_current > rain_time):
            Ri_BC.fill(0)
        for i in range(1, n+1):
            for j in range(1, m+1):
                # Calculate effective rainfall
                I = infil_t * dt
                if I < (h_0_BC_pre[i, j] + Ri_BC[i, j] * dt):
                    Re_BC[i, j] = Ri_BC[i, j] * dt - infil_t * dt
                else:
                    Re_BC[i, j] = Ri_BC[i, j] * dt - h_0_BC_pre[i, j]

        # Updating cell states
        h_0_BC = Re_BC + h_0_BC_pre
        H_0_BC = H_BC + h_0_BC
        z_data[:,:] = H_0_BC[1:-1, 1:-1]
        for i in range(1, n):
            for j in range(1, m):
                AVE, n_neighbor, NB = fd.Finding_delete(H_0_BC, i, j, direct_opt)
                f_i, f_0, dt, flag = fl.Flow_to_neighbor(H_0_BC, i, j, direct_opt, AVE, NB, dX, dt, n_man, h_0_BC, flag)
                if flag: 
                    break
                F_BC = tf.Total_flow(i, j, f_i, f_0, F_BC)
                x_data[i, j] = i 
                y_data[i, j] = j

            if flag: 
                break
    
        #axes.clear()
        #axes.plot_surface(x_data, y_data, z_data, cmap = "plasma")
        #plt.pause(0.1)
                
        dt, flag = inc.increase(H_0_BC, n, m, direct_opt, NB, dX, dt, n_man, h_0_BC, flag)
        if flag: 
            continue

        h_0_BC[1:n+1, 1:m+1] += F_BC[1:n+1, 1:m+1]
        h_0_BC_pre = np.copy(h_0_BC)

        Q = np.sum(F_BC[0, 1:m+1]) * dY * dX
        #runoff_rate = Q * 3600 / ((dX * m * dY * n) * dt)
        current_runoff_rate = Q * 3600 / ((dX * m * dY * n) * dt)
        runoff_rate.append(current_runoff_rate)
        #print(f"time {t[it-1]/60:.2f}(min) - runoff_rate {runoff_rate:.2f} (mm/h)")
        print(f"time {t_current /60:.2f}(min) - runoff_rate {current_runoff_rate:.2f} (mm/h)")
        plt.figure(1)
        #plt.plot(t[it-1]/60, runoff_rate, 'r*')
        plt.plot(t_current / 60, current_runoff_rate, 'r*')
        plt.xlabel('Time (min)')
        plt.ylabel('Runoff rate (mm/h)')
        #fileID.write(f"{t[it-1]/60:6.2f} {runoff_rate:12.8f}\n")
        fileID.write(f"{t_current / 60:6.2f} {current_runoff_rate:12.8f}\n")
        t_pre = t_current
        #t_pre = t[it-1]
        it += 1
        plt.savefig('E:/final_runoff_rate_plot2.png', dpi=300)
        plt.show()
        plt.pause(0.1)
X, Y = np.meshgrid(X_cell, Y_cell)
Z = H_0_BC[1:-1, 1:-1]   # Sử dụng giá trị của H_0_BC hoặc runoff_rate

'''# Tạo đồ thị 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Sử dụng plot_surface để vẽ mô hình 3D
surf = ax.plot_surface(X, Y, Z[1:-1, 1:-1], cmap='viridis')

# Thêm thanh màu để biểu diễn giá trị
fig.colorbar(surf)

# Thêm nhãn cho các trục
ax.set_xlabel('X axis (m)')
ax.set_ylabel('Y axis (m)')
ax.set_zlabel('Z axis (mm)')

plt.title('3D Water Depth Simulation')'''

# Hiển thị đồ thị
#plt.ioff()
#plt.show()
"""f_0_sum = np.zeros(round(T/dt))
f_0_head = np.zeros(round(T/dt))
f_0_foot = np.zeros(round(T/dt))

for it in range (round(T/dt)):
    t = it * dt
    print(f'iteration: {it}')
    F_BC[:,:] = 0
    
    if (t > 300):
        Ri_BC[:,:] = 0
    
    for i in range (1, n+1):
        for j in range (1, m+1):
            if (I < (h_0_BC_pre[i,j] + Ri_BC[i,j] * dt)):
                Re_BC[i,j] = Ri_BC[i,j] * dt - infil_t * dt
            else:
                Re_BC[i,j] = Ri_BC[i,j] * dt - h_0_BC_pre[i,j]
            
            Rcum_BC[i,j] = Ri_BC[i,j] * t
            Pcum_BC[i,j] = Pmax * (1 - np.exp(-0.046 * LAI * Rcum_BC[i,j] / Pmax))
            
            if (it >= 1):
                del_P_BC[i,j] = Pcum_BC[i,j] - Pcum_pre[i,j]
                P_BC[i,j] = P_pre[i,j] + del_P_BC[i,j] 
            Re_BC[i,j] = Ri_BC[i,j] * dt - P_BC[i,j] - I
            Pcum_pre = Pcum_BC.copy()
            P_pre = P_BC.copy()
            
            if (infil_opt == 1): #Philip eq
                infil_t = 0.5 * S_0 * t** (-0.5) + A
            elif (infil_opt == 2): #Green-Ampt eq
                infil_t = Ks * a
            elif (infil_opt == 3): #Horton eq
                infil_t = i_f + (i_0 - i_f) * np.exp(-k * t)
            elif (infil_opt == 4): #Holtan eq
                infil_t = i_f + (i_0 - i_f) * ((S - It)/(phi * D_Hol))**P_Hol
                I=infil_t * dt
                It = It + I
            I = infil_t * dt
    
    h_0_BC[:,:] = Re_BC[:,:] + h_0_BC_pre[:,:]
    H_0_BC[:,:] = H_BC[:,:] + h_0_BC[:,:]
    
    runoff_rate = np.zeros(round(T/dt))
    for i in range (2, n+1):
        for j in range (2, m+1):
            AVE, n_neighbor, NB = fr.Finding_repeat(H_0_BC, i, j, direct_opt)
            AVE, n_neighbor, NB = fd.Finding_delete(H_0_BC, i, j, direct_opt)
            f_i, f_0 = fl.Flow_to_neighbor(H_0_BC, i, j, direct_opt, AVE, NB, dX, dt, n_man, h_0_BC)
            f_0_sum[it] = f_0_sum[it] + f_0
            F_BC = tf.Total_flow(i, j, f_i, f_0, F_BC)
            if (j == 51):
                if (i == 2):
                    f_0_foot[it] = f_0 * 3600/dt
                elif (i == 501):
                    f_0_head[it] = f_0 * 3600/dt
    
    h_0_BC[1:(n+1), 1:(m+1)] = h_0_BC[1:(n+1), 1:(m+1)] + F_BC[1:(n+1), 1:[m+1]]
    h_0_BC_pre = h_0_BC.copy()
    
    Q = np.sum(F_BC[0, 1:(m+1)])* dY* dX
    runoff_rate[it] = Q* 3600/((dX* m* dY* n)*dt)
    runoff_rate[it] = F_BC[0,50] * 3600/(dt)
    
plt.figure(1)
plt.hold(True)

plt.plot(t / 60, runoff_rate[it], 'r*', label='Runoff Rate')  # Dòng chảy
plt.plot(t / 60, f_0_sum[it] * 3600 / (dt * m * n), 'b*', label='Total Outflow')  # Tổng dòng chảy ra
plt.plot(t / 60, f_0_foot[it], 'k*', label='Outflow at Foot')  # Dòng chảy tại chân
plt.plot(t / 60, f_0_head[it], 'g*', label='Outflow at Head')  # Dòng chảy tại đầu

plt.title('Runoff Rate and Outflow')
plt.xlabel('Time (minutes)')
plt.ylabel('Flow Rate (mm/s)')
plt.legend()  # Hiện thị chú thích cho các đường vẽ

plt.show()       
            
         """       



    