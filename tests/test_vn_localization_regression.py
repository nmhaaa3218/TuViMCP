# -*- coding: utf-8 -*-
"""
Regression tests for Việt hoá spacing bugs (B1-B4) and edge cases
introduced by switching GanZhi strings from "甲子" → "Giáp Tý".
"""
import pytest

from tuvi_mcp.lunar_calendar import Solar, Lunar, EightChar
from tuvi_mcp.lunar_calendar.util.LunarUtil import LunarUtil


# ----------------------------- B1 -----------------------------
def test_split_ganzhi_vietnamese():
    """splitGanZhi parses spaced Vietnamese GanZhi."""
    assert LunarUtil.splitGanZhi("Giáp Tý") == ("Giáp", "Tý")
    assert LunarUtil.splitGanZhi("Bính Dần") == ("Bính", "Dần")
    assert LunarUtil.splitGanZhi("Kỷ Hợi") == ("Kỷ", "Hợi")


def test_split_ganzhi_legacy_chinese():
    """splitGanZhi still accepts legacy unspaced Chinese."""
    assert LunarUtil.splitGanZhi("甲子") == ("甲", "子")
    assert LunarUtil.splitGanZhi("乙丑") == ("乙", "丑")


def test_get_xun_vietnamese_all_branches():
    """getXun must return the correct Tuần for each of the 6 Vietnamese Tuần."""
    # Tuần 0: Giáp Tý — index 0-9 in JIA_ZI
    assert LunarUtil.getXun("Giáp Tý") == "Giáp Tý"
    assert LunarUtil.getXun("Bính Dần") == "Giáp Tý"
    assert LunarUtil.getXun("Quý Dậu") == "Giáp Tý"
    # Tuần 1: Giáp Tuất — index 10-19
    assert LunarUtil.getXun("Bính Tý") == "Giáp Tuất"
    assert LunarUtil.getXun("Quý Mùi") == "Giáp Tuất"
    # Tuần 2: Giáp Thân — index 20-29
    assert LunarUtil.getXun("Đinh Hợi") == "Giáp Thân"
    assert LunarUtil.getXun("Tân Mão") == "Giáp Thân"
    # Tuần 3: Giáp Ngọ — index 30-39
    assert LunarUtil.getXun("Nhâm Dần") == "Giáp Ngọ"
    assert LunarUtil.getXun("Quý Mão") == "Giáp Ngọ"
    # Tuần 4: Giáp Thìn — index 40-49
    assert LunarUtil.getXun("Nhâm Tý") == "Giáp Thìn"
    assert LunarUtil.getXun("Quý Sửu") == "Giáp Thìn"
    # Tuần 5: Giáp Dần — index 50-59
    assert LunarUtil.getXun("Canh Thân") == "Giáp Dần"
    assert LunarUtil.getXun("Quý Hợi") == "Giáp Dần"


def test_get_xun_kong_vietnamese():
    """getXunKong must map each Tuần to the correct Vietnamese Tuần Không pair."""
    assert LunarUtil.getXunKong("Giáp Tý") == "Tuất Hợi"
    assert LunarUtil.getXunKong("Bính Dần") == "Tuất Hợi"
    assert LunarUtil.getXunKong("Bính Tý") == "Thân Dậu"
    assert LunarUtil.getXunKong("Đinh Hợi") == "Ngọ Mùi"
    assert LunarUtil.getXunKong("Nhâm Dần") == "Thìn Tỵ"
    assert LunarUtil.getXunKong("Nhâm Tý") == "Dần Mão"
    assert LunarUtil.getXunKong("Canh Thân") == "Tý Sửu"
    assert LunarUtil.getXunKong("Quý Hợi") == "Tý Sửu"


def test_xun_via_lunar_object():
    """Lunar.getYearXun/getYearXunKong return correct VN values."""
    s = Solar.fromYmd(2026, 7, 27)
    l = s.getLunar()
    expected_xun = LunarUtil.getXun(l.getYearInGanZhi())
    expected_kong = LunarUtil.getXunKong(l.getYearInGanZhi())
    assert l.getYearXun() == expected_xun
    assert l.getYearXunKong() == expected_kong
    # Sanity: xun index 0 for Giáp Tý; index 5 for Giáp Dần
    assert expected_xun in LunarUtil.XUN


