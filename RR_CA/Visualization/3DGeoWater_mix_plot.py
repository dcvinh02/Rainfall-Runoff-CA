"""
Mô tả:
-------
Script này thực hiện việc trực quan hóa địa hình và mực nước theo từng bước thời gian 
dưới dạng biểu đồ 3D từ dữ liệu DEM (.dat) và các ảnh mực nước (.tiff). 
Mỗi bước thời gian tương ứng với một file ảnh đầu ra 3D được lưu dưới dạng .png.

Chức năng chính:
----------------
- Đọc dữ liệu độ cao DEM từ file .dat.
- Đọc dữ liệu độ sâu nước từ các file .tiff theo từng bước thời gian.
- Loại bỏ viền lưới giả (boundary) trong dữ liệu nước.
- Tính toán mặt nước bằng cách cộng mực nước vào độ cao địa hình.
- Tạo mặt đất với bản đồ màu tùy chỉnh (màu nâu đất).
- Tạo mặt nước với bản đồ màu tùy chỉnh (tông màu xanh nước biển).
- Ánh xạ mặt nước chỉ tại các ô có nước (theo ngưỡng `wh_start`).
- Hiển thị cả địa hình và mặt nước trong biểu đồ 3D với tỉ lệ và góc nhìn tùy chỉnh.
- Lưu từng hình ảnh biểu đồ 3D vào thư mục chỉ định.
- Bắt lỗi nếu thiếu file hoặc lỗi dữ liệu.

Tham số cần thiết:
------------------
- dem_filename: đường dẫn đến file chứa dữ liệu DEM (.dat).
- water_folder: thư mục chứa các file mực nước dạng TIFF theo từng bước thời gian.
- output_folder: nơi lưu trữ các ảnh biểu đồ 3D.
- base_filename: tên cơ bản cho mỗi file TIFF (ví dụ: Generation1.tiff, Generation2.tiff...).
- index: tổng số bước thời gian (số lượng file tiff cần xử lý).
- wh_start: ngưỡng phân biệt có nước hay không (lọc các giá trị nhỏ không đáng kể).

Kết quả:
--------
- Các ảnh .png được lưu vào thư mục output, mỗi ảnh là biểu đồ 3D của địa hình và mực nước tại bước thời gian tương ứng.
- In log trạng thái sau mỗi lần lưu ảnh thành công hoặc gặp lỗi.
"""

from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tifffile as tiff
import os

# Đường dẫn đến file .dat và .tiff
dem_filename = 'E:/Thay canh/plotCA/DEM_HOALAC.dat'
water_folder = 'E:/Thay canh/plotCA/TIF_base/'
output_folder = 'E:/Thay canh/plotCA/output_images(DEM)/'
base_filename = 'Generation'
index = 3458
wh_start = 1

os.makedirs(output_folder, exist_ok=True)

