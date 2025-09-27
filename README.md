# 🚛 Hệ thống quản lý vận chuyển

Hệ thống quản lý vận chuyển được xây dựng với FastAPI backend và HTML/CSS frontend, sử dụng SQLite database để lưu trữ dữ liệu.

## ✨ Tính năng chính

- 👥 **Quản lý nhân viên**: Thêm, sửa, xóa thông tin nhân viên và lương cơ bản
- 🚚 **Quản lý xe**: Quản lý thông tin xe, biển số, trọng tải và tiêu hao nhiên liệu
- 🛣️ **Quản lý tuyến**: Thiết lập tuyến đường, khoảng cách, đơn giá và phân công nhân viên
- 📅 **Ghi nhận chuyến hàng ngày**: Ghi nhận chuyến hàng hàng ngày, chi phí xăng dầu và lương chuyến
- 💰 **Tính lương cuối tháng**: Tính lương cho từng nhân viên dựa trên chuyến và lương cơ bản

## 🛠️ Công nghệ sử dụng

- **Backend**: Python FastAPI
- **Frontend**: HTML + CSS (Jinja2 templates)
- **Database**: SQLite
- **Styling**: CSS Grid, Flexbox với gradient và glassmorphism effects

## 📦 Cài đặt

1. **Clone repository**:
```bash
git clone <repository-url>
cd transport-management
```

2. **Cài đặt dependencies**:
```bash
pip install -r requirements.txt
```

3. **Chạy ứng dụng**:
```bash
python main.py
```

4. **Truy cập ứng dụng**:
Mở trình duyệt và truy cập: `http://localhost:8000`

## 📁 Cấu trúc project

```
transport-management/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── README.md              # Documentation
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Trang chủ
│   ├── employees.html    # Quản lý nhân viên
│   ├── vehicles.html     # Quản lý xe
│   ├── routes.html       # Quản lý tuyến
│   ├── daily.html        # Ghi nhận chuyến hàng ngày
│   └── salary.html       # Tính lương
├── static/               # Static files
│   └── style.css        # CSS styling
└── transport.db         # SQLite database (tự động tạo)
```

## 🗄️ Database Schema

### Employees (Nhân viên)
- `id`: Primary key
- `name`: Họ tên nhân viên
- `phone`: Số điện thoại
- `base_salary`: Lương cơ bản
- `created_at`: Ngày tạo

### Vehicles (Xe)
- `id`: Primary key
- `license_plate`: Biển số xe
- `capacity`: Trọng tải (kg)
- `fuel_consumption`: Tiêu hao nhiên liệu (lít/100km)
- `created_at`: Ngày tạo

### Routes (Tuyến đường)
- `id`: Primary key
- `route_code`: Mã tuyến (VD: NA_002)
- `route_name`: Tên tuyến
- `distance`: Khoảng cách (km)
- `unit_price`: Đơn giá (VNĐ/km)
- `employee_id`: ID nhân viên phụ trách
- `vehicle_id`: ID xe phụ trách
- `is_active`: Trạng thái hoạt động
- `created_at`: Ngày tạo

### DailyRoutes (Chuyến hàng ngày)
- `id`: Primary key
- `route_id`: ID tuyến
- `date`: Ngày chạy
- `fuel_cost`: Chi phí xăng dầu (VNĐ)
- `fuel_quantity`: Số lít dầu
- `fuel_price`: Giá dầu (VNĐ/lít)
- `trip_salary`: Lương chuyến (VNĐ)
- `notes`: Ghi chú
- `created_at`: Ngày tạo

## 💰 Công thức tính lương

```
Tổng lương = Lương cơ bản + Tổng lương chuyến
```

- **Lương cơ bản**: Mức lương cố định hàng tháng
- **Lương chuyến**: Tiền thưởng cho mỗi chuyến hoàn thành
- **Chi phí xăng**: Tổng chi phí nhiên liệu (không trừ vào lương)

## 🎯 Hướng dẫn sử dụng

1. **Thêm nhân viên**: Vào mục "Nhân viên" để thêm thông tin nhân viên và lương cơ bản
2. **Thêm xe**: Vào mục "Xe" để thêm thông tin xe và biển số
3. **Thiết lập tuyến**: Vào mục "Tuyến đường" để tạo tuyến và phân công nhân viên
4. **Ghi nhận chuyến**: Mỗi ngày vào mục "Chuyến hàng ngày" để ghi nhận chuyến đã chạy
5. **Tính lương**: Cuối tháng vào mục "Tính lương" để xem bảng lương chi tiết

## 🔧 API Endpoints

- `GET /`: Trang chủ
- `GET /employees`: Danh sách nhân viên
- `POST /employees/add`: Thêm nhân viên
- `GET /vehicles`: Danh sách xe
- `POST /vehicles/add`: Thêm xe
- `GET /routes`: Danh sách tuyến
- `POST /routes/add`: Thêm tuyến
- `GET /daily`: Chuyến hàng ngày
- `POST /daily/add`: Ghi nhận chuyến
- `GET /salary`: Tính lương

## 📱 Responsive Design

Ứng dụng được thiết kế responsive, hoạt động tốt trên:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)

## 🎨 UI/UX Features

- **Modern Design**: Sử dụng gradient và glassmorphism effects
- **Responsive Layout**: CSS Grid và Flexbox
- **Interactive Elements**: Hover effects và smooth transitions
- **Color Coding**: Mã màu cho các trạng thái khác nhau
- **Statistics Cards**: Hiển thị thống kê tổng quan
- **Form Validation**: Validation phía client và server

## 🚀 Deployment

Để deploy lên production:

1. **Cài đặt production dependencies**:
```bash
pip install gunicorn
```

2. **Chạy với Gunicorn**:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

3. **Cấu hình reverse proxy** (Nginx):
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.
