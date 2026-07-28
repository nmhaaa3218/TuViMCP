# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

Vietnamese Auspicious Days & Hours Evaluator.
Wraps tuvi_mcp.lunar_calendar with a complete Vietnamese localization mapping layer.
"""

from .lunar_calendar import Lunar, Solar

# Can & Chi maps
CAN_MAP = {
    "甲": "Giáp", "乙": "Ất", "丙": "Bính", "丁": "Đinh", "戊": "Mậu",
    "己": "Kỷ", "庚": "Canh", "辛": "Tân", "壬": "Nhâm", "癸": "Quý"
}

ZHI_MAP = {
    "子": "Tý", "丑": "Sửu", "寅": "Dần", "卯": "Mão", "辰": "Thìn", "巳": "Tỵ",
    "午": "Ngọ", "未": "Mùi", "申": "Thân", "酉": "Dậu", "戌": "Tuất", "亥": "Hợi"
}

SHENGXIAO_MAP = {
    "鼠": "Chuột", "牛": "Trâu", "虎": "Hổ", "兔": "Thỏ", "龙": "Rồng", "蛇": "Rắn",
    "马": "Ngựa", "羊": "Dê", "猴": "Khỉ", "鸡": "Gà", "狗": "Chó", "猪": "Heo"
}

# 12 Thần Hoàng Đạo / Hắc Đạo
TIAN_SHEN_MAP = {
    "青龙": "Thanh Long",
    "明堂": "Minh Đường",
    "天刑": "Thiên Hình",
    "朱雀": "Chu Tước",
    "金匮": "Kim Quỹ",
    "天德": "Thiên Đức",
    "白虎": "Bạch Hổ",
    "玉堂": "Ngọc Đường",
    "天牢": "Thiên Lao",
    "玄武": "Huyền Vũ",
    "司命": "Tư Mệnh",
    "勾陈": "Câu Trần",
}

TIAN_SHEN_TYPE_MAP = {
    "黄道": "Hoàng Đạo",
    "黑道": "Hắc Đạo",
}

TIAN_SHEN_LUCK_MAP = {
    "吉": "Cát (Tốt)",
    "凶": "Hung (Xấu)",
    "平": "Bình (Bình thường)",
}

# 12 Trực & Lời khuyên cổ truyền
TRUC_MAP = {
    "Kiến": {"ten": "Trực Kiến", "danh_gia": "Cát (Tốt)", "loi_khuyen": "Tốt cho việc khởi công, làm nhà, xuất hành, nhậm chức. Tránh đào giếng, nhặt của rơi."},
    "Trừ": {"ten": "Trực Trừ", "danh_gia": "Bình", "loi_khuyen": "Tốt cho chữa bệnh, giải trừ tai ạch, dọn dẹp, tẩy uế. Tránh cưới hỏi, ký hợp đồng."},
    "Mãn": {"ten": "Trực Mãn", "danh_gia": "Cát (Tốt)", "loi_khuyen": "Tốt cho tế lễ, cầu tài, mở kho, nhập học, cất may quần áo. Tránh xuất hành, kiện tụng."},
    "Bình": {"ten": "Trực Bình", "danh_gia": "Bình", "loi_khuyen": "Tốt cho sửa đường, làm phẳng, hòa giải, đắp đập. Tránh khởi công công trình lớn."},
    "Định": {"ten": "Trực Định", "danh_gia": "Cát (Tốt)", "loi_khuyen": "Tốt cho nhập học, ký kết, đính hôn, lập hợp đồng, chăn nuôi. Tránh kiện tụng, di chuyển."},
    "Chấp": {"ten": "Trực Chấp", "danh_gia": "Bình", "loi_khuyen": "Tốt cho xây dựng, trồng trọt, săn bắt, bắt trộm. Tránh mở kho, xuất tiền tài."},
    "Phá": {"ten": "Trực Phá", "danh_gia": "Hung (Xấu)", "loi_khuyen": "Tốt cho phá vỡ, dỡ nhà, giải táng, chữa bệnh dứt điểm. Kỵ cưới hỏi, ký kết, kinh doanh."},
    "Nguy": {"ten": "Trực Nguy", "danh_gia": "Hung (Xấu)", "loi_khuyen": "Tốt cho cúng tế, cầu an. Kỵ trèo cao, đi thuyền, làm việc mạo hiểm, thi công công trình."},
    "Thành": {"ten": "Trực Thành", "danh_gia": "Cát (Tốt)", "loi_khuyen": "Tốt cho nhập học, khai trương, cưới hỏi, kết hôn, nhập trạch, mở cửa hàng."},
    "Thu": {"ten": "Trực Thâu", "danh_gia": "Cát (Tốt)", "loi_khuyen": "Tốt cho thu hoạch, cất giữ tài sản, gặt hái, thu nợ, mua bán. Tránh mở cửa hàng, tang lễ."},
    "Khai": {"ten": "Trực Khai", "danh_gia": "Cát (Tốt)", "loi_khuyen": "Tốt cho mở cửa hàng, bắt đầu công việc, khai trương, cưới hỏi, nhập học. Tránh động thổ, an táng."},
    "Bế": {"ten": "Trực Bế", "danh_gia": "Hung (Xấu)", "loi_khuyen": "Tốt cho đắp đập, xây nhà kho, an táng, cất giữ bí mật. Kỵ mở cửa hàng, xuất hành, khám bệnh."},
}


# 28 Tú (Nhị Thập Bát Tú)
XIU_MAP = {
    "Giác": {"ten": "Sao Giác", "dong_vat": "Giác Mộc Đổng (Cá Thần)", "danh_gia": "Cát (Tốt)"},
    "Cang": {"ten": "Sao Cang", "dong_vat": "Cang Kim Long (Rồng)", "danh_gia": "Hung (Xấu)"},
    "Đê": {"ten": "Sao Đê", "dong_vat": "Đê Thổ Lạc (Cừu)", "danh_gia": "Hung (Xấu)"},
    "Phòng": {"ten": "Sao Phòng", "dong_vat": "Phòng Nhật Thố (Thỏ)", "danh_gia": "Cát (Tốt)"},
    "Tâm": {"ten": "Sao Tâm", "dong_vat": "Tâm Nguyệt Hồ (Cáo)", "danh_gia": "Hung (Xấu)"},
    "Vĩ": {"ten": "Sao Vĩ", "dong_vat": "Vĩ Hỏa Hổ (Hổ)", "danh_gia": "Cát (Tốt)"},
    "Cơ": {"ten": "Sao Cơ", "dong_vat": "Cơ Thủy Báo (Báo)", "danh_gia": "Cát (Tốt)"},
    "Đẩu": {"ten": "Sao Đẩu", "dong_vat": "Đẩu Mộc Giải (Cua)", "danh_gia": "Cát (Tốt)"},
    "Ngưu": {"ten": "Sao Ngưu", "dong_vat": "Ngưu Kim Ngưu (Trâu)", "danh_gia": "Hung (Xấu)"},
    "Nữ": {"ten": "Sao Nữ", "dong_vat": "Nữ Thổ Bức (Dơi)", "danh_gia": "Hung (Xấu)"},
    "Hư": {"ten": "Sao Hư", "dong_vat": "Hư Nhật Thử (Chuột)", "danh_gia": "Hung (Xấu)"},
    "Nguy": {"ten": "Sao Nguy", "dong_vat": "Nguy Nguyệt Én (Chim Én)", "danh_gia": "Hung (Xấu)"},
    "Thất": {"ten": "Sao Thất", "dong_vat": "Thất Hỏa Trư (Heo)", "danh_gia": "Cát (Tốt)"},
    "Bích": {"ten": "Sao Bích", "dong_vat": "Bích Thủy Du (Rái Cá)", "danh_gia": "Cát (Tốt)"},
    "Khuê": {"ten": "Sao Khuê", "dong_vat": "Khuê Mộc Lang (Chó Sói)", "danh_gia": "Hung (Xấu)"},
    "Lâu": {"ten": "Sao Lâu", "dong_vat": "Lâu Kim Cẩu (Chó)", "danh_gia": "Cát (Tốt)"},
    "Vị": {"ten": "Sao Vị", "dong_vat": "Vị Thổ Trĩ (Chim Trĩ)", "danh_gia": "Cát (Tốt)"},
    "Mão": {"ten": "Sao Mão", "dong_vat": "Mão Nhật Kê (Gà)", "danh_gia": "Hung (Xấu)"},
    "Tất": {"ten": "Sao Tất", "dong_vat": "Tất Nguyệt Ô (Quạ)", "danh_gia": "Cát (Tốt)"},
    "Chủy": {"ten": "Sao Chủy", "dong_vat": "Chủy Hỏa Hầu (Khỉ)", "danh_gia": "Hung (Xấu)"},
    "Sâm": {"ten": "Sao Sâm", "dong_vat": "Sâm Thủy Vượn (Vượn)", "danh_gia": "Cát (Tốt)"},
    "Tỉnh": {"ten": "Sao Tỉnh", "dong_vat": "Tỉnh Mộc Hãn (Chim Trĩ)", "danh_gia": "Cát (Tốt)"},
    "Quỷ": {"ten": "Sao Quỷ", "dong_vat": "Quỷ Kim Dương (Dê)", "danh_gia": "Hung (Xấu)"},
    "Liễu": {"ten": "Sao Liễu", "dong_vat": "Liễu Thổ Chấu (Hoẵng)", "danh_gia": "Hung (Xấu)"},
    "Tinh": {"ten": "Sao Tinh", "dong_vat": "Tinh Nhật Mã (Ngựa)", "danh_gia": "Hung (Xấu)"},
    "Trương": {"ten": "Sao Trương", "dong_vat": "Trương Nguyệt Lộc (Nai)", "danh_gia": "Cát (Tốt)"},
    "Dực": {"ten": "Sao Dực", "dong_vat": "Dực Hỏa Xà (Rắn)", "danh_gia": "Hung (Xấu)"},
    "Chẩn": {"ten": "Sao Chẩn", "dong_vat": "Chẩn Thủy Dẫn (Giun)", "danh_gia": "Cát (Tốt)"},
}


# Directions
DIRECTION_MAP = {
    "东北": "Đông Bắc",
    "西北": "Tây Bắc",
    "西南": "Tây Nam",
    "正南": "Chính Nam",
    "东南": "Đông Nam",
    "正东": "Chính Đông",
    "正西": "Chính Tây",
    "正北": "Chính Bắc",
    "中": "Trung Tâm",
    "艮": "Đông Bắc",
    "乾": "Tây Bắc",
    "坤": "Tây Nam",
    "离": "Chính Nam",
    "巽": "Đông Nam",
    "震": "Chính Đông",
    "兑": "Chính Tây",
    "坎": "Chính Bắc",
}

# Lục Diệu
LIU_YAO_MAP = {
    "先胜": "Tốc Hỷ (Tin vui đến nhanh, đi xa có lộc)",
    "大安": "Đại An (Mọi việc yên ổn, bình an, hanh thông)",
    "留连": "Lưu Niên (Mọi việc dây dưa, mưu sự chậm trễ)",
    "友引": "Lưu Niên (Mọi việc dây dưa, mưu sự chậm trễ)",
    "流连": "Lưu Niên (Mọi việc dây dưa, mưu sự chậm trễ)",
    "先负": "Tiểu Cát (Gặp may mắn nhỏ, quý nhân phù trợ)",
    "速喜": "Tốc Hỷ (Tin vui đến nhanh, đi xa có lộc)",
    "赤口": "Xích Khẩu (Dễ sinh khẩu thiệt, mâu thuẫn, phòng thị phi)",
    "小吉": "Tiểu Cát (Gặp may mắn nhỏ, quý nhân phù trợ)",
    "空亡": "Không Vong (Tránh mưu đại sự, phòng hao tốn)",
    "佛灭": "Không Vong (Tránh mưu đại sự, phòng hao tốn)",
    # Vietnamese localized keys
    "Tiên Thắng": "Tốc Hỷ (Tin vui đến nhanh, đi xa có lộc)",
    "Hữu Dẫn": "Lưu Niên (Mọi việc dây dưa, mưu sự chậm trễ)",
    "Tiên Bại": "Tiểu Cát (Gặp may mắn nhỏ, quý nhân phù trợ)",
    "Phật Diệt": "Không Vong (Tránh mưu đại sự, phòng hao tốn)",
    "Đại An": "Đại An (Mọi việc yên ổn, bình an, hanh thông)",
    "Xích Khẩu": "Xích Khẩu (Dễ sinh khẩu thiệt, mâu thuẫn, phòng thị phi)",
    "Tốc Hỷ": "Tốc Hỷ (Tin vui đến nhanh, đi xa có lộc)",
    "Lưu Niên": "Lưu Niên (Mọi việc dây dưa, mưu sự chậm trễ)",
    "Tiểu Cát": "Tiểu Cát (Gặp may mắn nhỏ, quý nhân phù trợ)",
    "Không Vong": "Không Vong (Tránh mưu đại sự, phòng hao tốn)",
}

# Tiết khí (24 Solar Terms)
JIE_QI_MAP = {
    "立春": "Lập Xuân",
    "雨水": "Vũ Thủy",
    "惊蛰": "Kinh Trập",
    "春分": "Xuân Phân",
    "清明": "Thanh Minh",
    "谷雨": "Cốc Vũ",
    "立夏": "Lập Hạ",
    "小满": "Tiểu Mãn",
    "芒种": "Mang Chủng",
    "夏至": "Hạ Chí",
    "小暑": "Tiểu Thử",
    "大暑": "Đại Thử",
    "立秋": "Lập Thu",
    "处暑": "Xử Thử",
    "白露": "Bạch Lộ",
    "秋分": "Thu Phân",
    "寒露": "Hàn Lộ",
    "霜降": "Sương Giáng",
    "立冬": "Lập Đông",
    "小雪": "Tiểu Tuyết",
    "大雪": "Đại Tuyết",
    "冬至": "Đông Chí",
    "小寒": "Tiểu Hàn",
    "大寒": "Đại Hàn",
}

# Time windows for 12 Earthly Branch hours
HOUR_WINDOW_MAP = {
    "子": "23:00 - 01:00",
    "丑": "01:00 - 03:00",
    "寅": "03:00 - 05:00",
    "卯": "05:00 - 07:00",
    "辰": "07:00 - 09:00",
    "巳": "09:00 - 11:00",
    "午": "11:00 - 13:00",
    "未": "13:00 - 15:00",
    "申": "15:00 - 17:00",
    "酉": "17:00 - 19:00",
    "戌": "19:00 - 21:00",
    "亥": "21:00 - 23:00",
    "Tý": "23:00 - 01:00",
    "Sửu": "01:00 - 03:00",
    "Dần": "03:00 - 05:00",
    "Mão": "05:00 - 07:00",
    "Thìn": "07:00 - 09:00",
    "Tỵ": "09:00 - 11:00",
    "Ngọ": "11:00 - 13:00",
    "Mùi": "13:00 - 15:00",
    "Thân": "15:00 - 17:00",
    "Dậu": "17:00 - 19:00",
    "Tuất": "19:00 - 21:00",
    "Hợi": "21:00 - 23:00",
}



def format_gan_zhi(gan_zhi_str: str) -> str:
    """Format GanZhi string into Vietnamese with space e.g. '壬寅' -> 'Nhâm Dần'."""
    if not gan_zhi_str or len(gan_zhi_str) < 2:
        return gan_zhi_str
    if " " in gan_zhi_str:
        return gan_zhi_str
    g_zh, z_zh = gan_zhi_str[0], gan_zhi_str[1]
    g_vi = CAN_MAP.get(g_zh, g_zh)
    z_vi = ZHI_MAP.get(z_zh, z_zh)
    return f"{g_vi} {z_vi}"



def translate_direction(zh_dir: str) -> str:
    """Translate Chinese direction to Vietnamese."""
    if not zh_dir:
        return "N/A"
    return DIRECTION_MAP.get(zh_dir.strip(), zh_dir)


def get_auspicious_details(day: int, month: int, year: int, is_solar: bool = True) -> dict:
    """
    Evaluates Auspicious Days, Auspicious Hours (Hoàng Đạo / Hắc Đạo), 12 Trực, 28 Tú,
    Directions, Lục Diệu, and Tiết Khí for a given date in Vietnamese.
    """
    try:
        from . import tuvi_calculator
        val_err = tuvi_calculator.validate_calendar_convert(day, abs(month), year)
        if val_err:
            return val_err

        if is_solar:
            solar = Solar.fromYmd(year, month, day)
            lunar = solar.getLunar()
        else:
            lunar = Lunar.fromYmd(year, month, day)
            solar = lunar.getSolar()

        # Basic dates
        solar_str = f"{solar.getDay():02d}/{solar.getMonth():02d}/{solar.getYear()}"
        lunar_year_gz = format_gan_zhi(lunar.getYearInGanZhi())
        lunar_sx = SHENGXIAO_MAP.get(lunar.getYearShengXiao(), lunar.getYearShengXiao())
        abs_m = abs(lunar.getMonth())
        leap_str = " (Nhuận)" if (hasattr(lunar, 'isLeap') and lunar.isLeap()) or lunar.getMonth() < 0 else ""
        lunar_str = f"{lunar.getDay():02d}/{abs_m:02d}{leap_str}/{lunar.getYear()} ({lunar_year_gz} - Năm {lunar_sx})"

        day_gz = format_gan_zhi(lunar.getDayInGanZhi())
        day_sx = SHENGXIAO_MAP.get(lunar.getDayShengXiao(), lunar.getDayShengXiao())
        can_chi_ngay = f"{day_gz} (Ngày {day_sx})"

        # Day TianShen (Hoàng Đạo / Hắc Đạo)
        raw_tian_shen = lunar.getDayTianShen()
        raw_tian_shen_type = lunar.getDayTianShenType()
        raw_tian_shen_luck = lunar.getDayTianShenLuck()

        day_hoang_dao = {
            "is_hoang_dao": raw_tian_shen_type == "Hoàng Đạo",
            "ten_sao": TIAN_SHEN_MAP.get(raw_tian_shen, raw_tian_shen),
            "loai": TIAN_SHEN_TYPE_MAP.get(raw_tian_shen_type, raw_tian_shen_type),
            "danh_gia": TIAN_SHEN_LUCK_MAP.get(raw_tian_shen_luck, raw_tian_shen_luck),
        }

        # 12 Trực
        raw_truc = lunar.getZhiXing()
        truc_info = TRUC_MAP.get(raw_truc, {"ten": raw_truc, "danh_gia": "N/A", "loi_khuyen": ""})

        # 28 Tú
        raw_xiu = lunar.getXiu()
        xiu_info = XIU_MAP.get(raw_xiu, {"ten": raw_xiu, "dong_vat": "", "danh_gia": "N/A"})

        # Lục Diệu
        raw_liu_yao = lunar.getLiuYao()
        luc_dieu = LIU_YAO_MAP.get(raw_liu_yao, raw_liu_yao)

        # Tiết khí
        prev_jq = lunar.getPrevJieQi()
        next_jq = lunar.getNextJieQi()
        
        tiet_khi_hien_tai = "N/A"
        if prev_jq:
            p_name = JIE_QI_MAP.get(prev_jq.getName(), prev_jq.getName())
            p_time = prev_jq.getSolar().toYmdHms()
            tiet_khi_hien_tai = f"{p_name} (vào {p_time})"

        tiet_khi_tiep_theo = "N/A"
        if next_jq:
            n_name = JIE_QI_MAP.get(next_jq.getName(), next_jq.getName())
            n_time = next_jq.getSolar().toYmdHms()
            tiet_khi_tiep_theo = f"{n_name} (vào {n_time})"

        # Hướng xuất hành (Thần Hướng)
        huong_xuat_hanh = {
            "hy_than": translate_direction(lunar.getDayPositionXiDesc()),
            "tai_than": translate_direction(lunar.getDayPositionCaiDesc()),
            "phuc_than": translate_direction(lunar.getDayPositionFuDesc()),
            "duong_quy_than": translate_direction(lunar.getDayPositionYangGuiDesc()),
            "am_quy_than": translate_direction(lunar.getDayPositionYinGuiDesc()),
        }

        # Hourly breakdown (12 Giờ Hoàng Đạo / Hắc Đạo)
        times = lunar.getTimes()
        gio_hoang_dao = []
        visited_zhis = set()

        for t in times:
            zhi = t.getZhi()
            if zhi in visited_zhis:
                continue
            visited_zhis.add(zhi)

            raw_h_shen = t.getTianShen()
            raw_h_type = t.getTianShenType()
            raw_h_luck = t.getTianShenLuck()
            zhi_vi = ZHI_MAP.get(zhi, zhi)

            gio_hoang_dao.append(
                {
                    "chi": zhi_vi,
                    "can_chi": format_gan_zhi(t.getGanZhi()),
                    "khung_gio": HOUR_WINDOW_MAP.get(zhi, ""),
                    "is_hoang_dao": raw_h_type == "Hoàng Đạo",
                    "ten_sao": TIAN_SHEN_MAP.get(raw_h_shen, raw_h_shen),
                    "loai": TIAN_SHEN_TYPE_MAP.get(raw_h_type, raw_h_type),
                    "danh_gia": TIAN_SHEN_LUCK_MAP.get(raw_h_luck, raw_h_luck),
                }
            )

        return {
            "duong_lich": solar_str,
            "am_lich": lunar_str,
            "can_chi_ngay": can_chi_ngay,
            "tiet_khi_hien_tai": tiet_khi_hien_tai,
            "tiet_khi_tiep_theo": tiet_khi_tiep_theo,
            "ngay_hoang_dao": day_hoang_dao,
            "truc_ngay": truc_info,
            "nhi_thap_bat_tu": xiu_info,
            "luc_dieu": luc_dieu,
            "huong_xuat_hanh": huong_xuat_hanh,
            "gio_hoang_dao": gio_hoang_dao,
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

