# Tu Vi Horoscope MCP Server

This is a Model Context Protocol (MCP) server developed in Python that calculates and manages Vietnamese "Tử Vi" horoscope charts. It is optimized to output clean, structured JSON data that LLM agents can easily read, interpret, and explain to users.

---

## English Documentation

### Features
- **Horoscope Generation:** Converts Solar or Lunar birth dates and times into a full Tử Vi chart (Thiên Bàn and Địa Bàn with 12 houses and over 100 stars).
- **Vận Hạn (Transit Analysis):** Computes transit stars (Lưu tinh) and maps the active 10-year period (Đại Hạn), yearly period (Tiểu Hạn), and monthly period (Nguyệt Hạn) for any target year and month (e.g., 2026).
- **Local Persistence:** Save, retrieve, list, and delete horoscope charts from a local SQLite database (`tuvi_horoscopes.db`).
- **Flexible Hour Mapping:** Automatically maps calendar hours (e.g., "14:30") or string names (e.g., "Ngọ", "Tý") to the correct Earthly Branch hour index.
- **Local Inlining (Independent):** Includes the core `ansaotuvi` calculation logic internally with custom Tuần/Triệt double-cung fixes.

### Installation & Setup (Recommended)

To install and deploy the server cleanly in an isolated environment, we recommend setting up a virtual environment (`.venv`) and installing the package in editable mode (`-e .`). This registers `tuvi_mcp` inside the environment, allowing it to be executed from any working directory (essential for integrations like Claude Desktop):

1. **Create Virtual Environment:**
   ```bash
   python3 -m venv .venv
   ```

2. **Install Package & Dependencies:**
   ```bash
   .venv/bin/pip install --upgrade pip
   .venv/bin/pip install -e .
   ```

### How to Run

#### 1. Stdio Mode (Default for Claude Desktop & Cursor)
```bash
.venv/bin/tuvi-mcp
```

#### 2. Streamable HTTP Mode (For Remote & Cloud Deployments)
To run the server over HTTP (runs on port `1850` by default):
```bash
.venv/bin/tuvi-mcp --http
```
Override host and port:
```bash
.venv/bin/tuvi-mcp --http --host 127.0.0.1 --port 1850
```

### Tool API Reference

#### 1. `generate_horoscope`
Generates a full Tử Vi chart.
* **Arguments:**
  - `name` (string): Person's name (default: "Khách").
  - `day` (integer): Day of birth (1-31).
  - `month` (integer): Month of birth (1-12).
  - `year` (integer): Year of birth.
  - `hour_val` (string): Hour of birth (e.g., "14:30", "Ngọ", "Tý").
  - `gender_val` (string): Gender ("Nam" or "Nữ").
  - `is_solar` (boolean): True for Solar, False for Lunar (default: True).

#### 2. `get_van_han`
Calculates transit stars and active cungs (yearly, monthly, and 10-year periods) for a target year/month.
* **Arguments:**
  - `name`, `day`, `month`, `year`, `hour_val`, `gender_val`, `is_solar` (same as above).
  - `current_year` (integer): Target year to inspect (default: current year).
  - `current_month` (integer): Lunar month to inspect (1-12, default: 1).

#### 3. `save_horoscope`
Saves birth details to the SQLite database.
* **Arguments:**
  - `name`, `day`, `month`, `year`, `hour_val`, `gender_val`, `is_solar`, `notes` (string, optional).

#### 4. `list_saved_horoscopes`
Lists all saved records from the database.

#### 5. `get_saved_horoscope`
Retrieves a saved record and generates its chart.
* **Arguments:**
  - `horoscope_id` (integer, optional)
  - `name` (string, optional)

#### 6. `delete_saved_horoscope`
Deletes a record from the database.
* **Arguments:**
  - `horoscope_id` (integer)

### Client Integration Examples

