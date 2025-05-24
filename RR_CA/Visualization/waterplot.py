"""
Mô tả:
    Script này dùng để đọc một file ảnh TIFF mô phỏng kết quả Độ cao nước tại một thời điểm (generation) cụ thể,
    sau đó hiển thị và lưu ảnh dưới dạng PNG với màu sắc thể hiện giá trị độ sâu hoặc độ cao.

Chức năng chính:
    - Đọc dữ liệu ảnh từ file TIFF (được xuất từ mô hình CA).
    - Hiển thị ảnh với thang màu 'Blues', cố định giá trị vmin = 0 và vmax = 5.
    - Tùy chỉnh tiêu đề, nhãn trục, thanh màu và đảo trục Y để ảnh dễ nhìn hơn.
    - Lưu ảnh đã xử lý vào thư mục đầu ra với độ phân giải cao.

Tham số cần chỉnh:
    - `folder`: Đường dẫn đến thư mục chứa file TIFF.
    - `output_folder`: Đường dẫn lưu ảnh đầu ra (PNG).
    - `index`: Số thứ tự của generation cần vẽ (ví dụ: Generation2222.tiff).
    - `dem_filename`: (Không dùng trong đoạn này nhưng có thể để mở rộng thêm DEM nếu cần).
    
Lưu ý:
    - Nếu file không tồn tại, chương trình sẽ thông báo và bỏ qua mà không gây lỗi.
"""

import tifffile as tiff 
import matplotlib.pyplot as plt
import os

# Đường dẫn thư mục chứa ảnh
folder = 'E:/Thay canh/plotCA/tiff/'
output_folder = 'E:/Thay canh/plotCA/output_images(1)/'  # Thư mục lưu ảnh đã xuất
base_filename = 'Generation'
index = 2222  # Chỉ vẽ ảnh duy nhất, ví dụ Gen_700
dem_filename = 'E:/Thay canh/plotCA/DEM_HOALAC.dat'  # Thay bằng đường dẫn thực tế đến file .dat
# Tạo thư mục output nếu chưa có
os.makedirs(output_folder, exist_ok=True)

# Tạo đường dẫn file
filename = f"{folder}{base_filename}{index}.tiff"

try:
    # Load file TIFF
    tfile = tiff.imread(filename)

    # Hiển thị ảnh với colormap
    plt.figure(figsize=(8, 6))
    img = plt.imshow(tfile, cmap='Blues', vmin=0, vmax=5)  # Cố định scale vmin=0 và vmax=5
    plt.colorbar(img, label="Value")
    
    # Đặt tiêu đề là Gen_number
    plt.title(f'Gen_{index:03d}')  # Tiêu đề có định dạng Gen_001, Gen_002, ...
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    
    # Đảo ngược trục Y
    plt.gca().invert_yaxis()

    # Lưu ảnh
    output_filename = os.path.join(output_folder, f"output_image_{index:03d}.png")
    plt.savefig(output_filename, bbox_inches='tight', dpi=300)
    plt.show()  # Hiển thị ảnh

    print(f"Ảnh đã được lưu: {output_filename}")

except FileNotFoundError:
    print(f"File {filename} không tồn tại, bỏ qua.")
