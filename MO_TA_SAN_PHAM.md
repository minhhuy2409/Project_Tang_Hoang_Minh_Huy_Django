# ManagerZone - Hệ Thống Quản Lý Đội Bóng

## MÔ TẢ SẢN PHẨM

**ManagerZone** là ứng dụng web quản lý đội bóng đá nghiệp dư (sân 5/sân 7), giúp huấn luyện viên và cầu thủ dễ dàng quản lý thông tin đội, lịch thi đấu, thống kê cá nhân và hiệu suất thi đấu.

### Đặc điểm nổi bật:
- ⚽ **Quản lý thông tin cầu thủ**: Lưu trữ hồ sơ, vị trí, số áo, phong cách chơi
- 📅 **Lịch thi đấu**: Xem trận đấu sắp tới, đăng ký tham gia
- 📊 **Thống kê tự động**: Goals, assists, rating, tỷ lệ thắng được tính tự động
- 🏆 **Quản lý trận đấu**: Admin nhập kết quả, chấm điểm, ghi nhận sự kiện
- 🎨 **Giao diện hiện đại**: Dark theme với màu sắc sống động, responsive

### Công nghệ sử dụng:
- **Backend**: Django 5.2.8 (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS (Custom Design System)
- **Font**: Inter (Google Fonts)

---

## CHỨC NĂNG CHI TIẾT

### 1️⃣ **ĐĂNG KÝ & ĐĂNG NHẬP**

**Ai sử dụng**: Tất cả người dùng

**Chức năng**:
- Đăng ký tài khoản mới (tự động được gán role "Player")
- Đăng nhập/Đăng xuất
- Bảo mật với Django Authentication

**URL**: `/signup/`, `/login/`, `/logout/`

---

### 2️⃣ **DASHBOARD (Trang Chủ)**

**Ai sử dụng**: Cầu thủ & Admin

**Chức năng**:
- Xem tổng quan thông tin đội
- Quick access đến các tính năng chính
- Hiển thị thống kê tổng hợp

**URL**: `/dashboard/`

---

### 3️⃣ **HỒ SƠ CÁ NHÂN (Profile)**

**Ai sử dụng**: Cầu thủ & Admin

**Chức năng**:
- **Upload avatar**: Tải ảnh đại diện lên
- **Chỉnh sửa thông tin**:
  - Tên cầu thủ
  - Số áo
  - Vị trí (GK, DF, MF, FW)
  - Chân thuận (Left, Right, Both)
  - Phong cách chơi (Keeping ball, Long pass, Pressing)
  - Tình trạng sức khỏe

**URL**: `/profile/`

**Giao diện**: 
- Avatar tròn ở bên trái
- Form chỉnh sửa ở bên phải
- Nút "Save Changes" để lưu

---

### 4️⃣ **LỊCH THI ĐẤU (Schedule)**

**Ai sử dụng**: Cầu thủ & Admin

**Chức năng**:
- **Xem trận đấu sắp tới**: Danh sách các trận sắp diễn ra
- **Thông tin trận đấu**:
  - Đối thủ
  - Ngày giờ
  - Địa điểm
  - Ghi chú chiến thuật
- **Trạng thái tham gia**:
  - ✅ Going (Tham gia)
  - ❌ Not Going (Không tham gia)
  - ❓ Maybe (Chưa chắc)
  - Not Registered (Chưa đăng ký)

**URL**: `/schedule/`

**Giao diện**: Card layout hiển thị từng trận đấu

---

### 5️⃣ **ĐĂNG KÝ THAM GIA TRẬN ĐẤU (Attendance)**

**Ai sử dụng**: Cầu thủ

**Chức năng**:
- Chọn trạng thái cho từng trận đấu:
  - Going
  - Not Going
  - Maybe
- Lưu tất cả trạng thái một lúc

**URL**: `/attendance/`

---

### 6️⃣ **QUẢN LÝ TRẬN ĐẤU (Match Management)** 🔐 Admin Only

**Ai sử dụng**: Admin/Huấn luyện viên

**Chức năng**:
- **Nhập tỷ số**: Update score (VD: 3-1)
- **Ghi chú chiến thuật**: Tactical notes
- **Chấm điểm cầu thủ**: 
  - Rating từ 0-10
  - Chỉ chấm những cầu thủ có status "Going"
- **Ghi nhận sự kiện**:
  - ⚽ **Goals**: Ghi bàn (player + minute)
  - 👟 **Assists**: Kiến tạo (player + minute)
- **Danh sách cầu thủ**: Xem ai tham gia, ai vắng mặt

**URL**: `/match/<id>/`

**Giao diện**:
- Cột trái: Match info, Rating table
- Cột phải: Goals & Assists events list

---

### 7️⃣ **THỐNG KÊ CÁ NHÂN (Stats)**

**Ai sử dụng**: Cầu thủ & Admin

**Chức năng**:
- **Số liệu tự động**:
  - 🎯 **Matches Played**: Số trận đã chơi
  - ⚽ **Goals Scored**: Số bàn thắng
  - 👟 **Assists**: Số kiến tạo
  - ⭐ **Average Rating**: Điểm trung bình
  - 🏆 **Win Rate**: Tỷ lệ thắng (%)
- **Thông tin cầu thủ**:
  - Position
  - Shirt Number
  - Preferred Foot
  - Playing Style

**URL**: `/stats/`

**Giao diện**: Grid cards hiển thị từng số liệu với màu sắc riêng

---

### 8️⃣ **TÍNH NĂNG TỰ ĐỘNG (Signals)**

**Cách hoạt động**: Sử dụng Django Signals để tự động cập nhật thống kê

**Khi nào chạy**:
- Khi thêm/xóa **Goal** → Tự động cập nhật `Player.goals`
- Khi thêm/xóa **Assist** → Tự động cập nhật `Player.assists`
- Khi cập nhật **Attendance.rating** → Tự động tính lại `Player.average_rating`
- Khi cập nhật **Attendance.status** → Tự động đếm `Player.matches_played`

**Lợi ích**: Admin không cần tính toán thủ công, mọi thứ được update real-time

---

### 9️⃣ **DJANGO ADMIN PANEL**

**Ai sử dụng**: Admin/Superuser

**Chức năng**:
- Quản lý toàn bộ dữ liệu:
  - Users
  - UserProfiles
  - Players
  - Matches
  - Attendance
  - GoalEvent
  - AssistEvent
- CRUD operations (Create, Read, Update, Delete)
- Bulk actions

**URL**: `/admin/`

---

## CẤU TRÚC DỮ LIỆU (Models)

### 📊 **User** (Django built-in)
- username
- password
- email

### 👤 **UserProfile**
- user (OneToOne → User)
- role (admin/player)
- avatar (ImageField)

### ⚽ **Player**
- user_profile (OneToOne → UserProfile)
- name
- shirt_number
- position (GK/DF/MF/FW)
- foot (left/right/both)
- playing_style
- average_rating (auto-calculated)
- matches_played (auto-calculated)
- goals (auto-calculated)
- assists (auto-calculated)
- health_status

### 🏟️ **Match**
- opponent
- datetime
- location
- score
- tactical_notes
- players (ManyToMany through Attendance)

### ✅ **Attendance**
- match (FK → Match)
- player (FK → Player)
- status (going/not going/maybe)
- rating (0-10)

### ⚽ **GoalEvent**
- match (FK → Match)
- player (FK → Player)
- minute

### 👟 **AssistEvent**
- match (FK → Match)
- player (FK → Player)
- minute

---

## PHÂN QUYỀN

### 🔐 **Admin**
- Truy cập tất cả chức năng
- Quản lý trận đấu
- Chấm điểm cầu thủ
- Truy cập Django Admin

### 👤 **Player**
- Xem lịch thi đấu
- Đăng ký tham gia
- Chỉnh sửa profile
- Xem thống kê cá nhân

---

## HƯỚNG DẪN SỬ DỤNG

### Đối với Admin:
1. Đăng nhập với tài khoản admin
2. Tạo trận đấu mới qua Django Admin
3. Cầu thủ đăng ký tham gia
4. Sau trận: Truy cập `/match/<id>/`
5. Nhập tỷ số, chấm điểm, ghi nhận goals/assists
6. Stats tự động cập nhật

### Đối với Cầu thủ:
1. Đăng ký tài khoản tại `/signup/`
2. Đăng nhập
3. Cập nhật profile tại `/profile/`
4. Xem lịch đấu tại `/schedule/`
5. Đăng ký tham gia tại `/attendance/`
6. Xem stats tại `/stats/`

---

## YÊU CẦU HỆ THỐNG

- Python 3.8+
- Django 5.2.8
- SQLite (hoặc PostgreSQL cho production)
- Modern web browser (Chrome, Firefox, Safari)

---

## TÍNH NĂNG NỔI BẬT

✅ **Tự động hóa**: Thống kê được tính tự động bằng Signals  
✅ **Real-time**: Dữ liệu cập nhật ngay lập tức  
✅ **Modern UI**: Giao diện đẹp, responsive, dark theme  
✅ **Dễ sử dụng**: UX đơn giản, trực quan  
✅ **Bảo mật**: Django Authentication & Authorization  

---

**Phát triển bởi**: ManagerZone Team  
**Version**: 1.0  
**Ngày cập nhật**: 30/11/2025
