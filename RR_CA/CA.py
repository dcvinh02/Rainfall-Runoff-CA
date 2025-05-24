import numpy as np
import Boundary
import os
#import Finding_repeat as fr
import Finding_delete as fd
import Flow_to_neighbor as fl
import Total_flow as tf
import matplotlib.pyplot as plt
import increase_dt as inc
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
from to_tif import save_to_tiff
import time

plt.close('all')

current_dir = os.path.dirname(os.path.abspath(__file__))
x_cell_path = os.path.join(current_dir, 'X_cell.dat')
y_cell_path = os.path.join(current_dir, 'Y_cell.dat')
geo_slope_cell_path = os.path.join(current_dir, 'geo_slope_cell.dat')
Ri_path = os.path.join(current_dir, 'Ri.dat')
# Geometry input
X_cell = np.loadtxt(x_cell_path)
X_cell = X_cell * 1000 # đổi đơn vị từ m sang mm
Y_cell = np.loadtxt(y_cell_path)
Y_cell = Y_cell * 1000

geo_slope_cell = np.loadtxt(geo_slope_cell_path)
#geo_slope_cell = np.loadtxt('E:\DEM\HOALAC_DEM.dat')

n = X_cell.shape[0]
m = X_cell.shape[1] 

Ri = np.loadtxt(Ri_path)
Ri = (Ri) * 1000/3600 # đổi m/h sang mm/s

# Khởi tạo giá trị biến
n_man = 0.01 * (1000 ** (-1/3)) # m -> mm
H = geo_slope_cell * 1000 # m -> mm
wall = 500
gate = 1
delta_H_out = 50
dt = 10
direct_opt = 3
T = 30 * 60 # Time simulator, h
rain_time = 15 * 60
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
real_time = []
simu_time = []
H_BC, Ri_BC = Boundary.Boudary_conditions(H, Ri, wall, gate, delta_H_out)
t_pre = 0
t = []
it = 1
#fig = plt.figure()
'''fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12,8))
ax1.set_xlabel('Simulation Time (minutes)')
ax1.set_ylabel('Runoff Rate (mm/h)')
ax1.set_title('Runoff Rate Over Time')
ax2.set_xlabel('Simulation Time (minutes)')
ax2.set_ylabel('Real Time (seconds)')
ax2.set_title('Real Time Per Simulated Minute')'''
fig1, ax1 = plt.subplots(figsize=(12,4))  # Đồ thị cho runoff rate
fig2, ax2 = plt.subplots(figsize=(12,4))  # Đồ thị cho real time

ax1.set_xlabel('Simulation Time (minutes)')
ax1.set_ylabel('Runoff Rate (mm/h)')
ax1.set_title('Runoff Rate Over Time')

ax2.set_xlabel('Simulation Time (minutes)')
ax2.set_ylabel('Real Time (seconds)')
ax2.set_title('Real Time Per Simulated Minute')
generation = 0
with open('output','w+') as fileID:
    fileID.write(f"{'t(min)' :>6} {'runoff_rate(mm/h)' :>12}\n")
    runoff_rate = []
    while (t_pre < T):
        start_time = time.time()
        print(f"iteration: {it}")
        t_current = t_pre + dt
        F_BC.fill(0)
        flag = 0
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
        for i in range(1, n):
            for j in range(1, m):
                AVE, n_neighbor, NB = fd.Finding_delete(H_0_BC, i, j, direct_opt)
                f_i, f_0, dt, flag = fl.Flow_to_neighbor(H_0_BC, i, j, direct_opt, AVE, NB, dX, dt, n_man, h_0_BC, flag)
                if flag: 
                    break
                F_BC = tf.Total_flow(i, j, f_i, f_0, F_BC)
            if flag: 
                break
        generation+=1
        save_to_tiff(h_0_BC, generation)
        dt, flag = inc.increase(H_0_BC, n, m, direct_opt, NB, dX, dt, n_man, h_0_BC, flag)
        if flag: 
            continue
        h_0_BC[1:n+1, 1:m+1] += F_BC[1:n+1, 1:m+1]
        h_0_BC_pre = np.copy(h_0_BC)
        Q = np.sum(F_BC[0, 1:m+1]) * dY * dX
        current_runoff_rate = Q * 3600 / ((dX * m * dY * n) * dt)
        runoff_rate.append(current_runoff_rate)
        simu_time.append(t_current/60)
        end_time = time.time()
        real_time_taken = end_time - start_time
        real_time.append(real_time_taken)
        print(f"time {t_current /60:.2f}(min) - runoff_rate {current_runoff_rate:.2f} (mm/h)")
        fileID.write(f"{t_current / 60:6.2f} {current_runoff_rate:12.8f}\n")
        '''plt.savefig('E:/final_runoff_rate_plot1.png', dpi=300)
        plt.show()
        plt.pause(0.1)
        plt.subplot(2, 1, 1) 
        plt.plot(t_current / 60, current_runoff_rate, 'r*')
        plt.grid()
        # Vẽ biểu đồ Real Time
        plt.subplot(2, 1, 2)
        plt.plot(t_current / 60, real_time_taken, 'b*')
        plt.grid()
        plt.pause(0.1)'''
        with open('E:/chi/output_time_200.txt', 'a') as time_file:
            time_file.write(f"{real_time_taken:<20} {t_current / 60:.2f}\n")
        # Cập nhật trạng thái mô phỏng
        ax1.plot(t_current / 60, current_runoff_rate, 'r*')
        ax1.grid()

        # Vẽ vào cửa sổ thứ hai (Real Time)
        ax2.plot(t_current / 60, real_time_taken, 'b*')
        ax2.grid()

        plt.pause(0.1)
        t_pre = t_current
        t_current += dt
        it += 1
        plt.tight_layout()
        ax1.figure.savefig('E:/runoff100.png', dpi=300)
        ax2.figure.savefig('E:/final_runoff_and_real_time_plot100.png', dpi=300)
plt.show()


