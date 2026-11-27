"""The 日常清单 tab: codes in pasted messages, status, the journal's counts line, the Excel download.

Made-up tasks only. Codes: MMDD + letter + "-" + number (1124G-02). Letters
of group B01 (SOURCES in the page): none = 大老板 (his own list, 01间接上级),
G = 大老板 to the whole group, A = 组长, Z = 全组通知, X = 小组通知.
"""
import openpyxl

from browser import Journal

# a task as the page stores it
TASK = "(code, notes, got, more = {}) => Object.assign({ code, desc: '描述', notes, xDate: '', sent: 0, okSent: false, got }, more)"


def tasks(j, *rows):
    """Replace the to-do list with these tasks: (code, notes, got date[, extra fields])."""
    j.js(f"rows => {{ const t = {TASK}; TD().items = rows.map(r => t(...r)); TD().items.forEach(syncOk); save(); }}", list(rows))


def test_codes_found_anywhere_in_a_message():
    j = Journal("2026-11-27")
    got = j.js("parseMessages('大老板：1124G-2 下周一前回复样品意见\\n补充：要照片\\n组长 1125A-01，报价单发我')")
    assert [x["code"] for x in got] == ["1124G-02", "1125A-01"], got
    assert "下周一前回复样品意见 补充：要照片" in got[0]["desc"], got[0]["desc"]      # the line after belongs to it
    j.done()


def test_status_ok_and_g():
    # 须知 5: OK when the last note line ends in X; G when a note line starts with today's date
    j = Journal("2026-11-27")
    s = j.js("""[{ notes: '1124已查收\\n1126已回复X' }, { notes: '1124已查收\\n1127在等工厂1201' }, { notes: '1124已查收1201' }]
               .map(x => status(x))""")
    assert s == ["OK", "G", ""], s
    j.done()


def test_journal_line_counts():
    j = Journal("2026-11-27")      # Friday
    tasks(j, ("1127A-01", "1127已查收1201", "2026-11-27"),            # came in today
             ("1120G-01", "1120已查收\n1127已回复X", "2026-11-20"),    # closed today
             ("1118Z-01", "1118已查收1203", "2026-11-18"))             # still open
    assert j.js("[todoCount('tdIn'), todoCount('tdDone'), todoCount('tdOpen'), todoCount('tdSent')]") == [1, 1, 2, "未传"]
    assert "*组内日常清单表：1127当天接收1，当天完成1，未结2，传递：未传" in j.text()
    j.done()


def test_nothing_new_means_wuchuan_except_monday_with_open_tasks():
    j = Journal("2026-11-27")      # Friday: nothing in, nothing closed -> 无传
    tasks(j, ("1118Z-01", "1118已查收1203", "2026-11-18"))
    assert j.js("todoCount('tdSent')") == "无传"
    j.open("2026-11-30")           # Monday: open tasks are sent every Monday -> 未传
    assert j.js("todoCount('tdSent')") == "未传"
    j.done()


def test_boss_list_has_its_own_line():
    j = Journal("2026-11-27")
    tasks(j, ("1127-01", "1127已查收1201", "2026-11-27", {"sheet": "indirect"}),
             ("1127A-01", "1127已查收1201", "2026-11-27"))
    t = j.text()
    assert "*组内日常清单表：1127当天接收1，当天完成0，未结1，传递：未传" in t
    assert "*老板日常清单表：1127当天接收1，当天完成0，未结1，传递：未传" in t
    j.done()


def download(j):
    """Press 下载Excel and open the file."""
    with j.pg.expect_download() as d:
        j.js("downloadXlsx()")
    path = str(d.value.path()) + ".xlsx"
    d.value.save_as(path)
    return openpyxl.load_workbook(path)


def stats(wb, month):
    """02新增统计 of one month (e.g. '22611'): {row label: [day 1 .. day 31]}."""
    out = {}
    for row in wb["02新增统计"].iter_rows(min_row=2, values_only=True):
        if str(row[1]) == month:
            out[str(row[3]).strip()] = list(row[4:35])
    return out


def test_excel_tasks_and_new_counts():
    j = Journal("2026-11-27")
    tasks(j, ("1124G-01", "1124已查收1201", "2026-11-24"),
             ("1124G-02", "1124已查收\n1126已回复X", "2026-11-24"),
             ("1125A-01", "1125已查收1202", "2026-11-25"),
             ("1126-01", "1126已查收1203", "2026-11-26", {"sheet": "indirect"}))
    wb = download(j)
    rows = [r for r in wb["01日常清单-直接上级"].iter_rows(min_row=2, values_only=True) if r[0]]
    assert sorted(r[0] for r in rows) == ["1124G-01", "1124G-02", "1125A-01"], rows
    s = stats(wb, "22611")       # 月份 = 2 + YY + MM: November 2026 = 22611
    a1, a2, b1 = s["A来自直接上级-单独通知"], s["A来自直接上级-全组大群通知"], s["B来自间接上级-单独通知"]
    assert (a2[23], a1[24], b1[25]) == (2, 1, 1), (a2[20:27], a1[20:27], b1[20:27])
    assert a1[22] == 0 and a1[27] is None and a1[28] in (None, ""), a1[20:30]   # past weekday 0, Sat empty
    j.done()
