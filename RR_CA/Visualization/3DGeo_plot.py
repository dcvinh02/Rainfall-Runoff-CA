"""
Mô tả:
    Đoạn mã này thực hiện việc đọc dữ liệu Độ cao nước từ một file .dat chứa ma trận độ cao (DEM),
    sau đó trực quan hóa địa hình đó bằng đồ thị 3D với màu sắc thể hiện mức độ cao.

Chức năng chính:
    - Đọc dữ liệu DEM từ file .dat định dạng ma trận.
    - Tạo lưới tọa độ không gian X, Y, Z để biểu diễn địa hình 3D.
    - Tạo colormap tùy chỉnh (từ màu vàng nhạt đến nâu) để hiển thị độ cao trực quan hơn.
    - Vẽ đồ thị 3D bề mặt địa hình với Matplotlib và điều chỉnh góc nhìn, tỷ lệ các trục.
    - Lưu ảnh đồ thị dưới định dạng PNG với độ phân giải cao.

Thông số chính:
    - `dem_filename`: Đường dẫn tới file dữ liệu DEM (.dat), cần định dạng ma trận số thực.
    - `dem_min`, `dem_max`: Giới hạn giá trị hiển thị cho độ cao để điều chỉnh colormap phù hợp.
    - `output_filename`: Tên file ảnh đầu ra (định dạng PNG).

Lưu ý:
    - File DEM phải tồn tại và có định dạng phù hợp (ma trận số).
    - Nếu không tìm thấy file hoặc file lỗi định dạng, chương trình sẽ thông báo lỗi rõ ràng.
"""

from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Thêm thư viện cho đồ thị 3D

# Đường dẫn đến file .dat
dem_filename = 'E:\Thay canh\plotCA\DEM_HOALAC.dat'  # Thay bằng đường dẫn thực tế đến file .dat

try:
    # Đọc dữ liệu từ file .dat
    dem_data = np.loadtxt(dem_filename)

    # Lấy thông tin giới hạn giá trị độ cao
    dem_min, dem_max = 0, 50
    print(f"Độ cao tối thiểu: {dem_min}, Độ cao tối đa: {dem_max}")

    # Tạo colormap tùy chỉnh từ vàng nhạt đến nâu
    custom_cmap = LinearSegmentedColormap.from_list(
        "CustomBrown", ["#F5DEB3", "#D2B48C", "#8B4513"]  # Vàng nhạt -> Nâu nhẹ -> Nâu trung tính
    )

    # Lấy kích thước ma trận của dữ liệu địa hình
    rows, cols = dem_data.shape

    # Tạo lưới tọa độ cho đồ thị 3D
    X, Y = np.meshgrid(np.arange(cols), np.arange(rows))
    Z = dem_data  # Độ cao là dữ liệu trong ma trận

    # Tạo đồ thị 3D
    fig = plt.figure(figsize=(15, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Vẽ bề mặt 3D
    surf = ax.plot_surface(X, Y, Z, cmap=custom_cmap, vmin=dem_min, vmax=dem_max)

    # Thêm thanh màu
    fig.colorbar(surf, label="Độ cao địa hình (m)")

    # Tiêu đề và nhãn
    ax.set_title("Địa hình 3D Hòa Lạc")
    ax.set_xlabel("X (m)", labelpad = 15)  # Đơn vị là mét
    ax.set_ylabel("Y (m)", labelpad = 15)  # Đơn vị là mét
    ax.set_zlabel("Z (Độ cao)", labelpad = 15)

    # Đảm bảo trục có tỷ lệ đúng
    x_range = np.max(X) - np.min(X)
    y_range = np.max(Y) - np.min(Y)
    z_range = np.max(Z) - np.min(Z)
    ax.set_box_aspect([x_range, y_range, z_range])  # Thiết lập tỷ lệ các trục: X, Y, Z

    # Thiết lập góc nhìn 3D
    ax.view_init(elev=30, azim=225)  # Elevation = 30 độ, Azimuth = 45 độ

    # Lưu ảnh
    output_filename = "dem_3d_lightbrown_plot(test1).png"
    plt.savefig(output_filename, bbox_inches='tight', dpi=300)
    plt.show()
    print(f"Ảnh địa hình 3D đã được lưu: {output_filename}")

except FileNotFoundError:
    print(f"File {dem_filename} không tồn tại. Vui lòng kiểm tra đường dẫn.")
except ValueError as e:
    print(f"Lỗi khi đọc dữ liệu từ file: {e}")
