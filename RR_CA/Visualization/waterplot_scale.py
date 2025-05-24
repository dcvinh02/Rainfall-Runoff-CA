"""
Mô tả:
-------
Script này dùng để duyệt qua một loạt file ảnh định dạng TIFF, áp dụng bản đồ màu tùy chỉnh,
và xuất chúng dưới dạng ảnh PNG. Mỗi ảnh TIFF tương ứng với một bước thời gian (generation),
và được hiển thị với colormap tông màu xanh dương (Blues).

Chức năng chính:
----------------
- Đọc các ảnh TIFF từ thư mục đầu vào chứa thông tin như lượng mưa, nước mặt, v.v.
- Áp dụng colormap 'Blues' tùy chỉnh để tăng tính trực quan.
- Đặt giới hạn hiển thị giá trị ảnh trong khoảng từ 0 đến 7 (vmin, vmax).
- Thêm thanh màu (colorbar) và tiêu đề mang định dạng `Gen_XXX`.
- Lưu ảnh đã hiển thị vào thư mục đầu ra với định dạng PNG.

Tham số đầu vào:
----------------
- folder: đường dẫn tới thư mục chứa các ảnh TIFF đầu vào.
- output_folder: thư mục nơi lưu ảnh PNG sau khi xử lý.
- base_filename: tên cơ bản của các ảnh TIFF (ví dụ: Generation1.tiff, Generation2.tiff, ...).
- index: số ảnh cần xử lý (vẽ ảnh từ 1 đến index - 1).
- dem_filename (không được dùng trong đoạn này): có thể là dữ liệu nền để xử lý thêm nếu cần sau này.

Cài đặt mặc định:
-----------------
- Colormap: CustomBlues từ 40% đến 100% của cmap `Blues`.
- Vùng hiển thị dữ liệu: vmin = 0, vmax = 7.
- Kích thước ảnh đầu ra: 8x6 inches.
- Đảo ngược trục Y để hiển thị ảnh theo đúng định hướng raster.
"""

import numpy as np
import tifffile as tiff
import matplotlib.pyplot as plt
import os
from matplotlib.colors import LinearSegmentedColormap

# Đường dẫn thư mục chứa ảnh
#folder = 'E:/Thay canh/plotCA/TIF_base/'
folder = 'E:/tiffrain1/'
output_folder = 'E:/Thay canh/plotCA/output_images(rain)/'  # Thư mục lưu ảnh đã xuất
base_filename = 'Generation'
index = 6464  # Chỉ vẽ ảnh duy nhất, ví dụ Gen_700
dem_filename = 'E:/Thay canh/plotCA/DEM_HOALAC.dat'  # Thay bằng đường dẫn thực tế đến file .dat

# Tạo thư mục output nếu chưa có
os.makedirs(output_folder, exist_ok=True)

for i in range (1,index):
    # Tạo đường dẫn file
    filename = f"{folder}{base_filename}{i}.tiff"

    try:
        # Load file TIFF
        tfile = tiff.imread(filename)

        # Tạo colormap con từ colormap 'Blues' (ví dụ: lấy từ vị trí 0.2 đến 0.8 của colormap)
        cmap = plt.cm.Blues
        new_cmap = LinearSegmentedColormap.from_list("CustomBlues", cmap(np.linspace(0.4, 1.0, 256)))

        # Hiển thị ảnh với colormap tùy chỉnh
        fig, ax = plt.subplots(figsize=(8, 6))
        img = plt.imshow(tfile, cmap=new_cmap, vmin=0, vmax=7)  # Cố định scale vmin=4 và vmax=5
        plt.colorbar(img, label="Value")
        
        # Đặt tiêu đề là Gen_number
        plt.title(f'Gen_{i:03d}')  # Tiêu đề có định dạng Gen_001, Gen_002, ...
        plt.xlabel("X Coordinates")
        plt.ylabel("Y Coordinates")
        
        # Đảo ngược trục Y
        plt.gca().invert_yaxis()

        # Lưu ảnh
        output_filename = os.path.join(output_folder, f"output_image_{i:03d}.png")
        plt.savefig(output_filename, bbox_inches='tight', dpi=300)
        plt.close(fig)
        print(f"Ảnh đã được lưu: {output_filename}")
    except FileNotFoundError:
        print(f"File {filename} không tồn tại, bỏ qua.")