for i in range(1, index):
    try:
        dem_data = np.loadtxt(dem_filename)
        dem_min, dem_max = 0, 50
        water_min, water_max = 2, 7

        custom_cmap = LinearSegmentedColormap.from_list(
            "CustomBrown", ["#F5DEB3", "#D2B48C", "#8B4513"]
        )
        cmap = plt.cm.Blues
        water_cmap = LinearSegmentedColormap.from_list("CustomBlues", cmap(np.linspace(0.4, 1.0, 256)))

        rows, cols = dem_data.shape
        X, Y = np.meshgrid(np.arange(cols), np.arange(rows))

        fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={"projection": "3d"})
        water_filename = f"{water_folder}{base_filename}{i}.tiff"
        water_data_withboundary = tiff.imread(water_filename)
        water_data = water_data_withboundary[1:-1, 1:-1]

        water_mask = water_data >= wh_start
        Z_w = dem_data + water_data
        Z_water = np.where(water_mask, Z_w, np.nan)

        surf_land = ax.plot_surface(X, Y, dem_data, cmap=custom_cmap, vmin=dem_min, vmax=dem_max)

        normalized_water = (water_data - water_min) / (water_max - water_min)
        normalized_water = np.clip(normalized_water, 0, 1)
        water_facecolors = water_cmap(normalized_water)

        surf_water = ax.plot_surface(X, Y, Z_water, facecolors=water_facecolors, rstride=1, cstride=1)

        cbar_land = fig.colorbar(surf_land, ax=ax, shrink=0.5, aspect=10, label="Độ cao địa hình (m)", pad=0.1)
        cbar_water = fig.colorbar(
            plt.cm.ScalarMappable(norm=plt.Normalize(vmin=water_min, vmax=water_max), cmap=water_cmap),
            ax=ax, shrink=0.5, aspect=10, label="Độ cao nước (m)", pad=0.1
        )

        ax.set_title("Địa hình và Nước")
        ax.set_xlabel("X (m)")
        ax.set_ylabel("Y (m)")
        ax.set_zlabel("Z (Độ cao)")

        x_range, y_range, z_range = np.ptp(X), np.ptp(Y), np.ptp(Z_w)
        ax.set_box_aspect([x_range, y_range, z_range * 2])

        ax.view_init(elev=30, azim=220)

        output_filename = os.path.join(output_folder, f"dem_3d_lightbrown_plot_{i:03d}.png")
        plt.savefig(output_filename, bbox_inches='tight', dpi=300)
        plt.close(fig)
        print(f"Ảnh địa hình 3D đã được lưu: {output_filename}")

    except FileNotFoundError:
        print(f"File không tồn tại: {water_filename} hoặc {dem_filename}.")
    except ValueError as e:
        print(f"Lỗi đọc dữ liệu: {e}")
    except Exception as e:
        print(f"Lỗi không mong đợi: {e}")