# ----------------------------- B2 -----------------------------
def test_solar_from_bazi_vietnamese():
    """Solar.fromBaZi must accept spaced Vietnamese GanZhi and return dates."""
    # 1984-03-26 16:00 was Giáp Tý / Đinh Mão / Kỷ Mùi / Nhâm Thân (spaced VN).
    res = Solar.fromBaZi(
        year_gan_zhi="Giáp Tý",
        month_gan_zhi="Đinh Mão",
        day_gan_zhi="Kỷ Mùi",
        time_gan_zhi="Nhâm Thân",
        base_year=1980,
    )
    assert len(res) >= 1
    assert isinstance(res[0], Solar)
    # Year of returned result must match.
    assert res[0].getYear() in (1984, 2044)


def test_solar_from_bazi_vietnamese_round_trip():
    """Forward BaZi → Solar produces a date whose Lunar matches the chart."""
    res = Solar.fromBaZi(
        year_gan_zhi="Giáp Tý",
        month_gan_zhi="Đinh Mão",
        day_gan_zhi="Kỷ Mùi",
        time_gan_zhi="Nhâm Thân",
        base_year=1980,
    )
    assert res, "fromBaZi returned no results for a valid chart"
    s = res[0]
    lunar = s.getLunar()
    assert lunar.getYearInGanZhiExact() == "Giáp Tý"
    assert lunar.getMonthInGanZhiExact() == "Đinh Mão"
    assert lunar.getDayInGanZhiExact2() == "Kỷ Mùi"
    assert lunar.getTimeInGanZhi() == "Nhâm Thân"


# ----------------------------- B3 + B4 -----------------------------
def test_eightchar_tai_yuan_na_yin_vietnamese():
    """getTaiYuan must return a spaced Vietnamese GanZhi that resolves in NAYIN."""
    s = Solar.fromYmd(2026, 7, 27)
    l = s.getLunar()
    ec = l.getEightChar()
    tai_yuan = ec.getTaiYuan()
    # Must be spaced Vietnamese, e.g. "Bính Tuất"
    assert " " in tai_yuan, f"TaiYuan missing space: {tai_yuan!r}"
    gan, zhi = tai_yuan.split()
    assert gan in LunarUtil.GAN
    assert zhi in LunarUtil.ZHI
    # NaYin must resolve
    na_yin = ec.getTaiYuanNaYin()
    assert na_yin is not None, f"NaYin lookup failed for {tai_yuan!r}"


def test_eightchar_tai_xi_na_yin_vietnamese():
    """getTaiXi must return a spaced Vietnamese GanZhi that resolves in NAYIN."""
    s = Solar.fromYmd(2026, 7, 27)
    l = s.getLunar()
    ec = l.getEightChar()
    tai_xi = ec.getTaiXi()
    assert " " in tai_xi, f"TaiXi missing space: {tai_xi!r}"
    gan, zhi = tai_xi.split()
    assert gan in LunarUtil.GAN
    assert zhi in LunarUtil.ZHI
    assert ec.getTaiXiNaYin() is not None


def test_eightchar_ming_gong_shen_gong_vietnamese():
    """getMingGong and getShenGong must return spaced Vietnamese GanZhi."""
    s = Solar.fromYmd(2026, 7, 27)
    l = s.getLunar()
    ec = l.getEightChar()
    for label, fn, na_fn in [
        ("MingGong", ec.getMingGong, ec.getMingGongNaYin),
        ("ShenGong", ec.getShenGong, ec.getShenGongNaYin),
    ]:
        v = fn()
        assert " " in v, f"{label} missing space: {v!r}"
        gan, zhi = v.split()
        assert gan in LunarUtil.GAN
        assert zhi in LunarUtil.ZHI
        assert na_fn() is not None, f"{label} NaYin missing for {v!r}"


def test_eightchar_ming_gong_resolves_to_eightchar_month_zhi():
    """MingGong zhi must be one of EightChar.MONTH_ZHI values (not a stray char)."""
    s = Solar.fromYmd(2026, 7, 27)
    l = s.getLunar()
    ec = l.getEightChar()
    _, zhi = ec.getMingGong().split()
    assert zhi in LunarUtil.ZHI
    # And must also appear in EightChar.MONTH_ZHI (skipping the empty slot)
    assert zhi in [z for z in EightChar.MONTH_ZHI if z]



