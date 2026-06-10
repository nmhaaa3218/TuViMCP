# Tu Vi Horoscope MCP Server

[![CI](https://github.com/nmhaaa3218/TuViMCP/actions/workflows/ci.yml/badge.svg)](https://github.com/nmhaaa3218/TuViMCP/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is a Model Context Protocol (MCP) server developed in Python that calculates and manages Vietnamese "Tử Vi" horoscope charts. It is optimized to output clean, structured JSON data that LLM agents can easily read, interpret, and explain to users.

---

## English Documentation

### Quick Links
- [Contributing Guidelines](CONTRIBUTING.md)
- [Changelog / Release History](CHANGELOG.md)
- [Example JSON Outputs & Scripts](examples/)


### Features
- **Horoscope Generation:** Converts Solar or Lunar birth dates and times into a full Tử Vi chart (Thiên Bàn and Địa Bàn with 12 houses and over 100 stars).
- **Vận Hạn (Transit Analysis):** Computes transit stars (Lưu tinh) and maps the active 10-year period (Đại Hạn), yearly period (Tiểu Hạn), and monthly period (Nguyệt Hạn) for any target year and month (e.g., 2026).
- **Local Persistence:** Save, retrieve, list, and delete horoscope charts from a local SQLite database (`tuvi_horoscopes.db`).
- **Flexible Hour Mapping:** Automatically maps calendar hours (e.g., "14:30") or string names (e.g., "Ngọ", "Tý") to the correct Earthly Branch hour index.
- **Local Inlining (Independent):** Includes the core `ansaotuvi` calculation logic internally with custom Tuần/Triệt double-cung fixes.

### Known Limitations & Assumptions
- **Timezone Assumption:** Calculations default to the Vietnamese local timezone (GMT+7). Birth details outside this timezone must be converted beforehand.
- **Calendar Boundaries:** The core calculations are stable for modern birth years, but traditional leap months (tháng nhuận) follow standard Vietnamese lunar calendar mappings (Hoang Nam Dia methodology) which might vary in historical or remote future years.
- **Calculations School (Phái):** Star distributions follow standard consensus calculations. Customizable star weight/distributions (different schools like Nam Phái vs. Bắc Phái vs. custom configurations) are not supported.


### Installation & Setup (Recommended)

To install and deploy the server cleanly in an isolated environment, we recommend setting up a virtual environment (`.venv`) and installing the package in editable mode (`-e .`). This registers `tuvi_mcp` inside the environment, allowing it to be executed from any working directory (essential for integrations like Claude Desktop):

1. **Create Virtual Environment:**
   ```bash
   python3 -m venv .venv
   ```

2. **Install Package & Dependencies:**
   ```bash
   .venv/bin/pip install --upgrade pip
   .venv/bin/pip install -e ".[test]"
   ```

3. **Running Tests:**
   Ensure your development setup works by running the test suite with `pytest`:
   ```bash
   .venv/bin/pytest
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

### Example Tool Call & JSON Outputs

To illustrate the structured responses, here is an example of what the server outputs when calling the core tools.

#### 1. Horoscope Generation Output Summary (`generate_horoscope`)

When calling `generate_horoscope(name="Nguyễn Văn A", day=10, month=6, year=1995, hour_val="14:30", gender_val="Nam", is_solar=true)`, the server outputs a structured JSON response containing `thien_ban` (person information) and `dia_ban` (the list of 12 houses and their stars).

**Response Snippet:**
```json
{
  "thien_ban": {
    "ten": "Nguyễn Văn A",
    "gioi_tinh": "Nam",
    "ngay_duong": "10/6/1995",
    "ngay_am": "13/5/1995",
    "gio_sinh": "Đinh Mùi",
    "chi_gio_sinh": "Mùi",
    "am_duong_menh": "Âm dương thuận lý",
    "hanh_cuc": 5,
    "ten_cuc": "Thổ ngũ Cục",
    "menh_chu": "Cự môn",
    "than_chu": "Thiên tướng",
    "ban_menh": "SƠN ÐẦU HỎA"
  },
  "dia_ban": [
    {
      "cung_so": 1,
      "cung_ten": "Mậu Tý",
      "hanh_cung": "Thủy",
      "cung_chu": "Phụ mẫu",
      "dai_han": 115,
      "tieu_han": "Tuất",
      "sao": [
        {
          "id": 9,
          "name": "Tham lang",
          "element": "T",
          "type": 1,
          "attribute": "Hãm địa"
        }
      ]
    }
    // ... 11 other cungs (houses)
  ]
}
```

*For the complete output, see [examples/sample_horoscope_output.json](examples/sample_horoscope_output.json).*

#### 2. Vận Hạn Analysis Output Summary (`get_van_han`)

When calling `get_van_han(...)` for a target year/month, it tracks yearly transit stars (sao lưu) and flags the active houses:

**Response Snippet:**
```json
{
  "person_details": {
    "name": "Nguyễn Văn A",
    "element": "H",
    "destiny_cuc": "Thổ ngũ Cục"
  },
  "target_period": {
    "current_year": 2026,
    "current_year_can_chi": "Bính Ngọ",
    "current_month_lunar": 5,
    "current_age": 32
  },
  "transit_stars": [
    {"name": "Lưu Thái Tuế", "cung_so": 7, "chi": "Ngọ"},
    {"name": "Lưu Lộc Tồn", "cung_so": 9, "chi": "Thân"}
    // ... other transit stars
  ],
  "dai_han": {
    "cung_so": 10,
    "cung_chu": "Tử tức",
    "dai_han": 35,
    "transit_stars": []
  },
  "tieu_han": {
    "cung_so": 7,
    "cung_chu": "Tật ách",
    "tieu_han": "Ngọ",
    "transit_stars": ["Lưu Thái Tuế"]
  }
}
```

*For the complete output, see [examples/sample_van_han_output.json](examples/sample_van_han_output.json).*

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

Đây là máy chủ Model Context Protocol (MCP) được phát triển bằng Python, dùng để lập và quản lý lá số Tử Vi theo hệ Việt Nam. Kết quả được chuẩn hóa dưới dạng JSON sạch, có cấu trúc rõ ràng, giúp các LLM agent dễ dàng đọc, phân tích và diễn giải lại cho người dùng.

---

## Tài liệu Tiếng Việt

### Đường Dẫn Nhanh
- [Hướng dẫn Đóng góp](CONTRIBUTING.md)
- [Lịch sử Thay đổi](CHANGELOG.md)
- [Thư mục Output JSON mẫu & Mã nguồn ví dụ](examples/)

### Tính năng chính

* **Lập lá số Tử Vi:** Hỗ trợ chuyển đổi ngày giờ sinh Dương lịch hoặc Âm lịch thành lá số Tử Vi đầy đủ, bao gồm Thiên Bàn, Địa Bàn, 12 cung và hơn 100 sao.

* **Xem Vận Hạn:** Tính toán các sao lưu động như Lưu Thái Tuế, Lưu Lộc Tồn, v.v., đồng thời xác định các cung hạn đang kích hoạt gồm Đại Hạn 10 năm, Tiểu Hạn theo năm và Nguyệt Hạn theo tháng cho bất kỳ năm/tháng cần xem nào, ví dụ năm 2026.

* **Lưu trữ cục bộ:** Hỗ trợ lưu, truy xuất, liệt kê và xóa thông tin lá số thông qua cơ sở dữ liệu SQLite cục bộ (`tuvi_horoscopes.db`).

* **Tự động quy đổi giờ sinh:** Có thể tự động chuyển đổi giờ theo đồng hồ, ví dụ `"14:30"`, hoặc tên giờ truyền thống, ví dụ `"Ngọ"`, `"Tý"`, sang đúng chỉ số Địa Chi tương ứng.

* **Tích hợp logic tính toán nội bộ:** Bao gồm sẵn phần lõi tính toán từ `ansaotuvi`, đồng thời bổ sung các chỉnh sửa riêng cho trường hợp Tuần/Triệt bao phủ hai cung.

### Hạn chế hiện tại & Giả định
- **Giả định múi giờ:** Mặc định tính toán theo múi giờ Việt Nam (GMT+7). Mọi thông tin giờ sinh ở múi giờ khác cần được quy đổi về GMT+7 trước khi truyền vào.
- **Giới hạn lịch pháp:** Các phép tính toán âm dương lịch ổn định và chính xác cao với các năm sinh thời hiện đại. Thuật toán chuyển đổi lịch âm dựa trên phương pháp của Hoàng Nam Địa (HND), có thể có sai lệch nhỏ ở một số năm nhuận quá khứ xa hoặc tương lai xa.
- **Hệ phái an sao:** Thuật toán an sao theo quy chuẩn chung phổ biến tại Việt Nam. Dự án hiện chưa hỗ trợ cấu hình tùy biến trọng số sao hoặc các cách an sao khác nhau của các hệ phái khác (như Nam phái vs Bắc phái vs tự chọn).

---

### Cài đặt & Thiết lập khuyến nghị

Để cài đặt và triển khai máy chủ trong một môi trường sạch, độc lập, nên tạo môi trường ảo (`.venv`) và cài đặt package ở chế độ editable (`-e .`). Cách này sẽ đăng ký `tuvi_mcp` trực tiếp trong môi trường ảo, giúp bạn có thể chạy server từ bất kỳ thư mục làm việc nào. Điều này đặc biệt hữu ích khi tích hợp với các client như Claude Desktop.

1. **Tạo môi trường ảo:**
   ```bash
   python3 -m venv .venv
   ```

2. **Cài đặt package và các thư viện phụ thuộc:**
   ```bash
   .venv/bin/pip install --upgrade pip
   .venv/bin/pip install -e ".[test]"
   ```

3. **Chạy kiểm thử (Unit Tests):**
   Đảm bảo rằng môi trường phát triển hoạt động chính xác bằng cách chạy bộ kiểm thử tự động với `pytest`:
   ```bash
   .venv/bin/pytest
   ```

---

### Cách khởi chạy

#### 1. Chế độ Stdio

Đây là chế độ mặc định, phù hợp để tích hợp với Claude Desktop và Cursor.
```bash
.venv/bin/tuvi-mcp
```

#### 2. Chế độ Streamable HTTP

Dùng khi muốn triển khai server qua HTTP, phù hợp cho môi trường remote hoặc cloud. Mặc định server chạy trên cổng `1850`.
```bash
.venv/bin/tuvi-mcp --http
```

Có thể tùy chỉnh host và port như sau:
```bash
.venv/bin/tuvi-mcp --http --host 127.0.0.1 --port 1850
```

---

### Danh sách công cụ MCP

#### 1. `generate_horoscope`

Tạo lá số Tử Vi đầy đủ từ thông tin ngày giờ sinh.

* **Tham số:**
  * `name` (string): Tên người xem, mặc định là `"Khách"`.
  * `day` (integer): Ngày sinh, từ 1 đến 31.
  * `month` (integer): Tháng sinh, từ 1 đến 12.
  * `year` (integer): Năm sinh.
  * `hour_val` (string): Giờ sinh, ví dụ `"14:30"`, `"Ngọ"`, `"Tý"`.
  * `gender_val` (string): Giới tính, nhận giá trị `"Nam"` hoặc `"Nữ"`.
  * `is_solar` (boolean): `True` nếu dùng Dương lịch, `False` nếu dùng Âm lịch. Mặc định là `True`.

---

#### 2. `get_van_han`

Tính toán sao lưu động và xác định các cung hạn đang kích hoạt, bao gồm Đại Hạn, Tiểu Hạn và Nguyệt Hạn cho tháng/năm cần xem.

* **Tham số:**
  * `name`, `day`, `month`, `year`, `hour_val`, `gender_val`, `is_solar`: giống như trong `generate_horoscope`.
  * `current_year` (integer): Năm cần xem hạn. Mặc định là năm hiện tại.
  * `current_month` (integer): Tháng âm lịch cần xem hạn, từ 1 đến 12. Mặc định là 1.

---

#### 3. `save_horoscope`

Lưu thông tin ngày giờ sinh vào cơ sở dữ liệu SQLite cục bộ.

* **Tham số:**
  * `name`, `day`, `month`, `year`, `hour_val`, `gender_val`, `is_solar`, `notes` (string, tùy chọn).

---

#### 4. `list_saved_horoscopes`

Liệt kê toàn bộ lá số đã được lưu trong cơ sở dữ liệu.

---

#### 5. `get_saved_horoscope`

Truy xuất một bản ghi đã lưu và tạo lại lá số tương ứng.

* **Tham số:**
  * `horoscope_id` (integer, tùy chọn)
  * `name` (string, tùy chọn)

---

#### 6. `delete_saved_horoscope`

Xóa một bản ghi lá số đã lưu khỏi cơ sở dữ liệu.

* **Tham số:**
  * `horoscope_id` (integer): ID của lá số cần xóa.

---

### Ví dụ gọi Tool & Đầu ra JSON mẫu

Dưới đây là cấu trúc dữ liệu JSON thực tế do máy chủ MCP trả về để minh họa tính rõ ràng và gọn gàng của định dạng đầu ra.

#### 1. Kết quả Lập Lá Số (`generate_horoscope`)

Khi gọi `generate_horoscope(name="Nguyễn Văn A", day=10, month=6, year=1995, hour_val="14:30", gender_val="Nam", is_solar=true)`, đầu ra trả về đối tượng JSON gồm thông tin Thiên Bàn (`thien_ban`) và danh sách 12 cung Địa Bàn (`dia_ban`).

**Đoạn trích đầu ra:**
```json
{
  "thien_ban": {
    "ten": "Nguyễn Văn A",
    "gioi_tinh": "Nam",
    "ngay_duong": "10/6/1995",
    "ngay_am": "13/5/1995",
    "gio_sinh": "Đinh Mùi",
    "chi_gio_sinh": "Mùi",
    "am_duong_menh": "Âm dương thuận lý",
    "hanh_cuc": 5,
    "ten_cuc": "Thổ ngũ Cục",
    "menh_chu": "Cự môn",
    "than_chu": "Thiên tướng",
    "ban_menh": "SƠN ÐẦU HỎA"
  },
  "dia_ban": [
    {
      "cung_so": 1,
      "cung_ten": "Mậu Tý",
      "hanh_cung": "Thủy",
      "cung_chu": "Phụ mẫu",
      "dai_han": 115,
      "tieu_han": "Tuất",
      "sao": [
        {
          "id": 9,
          "name": "Tham lang",
          "element": "T",
          "type": 1,
          "attribute": "Hãm địa"
        }
      ]
    }
    // ... 11 cung tiếp theo
  ]
}
```

*Để xem dữ liệu đầy đủ, vui lòng tham khảo file mẫu tại [examples/sample_horoscope_output.json](examples/sample_horoscope_output.json).*

#### 2. Kết quả Phân Tích Vận Hạn (`get_van_han`)

Khi gọi `get_van_han(...)` cho một năm/tháng cụ thể, hệ thống tính toán vị trí các sao lưu và đánh dấu các cung hạn đang kích hoạt:

**Đoạn trích đầu ra:**
```json
{
  "person_details": {
    "name": "Nguyễn Văn A",
    "element": "H",
    "destiny_cuc": "Thổ ngũ Cục"
  },
  "target_period": {
    "current_year": 2026,
    "current_year_can_chi": "Bính Ngọ",
    "current_month_lunar": 5,
    "current_age": 32
  },
  "transit_stars": [
    {"name": "Lưu Thái Tuế", "cung_so": 7, "chi": "Ngọ"},
    {"name": "Lưu Lộc Tồn", "cung_so": 9, "chi": "Thân"}
    // ... các lưu tinh khác
  ],
  "dai_han": {
    "cung_so": 10,
    "cung_chu": "Tử tức",
    "dai_han": 35,
    "transit_stars": []
  },
  "tieu_han": {
    "cung_so": 7,
    "cung_chu": "Tật ách",
    "tieu_han": "Ngọ",
    "transit_stars": ["Lưu Thái Tuế"]
  }
}
```

*Để xem dữ liệu đầy đủ, vui lòng tham khảo file mẫu tại [examples/sample_van_han_output.json](examples/sample_van_han_output.json).*

---

### Ví dụ tích hợp với client

#### Cấu hình Claude Desktop

Thêm cấu hình sau vào file `claude_desktop_config.json`:

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

#### Tích hợp với Cursor

Vào Settings -> Features -> MCP, sau đó chọn "+ Add New MCP Server":

* **Name:** TuViMCP
* **Type:** command
* **Command:** `/path/to/TuViMCP/.venv/bin/tuvi-mcp`

