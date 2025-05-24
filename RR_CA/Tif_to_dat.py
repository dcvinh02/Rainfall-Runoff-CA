"""
Đoạn mã này thực hiện việc đọc một tệp GeoTIFF, thay đổi kích thước của nó bằng phương pháp nội suy song tuyến (bilinear resampling),
và sau đó lưu dữ liệu đã được thay đổi kích thước thành một tệp DAT ở định dạng văn bản.

Các bước thực hiện chính:
1. Chỉ định đường dẫn cho tệp GeoTIFF đầu vào (`tiff_path`) và tệp DAT đầu ra (`dat_path`).
2. Mở tệp GeoTIFF bằng thư viện `rasterio`.
3. Lấy kích thước ban đầu (chiều rộng và chiều cao) của tệp TIFF.
4. Xác định kích thước mới (chiều rộng và chiều cao) mong muốn cho việc thay đổi kích thước.
5. Tính toán tỷ lệ thay đổi kích thước theo chiều rộng và chiều cao.
6. Đọc kênh đầu tiên của tệp TIFF và thực hiện việc thay đổi kích thước bằng phương pháp nội suy song tuyến, lưu kết quả vào biến `data_resampled`.
7. Chuyển đổi kiểu dữ liệu của mảng đã thay đổi kích thước thành `numpy.float32`.
8. Mở tệp DAT đầu ra ở chế độ ghi.
9. Duyệt qua từng hàng của mảng dữ liệu đã được thay đổi kích thước.
10. Lưu mỗi hàng vào tệp DAT, với định dạng số học dấu phẩy động có độ chính xác 10 chữ số sau dấu thập phân và các giá trị được phân tách bằng ba dấu cách.

Lưu ý:
- Các đường dẫn tệp (`tiff_path` và `dat_path`) hiện đang được thiết lập cứng. Để sử dụng linh hoạt hơn, có thể cân nhắc việc truyền chúng như là tham số hoặc lấy từ cấu hình.
- Phương pháp nội suy song tuyến được sử dụng để thay đổi kích thước. Các phương pháp khác có thể được chọn tùy thuộc vào yêu cầu cụ thể.
- Dữ liệu được lưu vào tệp DAT dưới dạng các hàng, với các giá trị trong mỗi hàng được phân tách bằng ba dấu cách.
"""

import rasterio
from rasterio.enums import Resampling
import numpy as np

tiff_path = r"E:\DEM\DEM_HOALAC.tif"
dat_path = r"E:\DEM\HOALAC_100_200.dat"
#tiff_path = r"INPUT"
#dat_path = r"OUPUT"
with rasterio.open(tiff_path) as src:
    old_width = src.width # Kích thước cũ
    old_height = src.height
    new_width = 100 # Kích thước mới
    new_height = 200
    scale_width = new_width / old_width
    scale_height = new_height / old_height
    data_resampled = src.read(1, out_shape=(new_height, new_width), resampling=Resampling.bilinear )
data_float = data_resampled.astype(np.float32)
with open(dat_path, 'w') as f:
    for row in data_float:
        np.savetxt(f, [row], fmt='%.10e', delimiter='   ')