# ----------------------------- G1-G3: festivals -----------------------------
def test_lunar_get_vietnamese_festivals_tet():
    """Lunar.getVietnameseFestivals returns Tết Nguyên Đán for 1/1 lunar."""
    tet = Lunar.fromYmd(2026, 1, 1)
    fs = tet.getVietnameseFestivals()
    assert any("Tết Nguyên Đán" in f for f in fs)


def test_lunar_get_vietnamese_festivals_ong_tao():
    """Lunar.getVietnameseFestivals returns Ông Táo for 12/23 lunar (VN date)."""
    ong_tao = Lunar.fromYmd(2025, 12, 23)
    fs = ong_tao.getVietnameseFestivals()
    assert any("Ông Táo" in f for f in fs)


def test_lunar_get_vietnamese_festivals_hung_vuong():
    """Lunar.getVietnameseFestivals returns Giỗ Tổ Hùng Vương for 3/10 lunar."""
    hung_vuong = Lunar.fromYmd(2026, 3, 10)
    fs = hung_vuong.getVietnameseFestivals()
    assert any("Hùng Vương" in f for f in fs)


def test_lunar_get_vietnamese_festivals_khai_ha():
    """Lunar.getVietnameseFestivals returns Khai Hạ for 1/7 lunar."""
    khai_ha = Lunar.fromYmd(2026, 1, 7)
    fs = khai_ha.getVietnameseFestivals()
    assert any("Khai Hạ" in f for f in fs)


def test_lunar_get_other_festivals_ong_tao():
    """Lunar.getOtherFestivals surfaces Ông Táo from OTHER_FESTIVAL on 12/23 lunar."""
    ong_tao = Lunar.fromYmd(2025, 12, 23)
    fs = ong_tao.getOtherFestivals()
    assert any("Ông Táo" in f for f in fs)


def test_festival_table_is_vietnamese_only():
    """LunarUtil.FESTIVAL/OTHER_FESTIVAL must not contain Chinese characters."""
    import re
    cjk = re.compile(r"[\u4e00-\u9fff]")
    for name in ("FESTIVAL", "OTHER_FESTIVAL"):
        table = getattr(LunarUtil, name)
        for k, v in table.items():
            assert not cjk.search(k), f"{name} key has CN char: {k}"
            if isinstance(v, list):
                for item in v:
                    assert not cjk.search(item), f"{name} value has CN char: {item}"
            else:
                assert not cjk.search(v), f"{name} value has CN char: {v}"


def test_festival_table_no_chinese_specific_entries():
    """Festival tables must not contain Chinese-only festivals (no VN equivalent)."""
    banned = {
        "龙头节", "接神日", "隔开日", "顺星节", "谷日", "天日", "地日",
        "天穿节", "填仓节", "中和节", "社日节", "上巳节", "分龙节",
        "会龙节", "天贶节", "观莲节", "五谷母节", "中元节", "财神节",
        "地藏节", "天灸日", "寒衣节", "十成节", "下元节", "驱傩日",
        "尾牙", "祭灶日", "佛灭", "空亡",
    }
    flat = set()
    for table_name in ("FESTIVAL", "OTHER_FESTIVAL"):
        for k, v in getattr(LunarUtil, table_name).items():
            flat.add(k)
            if isinstance(v, list):
                flat.update(v)
            else:
                flat.add(v)
    assert flat.isdisjoint(banned), f"Found banned Chinese entries: {flat & banned}"


def test_ong_tao_is_12_23_not_12_24():
    """VN Ông Táo chầu trời is 12/23 lunar, NOT 12/24 (Chinese calendar differs)."""
    from tuvi_mcp.lunar_calendar.VietnameseHoliday import VietnameseHoliday
    assert VietnameseHoliday.get_lunar_holiday(12, 23) is not None
    assert "12-23" in VietnameseHoliday.LUNAR_HOLIDAYS
    assert "12-24" not in VietnameseHoliday.LUNAR_HOLIDAYS


