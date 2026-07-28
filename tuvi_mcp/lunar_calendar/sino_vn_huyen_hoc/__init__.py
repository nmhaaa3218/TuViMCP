# -*- coding: utf-8 -*-
"""
sino_vn_huyen_hoc - Sino-Vietnamese Huyền Học (Sino-VN metaphysics)

This subpackage hosts the Tứ Trụ / Bát Tự (四柱八字) system widely practiced
in Vietnam as a supplementary tool of Tử Vi. Although widely recognized and
practiced by Vietnamese phong thủy masters and Tử Vi readers, its theoretical
foundation is rooted in Chinese Đông Á metaphysics, NOT native Vietnamese
folk religion (tín ngưỡng dân gian Việt Nam such as thờ Mẫu, Tứ Phủ, thờ
Hùng Vương, etc.).

Imported directly:

    from tuvi_mcp.lunar_calendar.sino_vn_huyen_hoc import EightChar

Background:
    - "Tứ Trụ" (four pillars) here = 4 pillars of destiny: year/month/day/hour
      Can Chi pillars. Do NOT confuse with "Tứ Trụ sử học" (4 pillars of
      historical studies) or "Tứ Bất Tử" (four Vietnamese folk immortals).
    - Self-identified by Vietnamese Tử Vi literature as Chinese-origin
      ("Phát triển mạnh ở Trung Hoa và Nhật Bản").
    - Pure Vietnamese folk religion equivalents: Tứ Bất Tử (Tản Viên, Chử Đồng
      Tử, Liễu Hạnh, Phù Đổng), thờ Mẫu/Tứ Phủ, Lễ Vu Lan bản địa.
"""
from .EightChar import EightChar

__all__ = ["EightChar"]