#### Claude Desktop Configuration
Add the following to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "tuvi-horoscope": {
      "command": "/path/to/TuViMCP/.venv/bin/tuvi-mcp",
      "args": []
    }
  }
}
```

#### Cursor Integration
Go to Settings -> Features -> MCP, click "+ Add New MCP Server":
- **Name:** TuViMCP
- **Type:** command
- **Command:** `/path/to/TuViMCP/.venv/bin/tuvi-mcp`

---
---

# Máy chủ MCP Luận giải Lá số Tử Vi

Đây là máy chủ giao thức bối cảnh mô hình (MCP) được phát triển bằng Python giúp tính toán và quản lý lá số Tử Vi Việt Nam. Đầu ra được tối ưu hóa thành định dạng JSON cấu trúc gọn gàng giúp các mô hình AI dễ dàng đọc, phân tích và luận giải cho người dùng.

---

## Tài liệu Tiếng Việt

### Các Tính Năng
- **Lập Lá Số Tử Vi:** Đổi ngày giờ sinh Dương lịch hoặc Âm lịch sang bản đồ lá số đầy đủ (Thiên Bàn và Địa Bàn với 12 cung cùng hơn 100 chòm sao).
- **Xem Vận Hạn:** Tính toán các sao lưu hàng năm (Lưu Thái Tuế, Lưu Lộc Tồn, v.v.) và định vị các cung hạn: Đại Hạn (10 năm), Tiểu Hạn (năm hiện tại), và Nguyệt Hạn (tháng hiện tại) cho năm xem bất kỳ (ví dụ: 2026).
- **Lưu Trữ Cục Bộ:** Lưu, tải, liệt kê và xóa dữ liệu lá số sinh trực tiếp thông qua cơ sở dữ liệu SQLite cục bộ (`tuvi_horoscopes.db`).
- **Tự Động Đổi Giờ:** Tự động quy đổi các mốc giờ đồng hồ (ví dụ: "14:30") hoặc tên giờ truyền thống (ví dụ: "Ngọ", "Tý") sang Địa Chi giờ chính xác.
- **Nhúng Thư Viện Cục Bộ:** Tích hợp trực tiếp thư viện tính toán Tử Vi gốc và đã vá lỗi hiển thị Tuần/Triệt bao phủ cả 2 cung.

### Cài Đặt & Thiết Lập (Khuyên dùng)

Để cài đặt và triển khai máy chủ một cách sạch sẽ trong môi trường độc lập, chúng tôi khuyên bạn nên thiết lập môi trường ảo (`.venv`) và cài đặt gói ở chế độ có thể chỉnh sửa (`-e .`). Cách này giúp đăng ký gói `tuvi_mcp` vào môi trường ảo, cho phép thực thi chương trình từ bất kỳ thư mục làm việc nào (quan trọng đối với các tích hợp như Claude Desktop):

1. **Tạo môi trường ảo:**
   ```bash
   python3 -m venv .venv
   ```

2. **Cài đặt Gói & Thư viện phụ thuộc:**
   ```bash
   .venv/bin/pip install --upgrade pip
   .venv/bin/pip install -e .
   ```

### Cách Khởi Chạy

#### 1. Chế độ Stdio (Mặc định cho Claude Desktop & Cursor)
```bash
.venv/bin/tuvi-mcp
```

#### 2. Chế độ HTTP (Dành cho việc triển khai mạng/đám mây)
Khởi chạy server qua giao thức HTTP (mặc định trên cổng `1850`):
```bash
.venv/bin/tuvi-mcp --http
```
Thay đổi địa chỉ host và cổng port:
```bash
.venv/bin/tuvi-mcp --http --host 127.0.0.1 --port 1850
```

### Danh sách Công cụ MCP (API Reference)

#### 1. `generate_horoscope`
Khởi tạo lá số Tử Vi chi tiết.
* **Tham số:**
  - `name` (string): Tên người xem (mặc định: "Khách").
  - `day` (integer): Ngày sinh (1-31).
  - `month` (integer): Tháng sinh (1-12).
  - `year` (integer): Năm sinh.
  - `hour_val` (string): Giờ sinh (ví dụ: "14:30", "Ngọ").
  - `gender_val` (string): Giới tính ("Nam" hoặc "Nữ").
  - `is_solar` (boolean): True nếu là Dương lịch, False nếu Âm lịch (mặc định: True).

#### 2. `get_van_han`
Phân tích sao lưu và định vị cung hạn Đại Hạn, Tiểu Hạn, Nguyệt Hạn cho tháng/năm cần xem.
* **Tham số:**
  - `name`, `day`, `month`, `year`, `hour_val`, `gender_val`, `is_solar` (tương tự như trên).
  - `current_year` (integer): Năm muốn xem hạn (mặc định: năm hiện tại).
  - `current_month` (integer): Tháng âm lịch muốn xem hạn (1-12, mặc định: 1).

#### 3. `save_horoscope`
Lưu thông tin ngày sinh vào cơ sở dữ liệu.
* **Tham số:**
  - `name`, `day`, `month`, `year`, `hour_val`, `gender_val`, `is_solar`, `notes` (string, tùy chọn).

#### 4. `list_saved_horoscopes`
Liệt kê toàn bộ danh sách lá số đã lưu.

#### 5. `get_saved_horoscope`
Lấy dữ liệu đã lưu và xuất lá số.
* **Tham số:**
  - `horoscope_id` (integer, tùy chọn)
  - `name` (string, tùy chọn)

#### 6. `delete_saved_horoscope`
Xóa dữ liệu lá số đã lưu.
* **Tham số:**
  - `horoscope_id` (integer)

### Tích Hợp Client

#### Cấu hình cho Claude Desktop
Thêm đoạn cấu hình sau vào file `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tuvi-horoscope": {
      "command": "/path/to/TuViMCP/.venv/bin/tuvi-mcp",
      "args": []
    }
  }
}
```

#### Tích hợp cho Cursor
Truy cập Settings -> Features -> MCP, click "+ Add New MCP Server":
- **Name:** TuViMCP
- **Type:** command
- **Command:** `/path/to/TuViMCP/.venv/bin/tuvi-mcp`
