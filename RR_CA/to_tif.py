"""Lưu một mảng NumPy 2D vào một tệp GeoTIFF.

    Hàm này nhận một mảng NumPy 2D, thông tin về thế hệ, kích thước pixel, tọa độ góc trên bên trái và hệ tọa độ,
    sau đó lưu mảng này thành một tệp GeoTIFF trên đĩa.

    Các bước thực hiện chính:
    1. Kiểm tra xem mảng đầu vào có đúng 2 chiều hay không. Nếu không, hàm sẽ gây ra lỗi ValueError.
    2. Tạo đường dẫn cho tệp đầu ra dựa trên số thế hệ được cung cấp.
    3. Lấy kích thước (chiều cao và chiều rộng) của mảng đầu vào.
    4. Tạo một đối tượng transform của rasterio để xác định vị trí địa lý của raster dựa trên tọa độ góc trên bên trái và kích thước pixel.
    5. Xác định kiểu dữ liệu cho tệp TIFF đầu ra dựa trên kiểu dữ liệu của mảng đầu vào (float32 hoặc uint16).
    6. Mở một tệp TIFF mới ở chế độ ghi bằng thư viện rasterio, chỉ định các thuộc tính như trình điều khiển, kích thước, số lượng kênh (count=1), kiểu dữ liệu, hệ tọa độ và transform.
    7. Ghi mảng NumPy đầu vào vào tệp TIFF đã mở như là kênh (band) đầu tiên.

    Args:
        h_0_BC (numpy.ndarray): Một mảng NumPy 2D chứa dữ liệu cần lưu.
        generation (int): Một số nguyên đại diện cho số thế hệ, được sử dụng trong tên tệp đầu ra.
        pixel_size (float, tùy chọn): Kích thước của mỗi pixel trong tệp TIFF đầu ra. Mặc định là 1.
        top_left (tuple, tùy chọn): Một tuple đại diện cho tọa độ (x, y) của góc trên cùng bên trái của raster. Mặc định là (0,0).
        crs (str, tùy chọn): Hệ tọa độ (CRS) của tệp TIFF đầu ra. Mặc định là "EPSG:4326".

    Raises:
        ValueError: Nếu mảng đầu vào `h_0_BC` không có chính xác hai chiều.

    Returns:
        None
"""

import numpy as np
import rasterio
from rasterio.transform import from_origin

def save_to_tiff(h_0_BC, generation, pixel_size = 1, top_left = (0,0), crs="EPSG:4326"):
    if len(h_0_BC.shape) != 2:
        raise ValueError("Input error!")
    output_file = f'E:/tiffrain/Generation{generation}.tiff'
    height, width = h_0_BC.shape
    ransform = from_origin(top_left[0], top_left[1], pixel_size, pixel_size)
    dtype = rasterio.float32 if h_0_BC.dtype == np.float32 else rasterio.uint16
    with rasterio.open(
        output_file,
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=1,  
        dtype=dtype,
        crs=crs,
        transform=ransform,
    ) as dst:
        dst.write(h_0_BC, 1)  

