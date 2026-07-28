# -*- coding: utf-8 -*-
from ..TaoFestival import TaoFestival


class TaoUtil:
    """
    Taoist calendar utility
    """

    # Three meetings day
    SAN_HUI = ("1-7", "7-7", "10-15")

    # Three origin day
    SAN_YUAN = ("1-15", "7-15", "10-15")

    # Five La day
    WU_LA = ("1-1", "5-5", "7-7", "10-1", "12-8")

    # Dark Wu
    AN_WU = ("Mùi", "Tuất", "Thìn", "Dần", "Ngọ", "Tý", "Dậu", "Thân", "Tỵ", "Hợi", "Mão", "Sửu")

    # Eight meetings day
    BA_HUI = {
        "Bính Ngọ": "天会",
        "Nhâm Ngọ": "地会",
        "Nhâm Tý": "人会",
        "Canh Ngọ": "日会",
        "Canh Thân": "月会",
        "Tân Dậu": "星辰会",
        "Giáp Thìn": "五行会",
        "Giáp Tuất": "四时会"
    }

    # Eight festivals day
    BA_JIE = {
        "Lập Xuân": "东北方度仙上圣天尊同梵炁始青天君下降",
        "Xuân Phân": "东方玉宝星上天尊同青帝九炁天君下降",
        "Lập Hạ": "东南方好生度命天尊同梵炁始丹天君下降",
        "Hạ Chí": "南方玄真万福天尊同赤帝三炁天君下降",
        "Lập Thu": "西南方太灵虚皇天尊同梵炁始素天君下降",
        "Thu Phân": "西方太妙至极天尊同白帝七炁天君下降",
        "Lập Đông": "西北方无量太华天尊同梵炁始玄天君下降",
        "Đông Chí": "北方玄上玉宸天尊同黑帝五炁天君下降"
    }

    FESTIVAL = {}

    def __init__(self):
        pass
