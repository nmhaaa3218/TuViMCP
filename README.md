# Tu Vi Horoscope MCP Server

[![CI](https://github.com/nmhaaa3218/TuViMCP/actions/workflows/ci.yml/badge.svg)](https://github.com/nmhaaa3218/TuViMCP/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/tuvi-mcp-server)](https://pypi.org/project/tuvi-mcp-server/)
[![Documentation Status](https://readthedocs.org/projects/tuvi-mcp-server/badge/?version=latest)](https://tuvi-mcp-server.readthedocs.io/en/latest/)

[![TuViMCP MCP server](https://glama.ai/mcp/servers/nmhaaa3218/TuViMCP/badges/card.svg)](https://glama.ai/mcp/servers/nmhaaa3218/TuViMCP)

This is a Model Context Protocol (MCP) server developed in Python that calculates and manages Vietnamese "Tử Vi" horoscope charts. It is optimized to output clean, structured JSON data that LLM agents can easily read, interpret, and explain to users.

![TuViMCP Demo](assets/demo.gif)

---

## English Documentation

### Quick Links
- [Full Documentation](https://tuvi-mcp-server.readthedocs.io/en/latest/)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Changelog / Release History](CHANGELOG.md)
- [Example JSON Outputs & Scripts](examples/)


### Features
- **Horoscope Generation:** Converts Solar or Lunar birth dates and times into a full Tử Vi chart (Thiên Bàn and Địa Bàn with 12 houses and over 100 stars).
- **51 Cách Cục Evaluation Engine:** Automatically recognizes all 51 traditional astrological formations (51 Cách Cục Trung Châu Phái) during chart generation, returning matched patterns with descriptions, poems (Cổ Ca), commentary (Bình Chú), and pros/cons (Ưu/Khuyết điểm).
- **High-Quality Image Rendering:** Generates beautiful, print-ready chart images with element-based colored text (Green for Wood, Red for Fire, Yellow for Earth, Gray for Metal, Blue for Water), custom badge boxes for Tuần & Triệt, and geometric connecting lines highlighting the Mệnh and Thân relationship.
- **Vận Hạn (Transit Analysis):** Computes transit stars (Lưu tinh) and maps the active 10-year period (Đại Hạn), yearly period (Tiểu Hạn), monthly period (Nguyệt Hạn), and daily period (Nhật Hạn) for any target year, month, and day (e.g., 2026).
- **Auspicious Date & Time Checker:** Evaluates Hoàng Đạo/Hắc Đạo, 12 Trực, 28 Tú, Tiết Khí, travel directions, and auspicious hours for any calendar date.
- **Local Persistence (Python Library):** Includes built-in SQLite database utilities (`tuvi_mcp.database`) for Python library consumers to save, retrieve, list, and delete horoscope profiles. (MCP tools are stateless and do not require a database.)
- **Flexible Hour Mapping:** Automatically maps calendar hours (e.g., "14:30") or string names (e.g., "Ngọ", "Tý") to the correct Earthly Branch hour index.
- **Local Inlining (Independent):** Includes the core `ansaotuvi` calculation logic internally with custom Tuần/Triệt double-cung fixes.

### Python Library API

Beyond the MCP server, `tuvi-mcp-server` ships a typed, ergonomic Python API for direct use in scripts, notebooks, or web backends:

```python
from tuvi_mcp import Horoscope, BirthInfo, Gender, Calendar

# Construct a horoscope handle from birth details (flexible hour / gender / calendar inputs)
h = Horoscope.from_birth(
    name="Nguyễn Văn A",
    year=1995, month=6, day=10,
    hour="14:30",          # also accepts "Ngọ", 14, or 7 (branch index)
    gender="Nam",          # also accepts "male", 1, True, or Gender.MALE
    calendar="solar",      # also accepts Calendar.SOLAR
)

# Base birth chart
chart = h.chart()
print(chart.thien_ban["can_nam"], chart.thien_ban["chi_nam"])
print(len(chart.dia_ban), "cungs")

# Vận Hạn for a target Lunar year/month/day
van_han = h.transit(year=2026, month=5, day=15)
print(van_han["target_period"]["current_year_can_chi"])
print(van_han["nhat_han"])

# Auspicious day evaluation
auspicious = h.auspicious(day=27, month=7, year=2026)

# Render chart as PNG
path = h.render_chart(chart, year=2026)
```

The same library is what the MCP tools wrap, so behavior is identical whether you call `Horoscope.from_birth(...).chart()` or invoke the `generate_horoscope` tool from an MCP client.

```python
from tuvi_mcp import AuspiciousResult, TransitResult

# All results support attribute access + to_dict() for JSON serialization
chart = h.chart()
print(chart.thien_ban["can_nam"], chart.thien_ban["chi_nam"])
json_data = chart.to_dict()  # ← JSON-serializable dict

# Transit (Vận Hạn) and Auspicious results are also typed objects
van_han: TransitResult = h.transit(year=2026, month=5)
auspicious: AuspiciousResult = h.auspicious(day=27, month=7, year=2026)

# SQLite database — save, list, retrieve profiles
from tuvi_mcp.database import init_db, save_horoscope, list_saved_horoscopes, get_saved_horoscope_by_name

init_db()  # one-time setup
id_ = save_horoscope("My Chart", 10, 6, 1995, 14, "Nam", True)
print(f"saved as id {id_}")
profiles = list_saved_horoscopes()
print(profiles)  # [{"id": 1, "name": "My Chart", ...}]
```

### Known Limitations & Assumptions
- **Timezone Assumption:** Calculations default to the Vietnamese local timezone (GMT+7). Birth details outside this timezone must be converted beforehand.
- **Calendar Boundaries:** The core calculations are stable for modern birth years, but traditional leap months (tháng nhuận) follow standard Vietnamese lunar calendar mappings (Hoang Nam Dia methodology) which might vary in historical or remote future years.
- **Calculations School (Phái):** Star distributions follow standard consensus calculations. Customizable star weight/distributions (different schools like Nam Phái vs. Bắc Phái vs. custom configurations) are not supported.

### Accuracy, Methodology & Tradition Disclaimer
> [!NOTE]
> **Traditional Calculations Disclaimer:** Vietnamese "Tử Vi" is a highly rich astrological methodology with various traditional schools (e.g., Nam Phái vs. Bắc Phái). Calculation parameters, star rankings, element determinations, and interpretations may differ depending on the specific lineage or school. The output generated by this tool is calculated strictly according to standard consensus computational logic and should be treated as a computational reference rather than a definitive astrological interpretation.



### Installation

You can install `tuvi-mcp-server` directly from PyPI:
```bash
pip install tuvi-mcp-server
```

### Development & Contribution Setup

If you want to contribute to the package or run unit tests, set up a local development environment:

1. **Create Virtual Environment:**
   ```bash
   python3 -m venv .venv
   ```

2. **Install Package in Editable Mode:**
   ```bash
   .venv/bin/pip install --upgrade pip
   .venv/bin/pip install -e ".[test]"
   ```

3. **Running Tests:**
   Verify your local setup by running the test suite:
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

All tools run locally inside the MCP environment. They require no external authentication or network rate limiting.

#### 1. `generate_horoscope`
Generates a full Tử Vi chart from raw birth details, with optional high-quality chart image rendering.
* **Purpose & Comparison:** Use this tool to compute and inspect an astrological birth chart from scratch for arbitrary birth details.
* **Side Effects:** If `generate_image` is `True`, renders a PNG file to a temporary location on the local filesystem and returns its path.
* **Arguments:**
  - `name` (string): Person's name (default: "Khách").
  - `day` (integer): Day of birth (1-31).
  - `month` (integer): Month of birth (1-12).
  - `year` (integer): Year of birth.
  - `hour_val` (string): Hour of birth (e.g., "14:30", "Ngọ", "Tý", or branch index `1-12`).
  - `gender_val` (string): Gender ("Nam" or "Nữ", case-insensitive).
  - `is_solar` (boolean): True for Solar, False for Lunar (default: True).
  - `current_year` (integer, optional): Year to inspect transit stars/Vận Hạn for (defaults to current year).
  - `generate_image` (boolean, optional): Whether to generate and return the high-quality chart image along with the chart data (default: True).
* **Return Value:** 
  - If `generate_image` is `True`, returns a list containing `[Image, chart_data]` (where `Image` is a FastMCP Image content block pointing to the generated PNG).
  - If `generate_image` is `False`, returns the raw JSON dictionary `chart_data` directly. Contains keys: `thien_ban` (demographics, pillars, element, destiny) and `dia_ban` (12 houses with stars).
  - Returns `{"error": "error_message"}` if calculations fail.

#### 2. `get_van_han`
Calculates yearly transit stars and active houses (major, yearly, monthly, and daily periods) for a target period.
* **Purpose & Comparison:** Use this tool to perform predictive transit analysis for a specific target timeframe.
* **Side Effects:** None (read-only calculation).
* **Calendar Prerequisites:** **CRITICAL:** `current_year`, `current_month`, and (if provided) `current_day` represent the **Lunar** year, month, and day. If inspecting a Solar timeframe (e.g. 'October 2026'), you **MUST** convert it using `convert_calendar` first.
* **Arguments:**
  - `name`, `day`, `month`, `year`, `hour_val`, `gender_val`, `is_solar` (same as birth parameters above).
  - `current_year` (integer): Target Lunar year to inspect (default: current year).
  - `current_month` (integer): Target Lunar month to inspect (1-12, default: 1).
  - `current_day` (integer, optional): Target Lunar day to inspect (1-30, enables Nhật Hạn).
* **Return Value:** A dictionary with keys `person_details` (Can-Chi), `target_period` (resolved age and target), `transit_stars`, `dai_han`, `tieu_han`, `nguyet_han`, and (if `current_day` given) `nhat_han`. Returns `{"error": "error_message"}` if input details are invalid.

#### 3. `convert_calendar`
Converts a date between the Solar (Dương lịch) and Lunar (Âm lịch) calendars.
* **Purpose & Comparison:** Translate dates back and forth. Crucial for converting Solar target timeframes to Lunar periods before calling `get_van_han`.
* **Side Effects:** None (mathematical calculation).
* **Arguments:**
  - `day` (integer): Day of the date to convert.
  - `month` (integer): Month of the date to convert.
  - `year` (integer): Year of the date to convert.
  - `from_solar` (boolean): `True` to convert Solar -> Lunar (default), `False` to convert Lunar -> Solar.
  - `lunar_leap` (boolean): Only used if `from_solar` is `False`. `True` if the input lunar month is a leap month (tháng nhuận).
  - `timezone` (integer): Timezone offset (default: 7 for Vietnam/ICT).
* **Return Value:**
  - Converted date parameters: `day`, `month`, `year` of target calendar, plus a `leap` boolean (specifically indicating if the Lunar month is a leap month).
  - Returns `{"error": "error_message"}` if date arguments fail validation.

#### 4. `get_auspicious_info`
Evaluates auspicious days, hours, 12 Trực, 28 Tú, Tiết Khí, and travel directions for a given date.
* **Purpose & Comparison:** Use this tool to check good/bad days for weddings, store openings, construction, travel, or any activity requiring auspicious timing. Use `generate_horoscope` for a full birth chart instead.
* **Side Effects:** None (read-only calculation).
* **Arguments:**
  - `day` (integer, optional): Day of month. Defaults to today.
  - `month` (integer, optional): Month of year. Defaults to current month.
  - `year` (integer, optional): Year (4 digits). Defaults to current year.
  - `is_solar` (boolean, optional): `True` for Solar date (default), `False` for Lunar date.
* **Return Value:** A dictionary with keys: `duong_lich`, `am_lich`, `can_chi_ngay`, `ngay_hoang_dao`, `truc_ngay`, `nhi_thap_bat_tu`, `huong_xuat_hanh`, `gio_hoang_dao`, `tiet_khi_hien_tai`, `tiet_khi_tiep_theo`.

### Example Tool Call & JSON Outputs

To illustrate the structured responses, here is an example of what the server outputs when calling the core tools.

#### 1. Horoscope Generation Output Summary (`generate_horoscope`)

When calling `generate_horoscope(name="Nguyễn Văn A", day=10, month=6, year=1995, hour_val="14:30", gender_val="Nam", is_solar=true)`, the server outputs a structured JSON response containing `thien_ban` (person information), `dia_ban` (the list of 12 houses and their stars), and `cach_cuc` (recognized astrological formations).

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
    "than_chu": "Thiên cơ",
    "ban_menh": "SƠN ÐẦU HỎA"
  },
  "cach_cuc": [
    {
      "id": 5,
      "name": "Đan Trì Quế Trì Cách",
      "category": "Cát Cục",
      "description": "Thái Dương cư Thìn Tỵ Ngọ (Đan Trì) hoặc Thái Âm cư Dậu Tuất Hợi (Quế Trì)."
    }
  ],
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

![TuViMCP Demo](assets/demo.gif)

---

## Tài liệu Tiếng Việt

### Đường Dẫn Nhanh
- [Hướng dẫn Đóng góp](CONTRIBUTING.md)
- [Lịch sử Thay đổi](CHANGELOG.md)
- [Thư mục Output JSON mẫu & Mã nguồn ví dụ](examples/)

### Tính năng chính

* **Lập lá số Tử Vi:** Hỗ trợ chuyển đổi ngày giờ sinh Dương lịch hoặc Âm lịch thành lá số Tử Vi đầy đủ, bao gồm Thiên Bàn, Địa Bàn, 12 cung và hơn 100 sao.

* **51 Cách Cục Evaluation Engine:** Tự động nhận diện toàn bộ 51 cách cục Trung Châu Phái trong quá trình lập lá số, trả về các cách cục khớp kèm Cổ Ca, Bình Chú, và Ưu/Khuyết điểm.

* **Vẽ lá số chất lượng cao:** Xuất ảnh lá số sắc nét tỷ lệ chuẩn phù hợp in ấn, tự động tô màu chữ theo ngũ hành của sao (Mộc: Xanh lá, Hỏa: Đỏ, Thổ: Vàng cam, Kim: Xám, Thủy: Xanh dương), vẽ nhãn bao nổi bật cho cung bị Tuần/Triệt, vẽ các đường nối hình học làm nổi bật tam hợp chiếu mệnh thân.

* **Xem Vận Hạn:** Tính toán các sao lưu động như Lưu Thái Tuế, Lưu Lộc Tồn, v.v., đồng thời xác định các cung hạn đang kích hoạt gồm Đại Hạn 10 năm, Tiểu Hạn theo năm và Nguyệt Hạn theo tháng cho bất kỳ năm/tháng cần xem nào, ví dụ năm 2026.

* **Xem Ngày Tốt / Giờ Hoàng Đạo:** Đánh giá Hoàng Đạo/Hắc Đạo, 12 Trực, 28 Tú, Tiết Khí, hướng xuất hành và giờ tốt cho bất kỳ ngày tháng nào.

* **Lưu trữ cục bộ (Dành cho Python Library):** Cung cấp sẵn module cơ sở dữ liệu SQLite cục bộ (`tuvi_mcp.database`) hỗ trợ lưu, truy xuất, liệt kê và xóa thông tin lá số khi tích hợp trực tiếp bằng mã Python. (Các MCP tool không dùng cơ sở dữ liệu.)

* **Tự động quy đổi giờ sinh:** Có thể tự động chuyển đổi giờ theo đồng hồ, ví dụ `"14:30"`, hoặc tên giờ truyền thống, ví dụ `"Ngọ"`, `"Tý"`, sang đúng chỉ số Địa Chi tương ứng.

* **Tích hợp logic tính toán nội bộ:** Bao gồm sẵn phần lõi tính toán từ `ansaotuvi`, đồng thời bổ sung các chỉnh sửa riêng cho trường hợp Tuần/Triệt bao phủ hai cung.

### Hạn chế hiện tại & Giả định
- **Giả định múi giờ:** Mặc định tính toán theo múi giờ Việt Nam (GMT+7). Mọi thông tin giờ sinh ở múi giờ khác cần được quy đổi về GMT+7 trước khi truyền vào.
- **Giới hạn lịch pháp:** Các phép tính toán âm dương lịch ổn định và chính xác cao với các năm sinh thời hiện đại. Thuật toán chuyển đổi lịch âm dựa trên phương pháp của Hoàng Nam Địa (HND), có thể có sai lệch nhỏ ở một số năm nhuận quá khứ xa hoặc tương lai xa.
- **Hệ phái an sao:** Thuật toán an sao theo quy chuẩn chung phổ biến tại Việt Nam. Dự án hiện chưa hỗ trợ cấu hình tùy biến trọng số sao hoặc các cách an sao khác nhau của các hệ phái khác (như Nam phái vs Bắc phái vs tự chọn).

### Tuyên bố miễn trừ trách nhiệm về Lịch pháp & Học phái
> [!NOTE]
> **Tuyên bố về các trường phái tính toán:** Tử Vi Việt Nam là một bộ môn học thuật vô cùng phong phú với nhiều trường phái truyền thống khác nhau (như Nam Phái, Bắc Phái). Các phương pháp an sao, phân định thứ hạng sao, ngũ hành bản mệnh hay luận giải có thể có sự khác biệt nhất định tùy thuộc vào từng truyền thừa hay học phái. Kết quả thu được từ công cụ này được tính toán hoàn toàn dựa trên logic đồng thuận phổ biến và chỉ nên được sử dụng như một tài liệu tham khảo tính toán khách quan, không phải là lời luận giải Tử Vi mang tính chất duy nhất hay định mệnh.

---

### Cài đặt

Bạn có thể cài đặt trực tiếp `tuvi-mcp-server` từ PyPI bằng pip:
```bash
pip install tuvi-mcp-server
```

### Thiết lập môi trường phát triển & Đóng góp (Development Setup)

Nếu muốn đóng góp cho dự án hoặc chạy kiểm thử tự động, bạn có thể thiết lập môi trường phát triển cục bộ:

1. **Tạo môi trường ảo:**
   ```bash
   python3 -m venv .venv
   ```

2. **Cài đặt gói ở chế độ editable cùng các thư viện kiểm thử:**
   ```bash
   .venv/bin/pip install --upgrade pip
   .venv/bin/pip install -e ".[test]"
   ```

3. **Chạy kiểm thử (Unit Tests):**
   Xác minh cài đặt bằng cách chạy bộ kiểm thử với `pytest`:
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

Tạo lá số Tử Vi đầy đủ từ thông tin ngày giờ sinh, hỗ trợ xuất ảnh lá số chất lượng cao.

* **Tham số:**
  * `name` (string): Tên người xem, mặc định là `"Khách"`.
  * `day` (integer): Ngày sinh, từ 1 đến 31.
  * `month` (integer): Tháng sinh, từ 1 đến 12.
  * `year` (integer): Năm sinh.
  * `hour_val` (string): Giờ sinh, ví dụ `"14:30"`, `"Ngọ"`, `"Tý"`.
  * `gender_val` (string): Giới tính, nhận giá trị `"Nam"` hoặc `"Nữ"`.
  * `is_solar` (boolean): `True` nếu dùng Dương lịch, `False` nếu dùng Âm lịch. Mặc định là `True`.
  * `current_year` (integer, tùy chọn): Năm cần xem vận hạn để tính sao lưu (mặc định là năm hiện tại).
  * `generate_image` (boolean, tùy chọn): Có xuất và trả về ảnh lá số chất lượng cao đi kèm hay không (mặc định: `True`).
* **Đầu ra:**
  * Nếu `generate_image` là `True`, trả về danh sách `[Image, chart_data]` (trong đó `Image` là block chứa dữ liệu ảnh của FastMCP).
  * Nếu `generate_image` là `False`, trả về trực tiếp đối tượng JSON `chart_data`.

---

#### 2. `get_van_han`

Tính toán sao lưu động và xác định các cung hạn đang kích hoạt, bao gồm Đại Hạn, Tiểu Hạn, Nguyệt Hạn và Nhật Hạn cho tháng/năm cần xem.

* **Tham số:**
  * `name`, `day`, `month`, `year`, `hour_val`, `gender_val`, `is_solar`: giống như trong `generate_horoscope`.
  * `current_year` (integer): Năm âm lịch cần xem hạn. Mặc định là năm hiện tại.
  * `current_month` (integer): Tháng âm lịch cần xem hạn, từ 1 đến 12. Mặc định là 1.
  * `current_day` (integer, tùy chọn): Ngày âm lịch cần xem hạn (1-30). Nếu cung cấp, sẽ tính thêm Nhật Hạn.

---

#### 3. `convert_calendar`

Chuyển đổi ngày qua lại giữa Dương lịch và Âm lịch.

* **Tham số:**
  * `day` (integer): Ngày cần chuyển đổi.
  * `month` (integer): Tháng cần chuyển đổi.
  * `year` (integer): Năm cần chuyển đổi.
  * `from_solar` (boolean): `True` để chuyển đổi từ Dương lịch sang Âm lịch (mặc định), hoặc `False` để chuyển từ Âm lịch sang Dương lịch.
  * `lunar_leap` (boolean): Chỉ dùng khi `from_solar` là `False`. `True` nếu tháng âm lịch đầu vào là tháng nhuận.
  * `timezone` (integer): Múi giờ, mặc định là 7 (Giờ Việt Nam).
* **Đầu ra:**
  * Nếu `from_solar` là `True`, trả về dictionary chứa `lunar_day`, `lunar_month`, `lunar_year`, `lunar_leap` (boolean), và chuỗi ngày đã định dạng `formatted`.
  * Nếu `from_solar` là `False`, trả về dictionary chứa `solar_day`, `solar_month`, `solar_year`, và chuỗi ngày đã định dạng `formatted`.

---

#### 4. `get_auspicious_info`

Đánh giá ngày tốt, giờ Hoàng Đạo, 12 Trực, 28 Tú, Tiết Khí và hướng xuất hành cho một ngày bất kỳ.

* **Tham số:**
  * `day` (integer, tùy chọn): Ngày trong tháng. Mặc định là hôm nay.
  * `month` (integer, tùy chọn): Tháng. Mặc định là tháng hiện tại.
  * `year` (integer, tùy chọn): Năm (4 chữ số). Mặc định là năm hiện tại.
  * `is_solar` (boolean, tùy chọn): `True` nếu dùng Dương lịch (mặc định), `False` nếu dùng Âm lịch.
* **Đầu ra:** Dictionary chứa: `duong_lich`, `am_lich`, `can_chi_ngay`, `ngay_hoang_dao`, `truc_ngay`, `nhi_thap_bat_tu`, `huong_xuat_hanh`, `gio_hoang_dao`, `tiet_khi_hien_tai`, `tiet_khi_tiep_theo`.

---

### Ví dụ gọi Tool & Đầu ra JSON mẫu

Dưới đây là cấu trúc dữ liệu JSON thực tế do máy chủ MCP trả về để minh họa tính rõ ràng và gọn gàng của định dạng đầu ra.

#### 1. Kết quả Lập Lá Số (`generate_horoscope`)

Khi gọi `generate_horoscope(name="Nguyễn Văn A", day=10, month=6, year=1995, hour_val="14:30", gender_val="Nam", is_solar=true)`, đầu ra trả về đối tượng JSON gồm thông tin Thiên Bàn (`thien_ban`), danh sách 12 cung Địa Bàn (`dia_ban`), và các cách cục (`cach_cuc`).

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
    "than_chu": "Thiên cơ",
    "ban_menh": "SƠN ÐẦU HỎA"
  },
  "cach_cuc": [
    {
      "id": 5,
      "name": "Đan Trì Quế Trì Cách",
      "category": "Cát Cục",
      "description": "Thái Dương cư Thìn Tỵ Ngọ (Đan Trì) hoặc Thái Âm cư Dậu Tuất Hợi (Quế Trì)."
    }
  ],
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

