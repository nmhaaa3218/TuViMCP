# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>
"""
import os
import tempfile

from PIL import Image, ImageDraw, ImageFont

# Element Colors Mapping (Modern Palette)
ELEMENT_COLORS = {
    "Mộc": "#059669",  # Emerald Green
    "Hỏa": "#DC2626",  # Crimson Red
    "Thổ": "#D97706",  # Amber/Orange
    "Kim": "#4B5563",  # Cool Gray
    "Thủy": "#2563EB"  # Royal Blue
}

# 1-indexed Cung coordinates mapping on a 4x4 grid (col, row)
CUNG_COORDS = {
    1: (2, 3),   # Tý
    2: (1, 3),   # Sửu
    3: (0, 3),   # Dần
    4: (0, 2),   # Mão
    5: (0, 1),   # Thìn
    6: (0, 0),   # Tỵ
    7: (1, 0),   # Ngọ
    8: (2, 0),   # Mùi
    9: (3, 0),   # Thân
    10: (3, 1),  # Dậu
    11: (3, 2),  # Tuất
    12: (3, 3),  # Hợi
}

# Standard 14 chính tinh IDs
CHINH_TINH_IDS = set(range(1, 15))

# Transit stars mapping
TRANSIT_STAR_DETAILS = {
    "Lưu Thái Tuế": {"display": "L.Thái Tuế", "element": "H", "type": 15},
    "Lưu Lộc Tồn": {"display": "L.Lộc Tồn", "element": "O", "type": 3},
    "Lưu Kình Dương": {"display": "L.Kình Dương", "element": "K", "type": 11},
    "Lưu Đà La": {"display": "L.Đà La", "element": "K", "type": 11},
    "Lưu Thiên Mã": {"display": "L.Thiên Mã", "element": "H", "type": 3},
    "Lưu Thiên Khốc": {"display": "L.Thiên Khốc", "element": "T", "type": 12},
    "Lưu Thiên Hư": {"display": "L.Thiên Hư", "element": "T", "type": 12},
}

# Suffix maps for star attributes
ATTR_SUFFIX_MAP = {
    "Miếu địa": "M",
    "Vượng địa": "V",
    "Đắc địa": "Đ",
    "Bình hòa": "B",
    "Hãm địa": "H"
}

def get_font(size=12, bold=False, font_path=None):
    """Resolve font dynamically according to priority:
    1. Explicit custom font_path (if provided, valid type, and file exists)
    2. Package-bundled Unicode font (tuvi_mcp/_fonts/Roboto-*.ttf)
    3. OS System Desktop Fonts (macOS, Linux, Windows)
    4. Pillow default fallback (with size parameter support for Pillow >=10.1)
    """
    # 1. Custom font_path
    if font_path and isinstance(font_path, (str, os.PathLike)):
        try:
            if os.path.exists(font_path):
                return ImageFont.truetype(str(font_path), size)
        except Exception:
            pass

    font_filename = "Roboto-Bold.ttf" if bold else "Roboto-Regular.ttf"

    # 2. Try bundled package font
    bundled_path = None
    try:
        from importlib.resources import files
        p = files("tuvi_mcp").joinpath("_fonts", font_filename)
        p_str = str(p)
        if os.path.exists(p_str):
            bundled_path = p_str
    except Exception:
        pass

    if not bundled_path or not os.path.exists(bundled_path):
        bundled_path = os.path.join(os.path.dirname(__file__), "_fonts", font_filename)

    try:
        if bundled_path and os.path.exists(bundled_path):
            return ImageFont.truetype(bundled_path, size)
    except Exception:
        pass

    # 3. Try OS System Fonts
    paths = []
    if bold:
        paths = [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/Library/Fonts/Arial Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
            "C:\\Windows\\Fonts\\arialbd.ttf"
        ]
    else:
        paths = [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/Library/Fonts/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
            "C:\\Windows\\Fonts\\arial.ttf"
        ]

    for p in paths:
        try:
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
        except Exception:
            pass

    # 4. Pillow default fallback (supports size in Pillow >= 10.1.0)
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        try:
            return ImageFont.load_default()
        except Exception:
            return None

def draw_badge(draw, cx, cy, text, w, h, font=None):
    """Draw a dark badge on the shared border of cungs for Tuần/Triệt."""
    x0 = cx - w // 2
    y0 = cy - h // 2
    x1 = cx + w // 2
    y1 = cy + h // 2

    draw.rounded_rectangle([x0, y0, x1, y1], radius=4, fill="#111827", outline="#F3F4F6", width=1)
    if font is None:
        font = get_font(size=11, bold=True)
    tw = draw.textlength(text, font=font)
    th = 11
    draw.text((cx - tw / 2, cy - th / 2 - 1), text, fill="#FFFFFF", font=font)

def draw_tuan_triet(draw, dia_ban, font_bold=None):
    """Draw Tuần/Triệt border badges exactly on shared borders of cungs (Row height 400)."""
    pairs = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12)]

    for c1_id, c2_id in pairs:
        c1 = next((c for c in dia_ban if c["cung_so"] == c1_id), None)
        c2 = next((c for c in dia_ban if c["cung_so"] == c2_id), None)
        if not c1 or not c2:
            continue

        col1, row1 = CUNG_COORDS[c1_id]
        col2, row2 = CUNG_COORDS[c2_id]

        if col1 == col2:  # Horizontal border
            bx = col1 * 300 + 150
            by = max(row1, row2) * 400
        elif row1 == row2:  # Vertical border
            bx = max(col1, col2) * 300
            by = row1 * 400 + 200
        else:
            continue

        badge_w, badge_h = 55, 22
        if c1.get("tuan_trung") and c2.get("tuan_trung"):
            draw_badge(draw, bx, by, "Tuần", badge_w, badge_h, font=font_bold)
        if c1.get("triet_lo") and c2.get("triet_lo"):
            draw_badge(draw, bx, by, "Triệt", badge_w, badge_h, font=font_bold)

def dich_cung(cung_start, offset):
    val = (cung_start + offset)
    if val % 12 == 0:
        return 12
    return val % 12

def draw_lines_behind_center(draw, m_cung, t_cung):
    """Draw the connecting lines of Mệnh and Thân Tam Hợp (Triads) & Xung Chiếu (Row height 400)."""
    def get_center(cung_id):
        col, row = CUNG_COORDS[cung_id]
        return col * 300 + 150, row * 400 + 200

    # Draw Mệnh lines (Light Red)
    if m_cung:
        p_menh = get_center(m_cung)
        p_triad1 = get_center(dich_cung(m_cung, 4))
        p_triad2 = get_center(dich_cung(m_cung, 8))
        p_opposite = get_center(dich_cung(m_cung, 6))

        # Triad Triangle
        draw.line([p_menh, p_triad1, p_triad2, p_menh], fill="#FCA5A5", width=2)
        # Opposite line
        draw.line([p_menh, p_opposite], fill="#FCA5A5", width=2)

    # Draw Thân lines (Light Gray)
    if t_cung and t_cung != m_cung:
        p_than = get_center(t_cung)
        p_triad1 = get_center(dich_cung(t_cung, 4))
        p_triad2 = get_center(dich_cung(t_cung, 8))
        p_opposite = get_center(dich_cung(t_cung, 6))

        # Triad Triangle
        draw.line([p_than, p_triad1, p_triad2, p_than], fill="#D1D5DB", width=2)
        # Opposite line
        draw.line([p_than, p_opposite], fill="#D1D5DB", width=2)

def generate_laso_image(
    chart_data: dict, 
    current_year: int = None, 
    font_path: str = None, 
    font_bold_path: str = None
) -> str:
    """Renders an A4 aspect ratio (1200x1697 px) Tu Vi horoscope image from chart data.

    :param chart_data: Dict containing 'thien_ban', 'dia_ban', and optional 'transit_stars'.
    :param current_year: Transit target Lunar year for header label.
    :param font_path: Optional file path to a custom regular TrueType (.ttf) font.
    :param font_bold_path: Optional file path to a custom bold TrueType (.ttf) font.
    :return: File path to generated PNG image.
    """
    thien_ban = chart_data.get("thien_ban", {})
    dia_ban = chart_data.get("dia_ban", [])

    # Identify Mệnh and Thân cungs
    m_cung = None
    t_cung = None
    for cung in dia_ban:
        if cung.get("cung_chu") == "Mệnh":
            m_cung = cung["cung_so"]
        if cung.get("cung_than"):
            t_cung = cung["cung_so"]

    # Enrich dia_ban with transit stars if present
    transit_stars = chart_data.get("transit_stars", [])
    if transit_stars:
        enriched_dia_ban = []
        for cung in dia_ban:
            cung_copy = dict(cung)
            cung_copy["sao"] = list(cung["sao"])
            enriched_dia_ban.append(cung_copy)

        for t_star in transit_stars:
            name = t_star["name"]
            c_num = t_star["cung_so"]
            details = TRANSIT_STAR_DETAILS.get(name)
            if details:
                target_cung = next((c for c in enriched_dia_ban if c["cung_so"] == c_num), None)
                if target_cung:
                    target_cung["sao"].append({
                        "id": 200 + len(transit_stars),
                        "name": details["display"],
                        "element": details["element"],
                        "type": details["type"],
                        "yin_yang": 0,
                        "attribute": None
                    })
        dia_ban = enriched_dia_ban

    # 1. Canvas Setup (A4 equivalent size: 1200x1697 px)
    img = Image.new("RGB", (1200, 1697), "#FAFAFA")
    draw = ImageDraw.Draw(img)

    # 2. Outer Boxes Background Fill (Row height 400)
    for c_id, (col, row) in CUNG_COORDS.items():
        x0, y0 = col * 300, row * 400
        x1, y1 = x0 + 300, y0 + 400
        draw.rectangle([x0, y0, x1, y1], fill="#FFFFFF")

    # 3. Center region solid fill (300 to 900 px, 400 to 1200 px)
    draw.rectangle([300, 400, 900, 1200], fill="#FFFFFF")

    # 4. Draw Connecting Lines (under the text)
    draw_lines_behind_center(draw, m_cung, t_cung)

    # 5. Draw Borders
    for i in range(5):
        draw.line([(i * 300, 0), (i * 300, 1600)], fill="#D1D5DB", width=1)
    for i in range(5):
        draw.line([(0, i * 400), (1200, i * 400)], fill="#D1D5DB", width=1)

    # Center region borders
    draw.rectangle([300, 400, 900, 1200], outline="#9CA3AF", width=2)

    # 6. Render Cungs (Row height 400)
    reg_font_path = font_path
    bold_font_path = font_bold_path or font_path

    font_bold = get_font(size=12, bold=True, font_path=bold_font_path)
    font_regular = get_font(size=12, bold=False, font_path=reg_font_path)
    font_title = get_font(size=15, bold=True, font_path=bold_font_path)
    font_chinh_tinh = get_font(size=14, bold=True, font_path=bold_font_path)

    for cung in dia_ban:
        c_id = cung["cung_so"]
        col, row = CUNG_COORDS[c_id]
        x0, y0 = col * 300, row * 400
        x1, y1 = x0 + 300, y0 + 400

        # Abbr Can-Chi (e.g. "Đ.Tỵ")
        can_chi_str = cung.get("cung_ten", "")
        if " " in can_chi_str:
            can, chi = can_chi_str.split(" ", 1)
            can_abbr = can[0] if len(can) > 0 else ""
            cung_abbr = f"{can_abbr}.{chi}"
        else:
            cung_abbr = can_chi_str

        # Polarity & Element
        polarity = "+" if cung.get("cung_so", 1) % 2 != 0 else "-"
        hanh_cung = cung.get("hanh_cung", "")
        element_str = f"{polarity}{hanh_cung}"

        # Đại Vận and Lunar Month
        dai_han = cung.get("dai_han")
        dai_han_str = str(dai_han) if dai_han is not None else ""
        month_idx = (c_id - 3) % 12 + 1
        month_str = f"Th.{month_idx}"

        # Headers drawing
        draw.text((x0 + 10, y0 + 10), cung_abbr, fill="#1F2937", font=font_bold)
        draw.text((x0 + 10, y0 + 26), element_str, fill="#4B5563", font=font_regular)

        tw_dh = draw.textlength(dai_han_str, font=font_bold)
        draw.text((x1 - 10 - tw_dh, y0 + 10), dai_han_str, fill="#1F2937", font=font_bold)
        tw_mon = draw.textlength(month_str, font=font_regular)
        draw.text((x1 - 10 - tw_mon, y0 + 26), month_str, fill="#4B5563", font=font_regular)

        # Cung Name (e.g. "NÔ BỘC")
        cung_chu = cung.get("cung_chu", "")
        cung_title = cung_chu.upper()
        if cung.get("cung_than"):
            cung_title += "<THÂN>"

        cung_color = ELEMENT_COLORS.get(hanh_cung, "#1F2937")
        tw_title = draw.textlength(cung_title, font=font_title)
        draw.text((x0 + 150 - tw_title / 2, y0 + 16), cung_title, fill=cung_color, font=font_title)

        stars = cung.get("sao", [])

        chinh_tinh_list = []
        cang_tinh_list = []
        saut_tinh_list = []
        trang_sinh_star = ""

        for s in stars:
            s_name = s.get("name", "")
            s_id = s.get("id")
            s_type = s.get("type", 2)
            s_element = s.get("element", "")
            s_attr = s.get("attribute", "")

            el_map = {"M": "Mộc", "H": "Hỏa", "O": "Thổ", "K": "Kim", "T": "Thủy"}
            s_element_full = el_map.get(s_element, s_element)

            trang_sinh_set = {"Tràng sinh", "Mộc dục", "Quan đới", "Lâm quan", "Đế vượng", "Suy", "Bệnh", "Tử", "Mộ", "Tuyệt", "Thai", "Dưỡng"}
            if s_name in trang_sinh_set:
                trang_sinh_star = s_name
                continue

            attr_short = ATTR_SUFFIX_MAP.get(s_attr, "")
            attr_str = f" ({attr_short})" if attr_short else ""
            s_color = ELEMENT_COLORS.get(s_element_full, "#1F2937")

            if s_id in CHINH_TINH_IDS:
                y_y = s.get("yin_yang", 0)
                prefix = "+" if y_y == 1 else "-" if y_y == -1 else ""
                display_name = f"{prefix}{s_name.upper()}{attr_str}"
                chinh_tinh_list.append((display_name, s_color))
            elif s_type < 10:
                display_name = f"{s_name}{attr_str}"
                cang_tinh_list.append((display_name, s_color))
            else:
                display_name = f"{s_name}{attr_str}"
                saut_tinh_list.append((display_name, s_color))

        # Draw Chính tinh
        cy_chinh = y0 + 55
        for ct_name, ct_col in chinh_tinh_list:
            tw_ct = draw.textlength(ct_name, font=font_chinh_tinh)
            draw.text((x0 + 75 - tw_ct / 2, cy_chinh), ct_name, fill=ct_col, font=font_chinh_tinh)
            cy_chinh += 18

        # Draw Cát tinh (Left column)
        cy_cat = max(cy_chinh + 5, y0 + 95)
        for cat_name, cat_col in cang_tinh_list:
            draw.text((x0 + 15, cy_cat), cat_name, fill=cat_col, font=font_bold)
            cy_cat += 18

        # Draw Sát tinh (Right column)
        cy_sat = y0 + 55
        for sat_name, sat_col in saut_tinh_list:
            draw.text((x0 + 160, cy_sat), sat_name, fill=sat_col, font=font_bold)
            cy_sat += 18

        # Draw Bottom metadata (Đại Vận label, Tràng Sinh, Lưu Niên label)
        if trang_sinh_star:
            tw_ts = draw.textlength(trang_sinh_star, font=font_regular)
            draw.text((x0 + 150 - tw_ts / 2, y0 + 378), trang_sinh_star, fill="#1F2937", font=font_regular)

        active_dh_cung = chart_data.get("dai_han", {}).get("cung_so") if isinstance(chart_data.get("dai_han"), dict) else None
        if not active_dh_cung and "target_period" in chart_data:
            age = chart_data["target_period"].get("current_age", 1)
            for c in dia_ban:
                ds = c.get("dai_han")
                if ds is not None and ds <= age < ds + 10:
                    active_dh_cung = c["cung_so"]
                    break
        if not active_dh_cung:
            active_dh_cung = m_cung

        REL_NAMES = ["MỆNH", "PHỤ", "PHÚC", "ĐIỀN", "QUAN", "NÔ", "DI", "TẬT", "TÀI", "TỬ", "PHỐI", "HUYNH"]
        offset_dv = (c_id - active_dh_cung + 12) % 12

        dv_label = f"ĐV.{REL_NAMES[offset_dv]}"
        draw.text((x0 + 10, y0 + 378), dv_label, fill="#4B5563", font=font_regular)

        ln_label = f"LN.{REL_NAMES[offset_dv]}"
        tw_ln = draw.textlength(ln_label, font=font_regular)
        draw.text((x1 - 10 - tw_ln, y0 + 378), ln_label, fill="#4B5563", font=font_regular)

    # 7. Draw Tuần and Triệt borders
    draw_tuan_triet(draw, dia_ban, font_bold=font_bold)

    # 8. Render Center Region details (600x800 px)
    font_logo = get_font(size=14, bold=True, font_path=bold_font_path)
    font_logo_sub = get_font(size=11, bold=False, font_path=reg_font_path)

    logo_str = "TẠO BỞI NMHAAA3218/TUVIMCP"
    logo_sub = "https://github.com/nmhaaa3218/TuViMCP"

    tw_l = draw.textlength(logo_str, font=font_logo)
    draw.text((600 - tw_l / 2, 430), logo_str, fill="#1E3A8A", font=font_logo)

    tw_ls = draw.textlength(logo_sub, font=font_logo_sub)
    draw.text((600 - tw_ls / 2, 450), logo_sub, fill="#4B5563", font=font_logo_sub)

    font_main_title = get_font(size=36, bold=True, font_path=bold_font_path)
    main_title = "Lá Số Tử Vi"
    tw_mt = draw.textlength(main_title, font=font_main_title)
    draw.text((600 - tw_mt / 2, 500), main_title, fill="#9F1239", font=font_main_title)

    font_kv_k = get_font(size=13, bold=True, font_path=bold_font_path)
    font_kv_v = get_font(size=13, bold=False, font_path=reg_font_path)

    name_val = thien_ban.get("ten", "Khách")
    gioi_tinh = thien_ban.get("gioi_tinh", "Nam")
    ngay_duong = thien_ban.get("ngay_duong", "")
    ngay_am = thien_ban.get("ngay_am", "")

    can_nam = thien_ban.get("can_nam", "")
    chi_nam = thien_ban.get("chi_nam", "")
    nam_am_str = f"{can_nam} {chi_nam}"

    can_thang = thien_ban.get("can_thang", "")
    chi_thang = thien_ban.get("chi_thang", "")
    thang_am_str = f"{can_thang} {chi_thang}"

    can_ngay = thien_ban.get("can_ngay", "")
    chi_ngay = thien_ban.get("chi_ngay", "")
    ngay_am_str = f"{can_ngay} {chi_ngay}"

    gio_sinh = thien_ban.get("gio_sinh", "")
    chi_gio = thien_ban.get("chi_gio_sinh", "")
    can_gio = thien_ban.get("can_gio_sinh", "")
    gio_sinh_str = f"{gio_sinh} ({can_gio} {chi_gio})"

    am_duong_nam = thien_ban.get("am_duong_nam_sinh", "")
    ban_menh = thien_ban.get("ban_menh", "")
    hanh_cuc = thien_ban.get("hanh_cuc", "")
    ten_cuc = thien_ban.get("ten_cuc", "")

    menh_chu = thien_ban.get("menh_chu", "")
    than_chu = thien_ban.get("than_chu", "")
    lai_nhan = thien_ban.get("lai_nhan_cung", "")

    current_year_str = ""
    if current_year:
        current_year_str = f"{current_year}"
        if "target_period" in chart_data:
            tp = chart_data["target_period"]
            current_year_str += f" ({tp.get('current_year_can_chi', '')}), {tp.get('current_age', '')} tuổi"
    else:
        current_year_str = "N/A"

    left_items = [
        ("Họ tên:", name_val),
        ("Dương lịch:", ngay_duong),
        ("Âm lịch:", ngay_am),
        ("Giờ sinh:", gio_sinh_str),
        ("Năm sinh:", nam_am_str),
        ("Tháng sinh:", thang_am_str),
        ("Ngày sinh:", ngay_am_str),
    ]

    right_items = [
        ("Âm dương:", f"{am_duong_nam} {gioi_tinh}"),
        ("Bản mệnh:", ban_menh),
        ("Hành cục:", f"{ten_cuc} ({hanh_cuc})"),
        ("Chủ mệnh:", menh_chu),
        ("Chủ thân:", than_chu),
        ("Lai nhân cung:", lai_nhan),
        ("Năm xem:", current_year_str),
    ]

    ly = 590
    for k, v in left_items:
        draw.text((330, ly), k, fill="#374151", font=font_kv_k)
        draw.text((420, ly), v, fill="#111827", font=font_kv_v)
        ly += 30

    ry = 590
    for k, v in right_items:
        draw.text((610, ry), k, fill="#374151", font=font_kv_k)
        draw.text((710, ry), v, fill="#111827", font=font_kv_v)
        ry += 30

    # Draw stamp emblem logo
    draw.rectangle([780, 1080, 850, 1150], outline="#DC2626", width=2)
    font_seal = get_font(size=12, bold=True, font_path=bold_font_path)
    draw.text((795, 1092), "TỬ", fill="#DC2626", font=font_seal)
    draw.text((795, 1108), "VI", fill="#DC2626", font=font_seal)
    draw.text((795, 1124), "MCP", fill="#DC2626", font=font_seal)

    # 9. Legend Footer Rendering (1200x1600 px to 1200x1697 px)
    draw.rectangle([0, 1600, 1200, 1697], fill="#F3F4F6")
    draw.line([(0, 1600), (1200, 1600)], fill="#D1D5DB", width=2)

    lx = 30
    for el_name, el_col in ELEMENT_COLORS.items():
        draw.rectangle([lx, 1635, lx + 20, 1655], fill=el_col)
        draw.text((lx + 28, 1637), el_name, fill="#1F2937", font=font_bold)
        lx += 120

    draw.text((620, 1637), "Sao Đắc Tính:  M: Miếu địa  |  V: Vượng địa  |  Đ: Đắc địa  |  B: Bình hòa  |  H: Hãm địa", fill="#374151", font=font_regular)

    powered_text = "Powered by nmhaaa3218/TuViMCP"
    tw_pw = draw.textlength(powered_text, font=font_bold)
    draw.text((1170 - tw_pw, 1665), powered_text, fill="#6B7280", font=font_bold)

    # 10. Save to a temporary file
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, f"tuvi_chart_{name_val.replace(' ', '_')}.png")
    img.save(output_path, "PNG")

    return output_path
