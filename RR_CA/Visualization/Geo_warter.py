"""
Mô tả:
-------
Script này tạo ảnh chồng lớp giữa dữ liệu địa hình (DEM) và lớp mực nước từ ảnh TIFF 
ở một bước thời gian cụ thể, và lưu ảnh đầu ra dưới dạng ảnh màu 2D (raster).

Chức năng chính:
----------------
- Đọc dữ liệu địa hình từ file .dat (định dạng ASCII).
- Đọc dữ liệu độ sâu nước từ file .tiff tại một thời điểm cụ thể (generation).
- Sử dụng mặt nạ để chỉ hiển thị các ô có độ sâu nước lớn hơn một ngưỡng nhất định (`wh_start`).
- Tạo bản đồ màu tùy chỉnh cho địa hình (tông màu nâu đất) và nước (tông màu xanh nước biển).
- Hiển thị lớp địa hình và lớp nước chồng lên nhau trong ảnh 2D.
- Lưu ảnh đã chồng lớp vào thư mục chỉ định.

Tham số đầu vào:
----------------
- dem_filename: đường dẫn đến file chứa dữ liệu DEM (.dat).
- water_folder: thư mục chứa ảnh TIFF biểu thị mực nước tại các bước thời gian.
- output_folder: thư mục nơi lưu các ảnh đã kết hợp.
- base_filename: tên cơ bản của mỗi ảnh TIFF (ví dụ: Generation1.tiff).
- index: số bước thời gian tối đa, ảnh được lấy tại bước thời gian có chỉ số `index`.
- wh_start: ngưỡng xác định vùng có nước để hiển thị (ví dụ: chỉ hiển thị nước > 2).

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import tifffile as tiff
import os

# Đường dẫn đến file .dat và .tiff
dem_filename = 'E:/Thay canh/plotCA/DEM_HOALAC.dat'  # Thay bằng đường dẫn thực tế đến file .dat
water_folder = 'E:/Thay canh/plotCA/TIF_base/'  # Thư mục chứa các ảnh nước (TIFF)
output_folder = 'E:/Thay canh/plotCA/output_images(1)/'  # Thư mục lưu ảnh đã xuất
base_filename = 'Generation'
index = 884  # Chỉ vẽ ảnh duy nhất, ví dụ Gen_700
wh_start = 2

# Tạo thư mục output nếu chưa có
os.makedirs(output_folder, exist_ok=True)
for i in range (1,index):
    try:
        # Đọc dữ liệu từ file .dat (địa hình)
        dem_data = np.loadtxt(dem_filename)

        # Lấy thông tin giới hạn giá trị độ cao của địa hình
        dem_min, dem_max = 0, 50

        # Tạo colormap tùy chỉnh từ vàng nhạt đến nâu
        custom_cmap = LinearSegmentedColormap.from_list(
            "CustomBrown", ["#F5DEB3", "#D2B48C", "#8B4513"]  # Vàng nhạt -> Nâu nhẹ -> Nâu trung tính
        )

        # Tạo đường dẫn file cho ảnh nước (tiff)
        water_filename = f"{water_folder}{base_filename}{index}.tiff"

        # Load file TIFF nước
        water_data = tiff.imread(water_filename)

        # Tạo colormap con từ colormap 'Blues' (ví dụ: lấy từ vị trí 0.2 đến 0.8 của colormap)
        cmap = plt.cm.Blues
        new_cmap = LinearSegmentedColormap.from_list("CustomBlues", cmap(np.linspace(0.4, 1.0, 256)))

        # Vẽ địa hình với colormap tùy chỉnh
        fig, ax = plt.subplots(figsize=(8, 6))

        # Vẽ lớp địa hình
        dem_img = plt.imshow(dem_data, cmap=custom_cmap, vmin=0, vmax=50)

        # Thêm thanh màu cho địa hình
        plt.colorbar(dem_img, label="Độ cao địa hình (m)")

        # Vẽ lớp nước: Chỉ vẽ các ô lưới có giá trị nước > wh_start
        water_mask = water_data > wh_start  # Tạo mặt nạ cho các giá trị nước > wh_start
        plt.imshow(np.ma.masked_where(~water_mask, water_data), cmap=new_cmap, vmin=wh_start, vmax=5, alpha=0.8)


        # Thêm thanh màu cho nước
        plt.colorbar(label="Độ sâu nước (m)")

        # Tiêu đề và nhãn
        plt.title(f"Địa hình và Nước - Gen_{index:03d}")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")

        # Đảo ngược trục Y
        plt.gca().invert_yaxis()

        # Lưu ảnh
        output_filename = os.path.join(output_folder, f"combined_image_{index:03d}.png")
        plt.savefig(output_filename, bbox_inches='tight', dpi=300)
        plt.close(fig)
        print(f"Ảnh đã được lưu: {output_filename}")

    except FileNotFoundError:
        print(f"File không tồn tại. Vui lòng kiểm tra đường dẫn.")
    except ValueError as e:
        print(f"Lỗi khi đọc dữ liệu từ file: {e}")
