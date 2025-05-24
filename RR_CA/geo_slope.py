"""Tạo và lưu dữ liệu về độ dốc địa hình (geo_slope) từ một tệp DAT đầu vào.

    Hàm này đọc dữ liệu kích thước lưới từ một tệp DAT, tạo ra một mặt nghiêng 2D trong không gian 3D
    dựa trên phần trăm độ dốc được chỉ định, và sau đó tính toán và lưu tọa độ trung tâm của các ô lưới
    cùng với giá trị độ dốc trung bình của mỗi ô vào các tệp DAT riêng biệt trong thư mục đầu ra.

    Args:
        dat_file (str): Đường dẫn đến tệp DAT đầu vào chứa dữ liệu về kích thước lưới.
                          Tệp này dự kiến chứa một ma trận số, trong đó số hàng và số cột
                          sẽ được sử dụng để xác định kích thước của lưới.
        slope_percent (float, tùy chọn): Phần trăm độ dốc của mặt nghiêng cần tạo. Mặc định là 5.
        Z_size (float, tùy chọn): Giá trị dịch chuyển theo trục Z cho mặt nghiêng. Mặc định là 0.
        output_dir (str, tùy chọn): Đường dẫn đến thư mục nơi các tệp kết quả sẽ được lưu.
                                     Mặc định là thư mục hiện tại (".")

    Returns:
        None

    Output Files:
        - X_cell.dat: Tệp chứa tọa độ x của trung tâm các ô lưới.
        - Y_cell.dat: Tệp chứa tọa độ y của trung tâm các ô lưới.
        - geo_slope_cell.dat: Tệp chứa giá trị độ dốc địa hình trung bình của mỗi ô lưới (giá trị z).

    Prints:
        - Thông báo xác nhận việc lưu tệp thành công và đường dẫn thư mục.
        - Kích thước của dữ liệu đầu vào (số hàng và số cột).
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def geo_slope(dat_file, slope_percent=5, Z_size=0, output_dir="."):
    for i in plt.get_fignums():
        plt.close(i)
    
    input_data = np.loadtxt(dat_file)
    n, m = input_data.shape  # Kích thước mảng từ dữ liệu
    X_size = m
    Y_size = n
    # Tạo lưới
    dX = X_size / m
    dY = Y_size / n
    X, Y = np.meshgrid(np.arange(0, X_size + dX, dX), np.arange(0, Y_size + dY, dY))

    # Tạo mặt nghiêng Z
    slope = np.arcsin(slope_percent / 100) * 180 / np.pi
    Z = np.zeros_like(X)
    XYZ = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))

    # Xoay để tạo mặt nghiêng
    rotation_matrix = np.array([[1, 0, 0],
                                [0, np.cos(-np.radians(slope)), -np.sin(-np.radians(slope))],
                                [0, np.sin(-np.radians(slope)), np.cos(-np.radians(slope))]])
    xyz = XYZ @ rotation_matrix.T
    z = xyz[:, 2].reshape(Z.shape) + Z_size

    # Tính toán các tọa độ trung tâm của các ô
    geo_slope = z.copy()
    X_cell = (X[:-1, :-1] + X[:-1, 1:] + X[1:, :-1] + X[1:, 1:]) / 4
    Y_cell = (Y[:-1, :-1] + Y[:-1, 1:] + Y[1:, :-1] + Y[1:, 1:]) / 4
    geo_slope_cell = (geo_slope[:-1, :-1] + geo_slope[:-1, 1:] + geo_slope[1:, :-1] + geo_slope[1:, 1:]) / 4

    # Lưu các file kết quả
    np.savetxt(f"{output_dir}/X_cell.dat", X_cell, fmt="%.6f")
    np.savetxt(f"{output_dir}/Y_cell.dat", Y_cell, fmt="%.6f")
    np.savetxt(f"{output_dir}/geo_slope_cell.dat", geo_slope_cell, fmt="%.6f")

    print(f"Các file đã được lưu thành công tại: {output_dir}")
    print(f"Kích thước dữ liệu đầu vào: {n} x {m}")