#initial
'''from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tifffile as tiff
import os

# Đường dẫn đến file .dat và .tiff
# Đường dẫn đến file .dat
dem_filename = 'E:/Thay canh/plotCA/DEM_HOALAC.dat'  # Thay bằng đường dẫn thực tế đến file .dat
water_folder = 'E:/Thay canh/plotCA/TIF_base/'  # Thư mục chứa các ảnh nước (TIFF)
output_folder = 'E:/Thay canh/plotCA/output_images(DEM)/'  # Thư mục lưu ảnh đã xuất
base_filename = 'Generation'
index = 3458  # Chỉ vẽ ảnh duy nhất, ví dụ Gen_700
wh_start = 1  # Ngưỡng phân biệt giữa nước và địa hình
for i in range (1,index):
# Tạo thư mục output nếu chưa có
    os.makedirs(output_folder, exist_ok=True)

    try:
        # Đọc dữ liệu từ file .dat (địa hình)
        dem_data = np.loadtxt(dem_filename)

        # Lấy thông tin giới hạn giá trị độ cao, water
        dem_min, dem_max = 0, 50
        water_min, water_max = 2, 7

        # Tạo colormap tùy chỉnh từ vàng nhạt đến nâu cho đất
        custom_cmap = LinearSegmentedColormap.from_list(
            "CustomBrown", ["#F5DEB3", "#D2B48C", "#8B4513"]  # Vàng nhạt -> Nâu nhẹ -> Nâu trung tính
        )

        # Tạo colormap cho nước từ colormap 'Blues' (ví dụ: lấy từ vị trí 0.2 đến 0.8 của colormap)
        cmap = plt.cm.Blues
        water_cmap = LinearSegmentedColormap.from_list("CustomBlues", cmap(np.linspace(0.4, 1.0, 256)))

        # Lấy kích thước ma trận của dữ liệu địa hình
        rows, cols = dem_data.shape

        # Tạo lưới tọa độ cho đồ thị 3D
        X, Y = np.meshgrid(np.arange(cols), np.arange(rows))

        # Tạo đồ thị 3D
        fig = plt.subplots(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')

        # Tạo đường dẫn file cho ảnh nước (tiff)
        water_filename = f"{water_folder}{base_filename}{index}.tiff"

        # Load file TIFF nước
        water_data_withboundary = tiff.imread(water_filename)
        water_data = water_data_withboundary[1:-1, 1:-1]  # Cắt bỏ biên nếu có

        # Tạo mask cho vùng đất và vùng nước
        water_mask = water_data >= wh_start  # Nước cao hơn ngưỡng wh_start

        # Tạo độ cao mới = Địa hình + Nước 
        Z_w = dem_data + water_data

        # Vẽ bề mặt 3D cho địa hình
        surf_land = ax.plot_surface(X, Y, Z_w, cmap=custom_cmap, vmin=dem_min, vmax=dem_max)

        # Vẽ bề mặt 3D cho nước
        # surf_water = ax.plot_surface(X, Y, Z_w, cmap=water_cmap, vmin=water_min, vmax=water_max)
        water_min_real = np.min(water_data)
        water_max_real = np.max(water_data) 
        print(water_min_real,water_max_real)
        print(water_min,water_max)
        # Áp dụng transparent cho vùng nước nhỏ hơn wh_start bằng cách sử dụng alpha
        # surf_water.set_alpha(1.0)  # Mặc định alpha = 1 cho bề mặt nước
        water_data[water_data < wh_start] = np.nan  # Chuyển giá trị nhỏ hơn wh_start thành NaN (tương đương transparent)
        # Vẽ lại bề mặt nước với alpha cho các vùng nước nhỏ hơn wh_start là transparent
        # Chuẩn hóa dữ liệu water_data để đưa vào phạm vi [0, 1]
    
        # normalized_water = (water_data - water_min_real) / (water_max_real - water_min_real)
        normalized_water = (water_data - water_min) / (water_max - water_min)  # lấy giá trị này vì cần tỉ lệ cho khaonrg max min này, đỒng thời vì giá trị bên ngoài clip sẽ cắt hộ, 
        normalized_water = np.clip(normalized_water, 0, 1)  # Đảm bảo giá trị nằm trong [0, 1]
        

        # Tạo facecolors bằng cách ánh xạ dữ liệu normalized_water vào colormap
        water_facecolors = water_cmap(normalized_water)

        # Sử dụng water_facecolors trong plot_surface
        surf_water = ax.plot_surface(
            X, Y, Z_w,
            facecolors=water_facecolors,
            cmap=water_cmap, # bật lên ra kết quả khác, sợ là xung đột, nhưng kết quả mịn hơn???
            # vmin=water_min, vmax=water_max,
            # rstride=1, 
            # cstride=1, 
            # alpha=1
    )

        # Thêm thanh màu cho địa hình
        cbar_land = fig.colorbar(surf_land, ax=ax, shrink=0.5, aspect=10, label="Độ cao địa hình (m)", pad=0.1)
        
        # Thêm thanh màu cho nước
        cbar_water = fig.colorbar(plt.cm.ScalarMappable(cmap=water_cmap, norm=plt.Normalize(vmin=water_min, vmax=water_max)), ax=ax, shrink=0.5, aspect=10, label="Độ cao nước (m)", pad=0.1)

        # Tiêu đề và nhãn
        ax.set_title("Địa hình và Nước")
        ax.set_xlabel("X (m)")  # Đơn vị là mét
        ax.set_ylabel("Y (m)")  # Đơn vị là mét
        ax.set_zlabel("Z (Độ cao)")

        # Đảm bảo trục có tỷ lệ đúng
        x_range = np.max(X) - np.min(X)
        y_range = np.max(Y) - np.min(Y)
        z_range = np.max(Z_w) - np.min(Z_w)
        ax.set_box_aspect([x_range, y_range, z_range])  # Thiết lập tỷ lệ các trục: X, Y, Z

        # Thiết lập góc nhìn 3D
        ax.view_init(elev=30, azim=220)  # Elevation = 30 độ, Azimuth = 225 độ

        # Lưu ảnh
        output_filename = os.path.join(output_folder, f"dem_3d_lightbrown_plot_{index:03d}.png")
        plt.savefig(output_filename, bbox_inches='tight', dpi=300)
        plt.close(fig)
        print(f"Ảnh địa hình 3D đã được lưu: {output_filename}")

    except FileNotFoundError:
        print(f"File {dem_filename} không tồn tại. Vui lòng kiểm tra đường dẫn.")
    except ValueError as e:
        print(f"Lỗi khi đọc dữ liệu từ file: {e}")'''
