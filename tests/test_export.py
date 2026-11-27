"""The 日常清单 Excel download, with an imported file (tests/todo_file.py, made up).

Rules (README "日常清单 Excel"): the 01 sheets follow the code's letter; unreadable codes go on their
own sheet and aren't counted; oldest code first; each task keeps its row's look and comment;
02新增统计 takes the file's own month layout (incl. 未完成 rows), from the file's first month.
"""
import os
import tempfile

import openpyxl

import todo_file
from browser import Journal

TMP = tempfile.mkdtemp()
_cache = {}


def imported(day="2026-11-27"):
    """The page with the made-up file imported (confirm answered OK)."""
    j = Journal(day)
    j.pg.click("#tabTodo")
    j.pg.set_input_files("#xlsxIn", todo_file.make(os.path.join(TMP, "日常清单-B01组-测试-20261126.xlsx")))
    j.pg.wait_for_function("TD().items.length > 0")
    return j


def exported():
    """Import the file, download it, open the download (once per run)."""
    if "wb" not in _cache:
        j = imported()
        with j.pg.expect_download() as d:
            j.js("downloadXlsx()")
        path = os.path.join(TMP, "out.xlsx")
        d.value.save_as(path)
        _cache["wb"], _cache["path"] = openpyxl.load_workbook(path), path
        j.done()
    return _cache["wb"]


def codes(ws):
    return [ws.cell(r, 1).value for r in range(2, ws.max_row + 1)]


def row_of(ws, code):
    return next(r for r in range(2, ws.max_row + 1) if ws.cell(r, 1).value == code)


def test_sheets_follow_the_code_letter_oldest_first():
    wb = exported()
    assert codes(wb["01日常清单-直接上级"]) == ["1102A-01", "1110Z-01", "1124G-01"]
    assert codes(wb["01日常清单-间接上级"]) == ["1120-01", "1125-02"]       # no letter = 大老板's own list


def test_unreadable_codes_get_their_own_sheet():
    wb = exported()
    assert wb.sheetnames[-1] == "旧编码-无法识别"
    ws = wb["旧编码-无法识别"]
    assert codes(ws) == ["1117T01", "G20-014"]
    assert [c.value for c in ws[1]][:6] == todo_file.HEAD                    # same columns as 01直接上级


def test_unreadable_codes_not_counted_and_not_shown():
    j = imported()
    # import day: G20-014 has no date, so it isn't 今天收到
    assert j.js("[todoCount('tdIn'), todoCount('tdOpen'), todoCount('tdBOpen')]") == [0, 2, 2]
    assert "1117T01" not in j.pg.inner_text("#todoCols") and "G20-014" not in j.pg.inner_text("#todoCols")
    assert "旧编码" in j.pg.inner_text(".unread summary") and "2 条" in j.pg.inner_text(".unread summary")
    j.done()


def test_each_task_keeps_its_look_and_comment():
    wb = exported()
    ws = wb["01日常清单-间接上级"]
    r = row_of(ws, "1120-01")               # moved from 01直接上级, yellow, with a comment
    assert ws.cell(r, 2).fill.fgColor.rgb == todo_file.YELLOW
    assert ws.cell(r, 2).font.name == "微软雅黑"
    assert ws.row_dimensions[r].height == 40
    assert ws.cell(r, 6).comment and "老板的原话：先做这个" in ws.cell(r, 6).comment.text
    assert not any(c.comment for row in wb["01日常清单-直接上级"].iter_rows() for c in row)   # it left the old sheet
    d = wb["01日常清单-直接上级"]
    assert d.column_dimensions["B"].width == 60 and d.freeze_panes == "A2"
    assert d.cell(1, 1).font.bold and d.auto_filter.ref == f"A1:F{d.max_row}"


def stats(wb, month):
    out = {}
    for row in wb["02新增统计"].iter_rows(min_row=2):
        if str(row[1].value) == month:
            out[str(row[3].value)] = row
    return out


def test_stats_keep_the_files_layout_and_colours():
    wb = exported()
    s = stats(wb, "22611")
    assert list(s) == todo_file.LAYOUT
    assert s["来自直接上级未完成"][10].fill.fgColor.rgb == todo_file.YELLOW
    assert s["A来自直接上级-单独通知"][10].fill.fgColor.rgb in (None, "00000000")
    months = sorted({str(r[1]) for r in wb["02新增统计"].iter_rows(min_row=2, values_only=True)})
    assert months == ["22610", "22611"]                                     # from the file's first month


def test_stats_counts():
    s = stats(exported(), "22611")
    day = lambda label, d: s[label][3 + d].value
    assert day("A来自直接上级-单独通知", 2) == 1                 # 1102A-01
    assert day("A来自直接上级-全组大群通知", 10) == 1 and day("A来自直接上级-全组大群通知", 24) == 1
    assert day("B来自间接上级-单独通知", 20) == 1 and day("B来自间接上级-单独通知", 25) == 1
    assert day("A来自直接上级-单独通知", 17) == 0                # 1117T01 is unreadable: not counted
    assert day("A来自直接上级-单独通知", 28) is None             # Saturday
    assert s["A来自直接上级-汇总"][4].value == "=IF(COUNT(E{0}:E{1}),SUM(E{0}:E{1}),\"\")".format(s["A来自直接上级-单独通知"][0].row, s["A来自直接上级-组内组小群通知"][0].row)
    # 未完成 = open at the end of the day
    assert [day("来自直接上级未完成", d) for d in (3, 5, 10, 26)] == [1, 0, 1, 2]
    assert [day("来自间接上级未完成", d) for d in (19, 20, 26)] == [0, 1, 2]


def test_download_reads_back_the_same():
    exported()
    j = Journal("2026-11-27")
    j.pg.click("#tabTodo")
    j.pg.set_input_files("#xlsxIn", _cache["path"])
    j.pg.wait_for_function("TD().items.length > 0")
    got = j.js("TD().items.map(x => [x.code, sheetOf(x)]).sort()")
    assert got == sorted([["1102A-01", "direct"], ["1110Z-01", "direct"], ["1124G-01", "direct"], ["1120-01", "indirect"],
                          ["1125-02", "indirect"], ["1117T01", "unread"], ["G20-014", "unread"]]), got
    j.done()


def test_download_warns_when_a_task_is_missing():
    # every download reads its own file back: no warning normally; a task gone from the list -> warning naming it
    j = imported()
    with j.pg.expect_download():
        j.js("downloadXlsx()")
    assert not [m for m in j.dialogs if "任务数对不上" in m], j.dialogs
    j.js("TD().items.splice(TD().items.findIndex(x => x.code === '1125-02'), 1)")       # lost, not deleted with ×
    with j.pg.expect_download():                     # the confirm() is answered OK = 仍然下载
        j.js("downloadXlsx()")
    warn = [m for m in j.dialogs if "任务数对不上" in m]
    assert warn and "清单里有 6 条，应该有 7 条" in warn[0], j.dialogs
    j.done()