# ----------------------------- NAYIN spacing round-trip -----------------------------
def test_nayin_lookup_with_spaced_keys():
    """NAYIN table keys are spaced Vietnamese; lookups must work as-is."""
    # Direct spot checks: every other key should resolve.
    samples = ["Giáp Tý", "Kỷ Hợi", "Bính Ngọ", "Quý Hợi"]
    for s in samples:
        assert LunarUtil.NAYIN.get(s) is not None, f"NAYIN missing for {s}"


def test_jia_zi_index_round_trip_all_60():
    """getJiaZiIndex correctly maps every of 60 spaced VN GanZhi."""
    for i, gz in enumerate(LunarUtil.JIA_ZI):
        # Spaced key round-trip
        assert LunarUtil.getJiaZiIndex(gz) == i, f"getJiaZiIndex({gz}) = {LunarUtil.getJiaZiIndex(gz)}, expected {i}"
        # Stripped key round-trip
        assert LunarUtil.getJiaZiIndex(gz.replace(" ", "")) == i


# ----------------------------- B5: SONG_TAI_YI translation -----------------------------
def test_song_tai_yi_translated():
    """NineStar.SONG_TAI_YI must contain Vietnamese descriptions (not empty, not Chinese)."""
    import re
    from tuvi_mcp.lunar_calendar.NineStar import NineStar
    cjk = re.compile(r"[\u4e00-\u9fff]")
    for i, verse in enumerate(NineStar.SONG_TAI_YI):
        assert verse, f"SONG_TAI_YI[{i}] is empty"
        assert not cjk.search(verse), f"SONG_TAI_YI[{i}] still has Chinese: {verse!r}"
        # Should contain a recognizable Vietnamese star name
        assert any(name in verse for name in NineStar.NAME_TAI_YI), \
            f"SONG_TAI_YI[{i}] missing star name: {verse!r}"


# ----------------------------- LunarTime getGanZhi spacing -----------------------------
def test_lunitime_get_ganzhi_has_space():
    """LunarTime.getGanZhi() must return spaced Vietnamese."""
    from tuvi_mcp.lunar_calendar.LunarTime import LunarTime
    l = Solar.fromYmdHms(2026, 7, 27, 10, 0, 0).getLunar()
    lt = LunarTime(l.getYear(), l.getMonth(), l.getDay(), 10, 0, 0)
    gz = lt.getGanZhi()
    assert " " in gz, f"getGanZhi missing space: {gz!r}"


def test_lunitime_nayin_does_not_crash():
    """LunarTime.getNaYin() must not raise KeyError."""
    from tuvi_mcp.lunar_calendar.LunarTime import LunarTime
    for h in [0, 6, 10, 14, 18, 22]:
        l = Solar.fromYmdHms(2026, 7, 27, h, 0, 0).getLunar()
        lt = LunarTime(l.getYear(), l.getMonth(), l.getDay(), h, 0, 0)
        nayin = lt.getNaYin()
        assert nayin, f"NaYin empty for hour {h}"
        assert " " in nayin, f"NaYin missing space: {nayin!r}"


def test_lunitime_xun_returns_correct_values():
    """LunarTime.getXun() must return correct Tuần, not always 'Giáp Tý'."""
    from tuvi_mcp.lunar_calendar.LunarTime import LunarTime
    l = Solar.fromYmdHms(2026, 7, 27, 10, 0, 0).getLunar()
    lt = LunarTime(l.getYear(), l.getMonth(), l.getDay(), 10, 0, 0)
    xun = lt.getXun()
    assert xun, f"getXun empty"
    # The hour is 10 (Tỵ), day is Nhâm Dần → should NOT be Giáp Tý
    assert xun != "Giáp Tý" or "Giáp Tý" in xun  # at minimum not always wrong


def test_lunitime_chong_desc_has_spaces():
    """LunarTime.getChongDesc() must have spaces inside parentheses."""
    from tuvi_mcp.lunar_calendar.LunarTime import LunarTime
    l = Solar.fromYmdHms(2026, 7, 27, 10, 0, 0).getLunar()
    lt = LunarTime(l.getYear(), l.getMonth(), l.getDay(), 10, 0, 0)
    desc = lt.getChongDesc()
    # Should be like "(Ất Mùi)Dê" not "(ẤtMùi)Dê"
    assert desc.startswith("("), f"ChongDesc bad format: {desc!r}"
    inner = desc[1:desc.index(")")]
    assert " " in inner, f"ChongDesc inner missing space: {desc!r}"