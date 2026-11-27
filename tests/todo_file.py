"""A made-up 日常清单 Excel, built like the group's real files (no real data):

01直接上级 and 01间接上级 (columns 编码号 描述 状态 打X登记日期 先前已传 进展备注, frozen header,
filter on 先前已传), a yellow row with an Excel comment, old-style codes, and 02新增统计 with the
layout of a long-used file: A单独/A大群/A小群/A汇总/直接上级未完成/B单独/B汇总/间接上级未完成 per month,
未完成 rows yellow, 汇总 rows as formulas. Pretend today: Friday 2026-11-27.
"""
import datetime

import openpyxl
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

YELLOW = "FFFFFF00"
HEAD = ["编码号", "描述", "状态", "打X登记日期", "先前已传", "进展备注"]
THIN = Side(style="thin")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
FONT = Font(name="微软雅黑", size=11)

# (code, description, status, closed date, sent, notes, yellow?, comment)
DIRECT = [
    ("1124G-01", "测试任务甲", "", None, None, "1124已查收1201", False, None),
    ("1120-01", "没有字母的编码（老板单独）", "", None, None, "1120已查收1203", True, "老板的原话：先做这个"),
    ("1117T01", "旧格式编码", "OK", datetime.date(2025, 11, 18), 1, "1117已查收\n1118已完成X", False, None),
    ("G20-014", "没有日期的编码", "", None, None, "", False, None),
    ("1102A-01", "组长单独通知", "OK", datetime.date(2026, 11, 5), 1, "1102已查收\n1105已完成X", False, None),
]
INDIRECT = [
    ("1125-02", "老板单独通知", "", None, None, "1125已查收1202", False, None),
    ("1110Z-01", "全组通知，却在间接上级表里", "", None, None, "1110已查收1204", False, None),
]
LAYOUT = ["A来自直接上级-单独通知", "A来自直接上级-全组大群通知", "A来自直接上级-组内组小群通知", "A来自直接上级-汇总",
          "来自直接上级未完成", "B来自间接上级-单独通知", "B来自间接上级-汇总", "来自间接上级未完成"]


def list_sheet(ws, rows):
    ws.append(HEAD)
    for c in ws[1]:
        c.font = Font(name="微软雅黑", size=11, bold=True)
        c.border = BOX
    for code, desc, st, xd, sent, notes, yellow, note in rows:
        ws.append([code, desc, st, xd, sent, notes])
        r = ws.max_row
        for c in ws[r]:
            c.font, c.border = FONT, BOX
            c.alignment = Alignment(vertical="center", wrap_text=True)
            if yellow:
                c.fill = PatternFill("solid", fgColor=YELLOW)
        ws.cell(r, 4).number_format = "mm-dd-yy"
        ws.row_dimensions[r].height = 40
        if note:
            ws.cell(r, 6).comment = Comment(note, "测试员")
    for col, w in zip("ABCDEF", [11, 60, 10, 16, 10, 40]):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:F{ws.max_row}"


def make(path):
    wb = openpyxl.Workbook()
    list_sheet(wb.active, DIRECT)
    wb.active.title = "01日常清单-直接上级"
    list_sheet(wb.create_sheet("01日常清单-间接上级"), INDIRECT)
    ws = wb.create_sheet("02新增统计")
    ws.append(["年度", "月份", "统计", "新增编码记录数"] + [f"D {d:02d}" for d in range(1, 32)] + ["月汇总"])
    for month in (22610, 22611):
        start = ws.max_row + 1
        for i, label in enumerate(LAYOUT):
            r = start + i
            ws.append([227 if month == 22611 else 226, month, 1, label])
            if "汇总" in label:
                first = start if label[0] == "A" else start + 5
                last = start + 2 if label[0] == "A" else start + 5
                ws.cell(r, 3).value = f"=SUM(C{first}:C{last})"
            for c in range(1, 37):
                cell = ws.cell(r, c)
                cell.border, cell.font = BOX, Font(name="等线", size=10)
                if "未完成" in label:
                    cell.fill = PatternFill("solid", fgColor=YELLOW)
    ws.freeze_panes = "E2"
    wb.create_sheet("03系统问题反馈")
    wb.save(path)
    return path
