"""
Mô tả:
    Đoạn mã này kết hợp dữ liệu địa hình (DEM) từ file .dat và dữ liệu nước từ file ảnh TIFF,
    sau đó hiển thị chúng trong một biểu đồ 2D và lưu lại dưới dạng ảnh PNG.

Chức năng chính:
    - Đọc dữ liệu địa hình từ file .dat.
    - Đọc dữ liệu độ sâu nước từ file TIFF.
    - Vẽ bản đồ địa hình với colormap tùy chỉnh (vàng nhạt đến nâu) để phân biệt cao độ.
    - Lớp nước được vẽ đè lên, chỉ hiển thị các ô có mực nước vượt ngưỡng `wh_start`.
    - Dùng colormap 'Blues' cho lớp nước, tùy chỉnh để màu nước rõ hơn.
    - Lưu biểu đồ tổng hợp thành ảnh PNG với độ phân giải cao.

Thông số chính:
    - `dem_filename`: Đường dẫn đến file dữ liệu địa hình (.dat).
    - `water_folder`: Thư mục chứa ảnh TIFF mô phỏng mực nước theo thời gian.
    - `base_filename` & `index`: Dùng để xác định ảnh nước cụ thể cần vẽ.
    - `wh_start`: Ngưỡng tối thiểu để vẽ lớp nước (giá trị nước nhỏ hơn sẽ bị bỏ qua).
    - `output_folder`: Thư mục lưu kết quả hình ảnh đầu ra.

Lưu ý:
    - Dữ liệu đầu vào cần đúng định dạng và phải tồn tại.
    - Có thể điều chỉnh `vmin`, `vmax` để phù hợp với phạm vi độ cao và mực nước thực tế.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import tifffile as tiff
import os

# Đường dẫn đến file .dat và .tiff
dem_filename = 'E:/Thay canh/plotCA/DEM_HOALAC.dat'  # Thay bằng đường dẫn thực tế đến file .dat
water_folder = 'E:/Thay canh/plotCA/tiff(base)/'  # Thư mục chứa các ảnh nước (TIFF)
output_folder = 'E:/Thay canh/plotCA/output_images(1)/'  # Thư mục lưu ảnh đã xuất
base_filename = 'Generation'
index = 100  # Chỉ vẽ ảnh duy nhất, ví dụ Gen_700
wh_start = 2

# Tạo thư mục output nếu chưa có
os.makedirs(output_folder, exist_ok=True)

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
    plt.figure(figsize=(10, 8))

    # Vẽ lớp địa hình
    dem_img = plt.imshow(dem_data, cmap=custom_cmap, vmin=dem_min, vmax=dem_max)

    # Thêm thanh màu cho địa hình
    plt.colorbar(dem_img, label="Độ cao địa hình (m)")

    # Vẽ lớp nước: Chỉ vẽ các ô lưới có giá trị nước > wh_start
    water_mask = water_data > wh_start  # Tạo mặt nạ cho các giá trị nước > wh_start
    plt.imshow(np.ma.masked_where(~water_mask, water_data), cmap=new_cmap, vmin=wh_start, vmax=7, alpha=1.0)


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
    plt.show()  # Hiển thị ảnh

    print(f"Ảnh đã được lưu: {output_filename}")

except FileNotFoundError:
    print(f"File không tồn tại. Vui lòng kiểm tra đường dẫn.")
except ValueError as e:
    print(f"Lỗi khi đọc dữ liệu từ file: {e}")
