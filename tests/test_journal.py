"""The journal tab: the text the page writes from the form, and what happens on a new day.

Dates used: Wed 2026-11-25, Thu 11-26, Fri 11-27 (week 48), Mon 11-30 (week 49).
The page starts with the template's example journal (made-up names), so
these tests change only the part they check.
"""
from browser import Journal

# an item as the page stores it (start date, category, text, plan date)
ITEM = "(start, cat, text, plan, edited = '', closed = '') => ({ id: 'i' + Math.random(), start, cat, text, plan, edited, closed })"


def test_example_journal_loads():
    j = Journal("2026-11-27")
    t = j.text()
    assert t[0] == "@邮件回复1h（MDC，TTT为主）", t[0]
    assert "@总计7h15+" in t
    assert "▲提醒：本周第48周" in t
    assert t[-1] == "*日常清单表：若有未完成的记录，无论有无更新，每周一传递；"
    j.done()


def test_hours_written_like_the_group_leader():
    # one entry: its text in brackets; several: each with its time; 4h15 = 4 h 15 min; 45 = 45 min
    j = Journal("2026-11-27")
    j.set("S.entries = [{cat: 0, text: '寄样给ABC', min: 255, sign: ''}, {cat: 1, text: 'A款', min: 45, sign: ''},"
          " {cat: 1, text: 'B', min: 30, sign: '+'}]")
    t = j.text()
    assert t[0] == "@邮件回复4h15（寄样给ABC）", t[0]
    assert t[1] == "@立项开发1h15+（A款45，B 30+）", t[1]
    assert t[2] == "@搜款推客0h", t[2]
    assert t[8] == "@总计5h30+", t[8]
    j.done()


def test_plus_today_minus_the_next_day():
    j = Journal("2026-11-26")
    j.set(f"const it = {ITEM}; S.focus = [it('1120', '品质', '鞋底开胶，1126已换料', '1203', today())]")
    assert "+1120品质：鞋底开胶，1126已换料1203" in j.text()
    j.open("2026-11-27")
    assert "-1120品质：鞋底开胶，1126已换料1203" in j.text()
    j.done()


def test_x_item_shown_on_its_day_then_gone():
    j = Journal("2026-11-26")
    j.set(f"const it = {ITEM}; S.focus = [it('1120', '', '样品寄出', 'X', today(), today())]")
    assert "+1120样品寄出X" in j.text()
    j.open("2026-11-27")
    assert not [l for l in j.text() if "样品寄出" in l]
    j.done()


def test_plan_date_must_be_after_today():
    j = Journal("2026-11-27")
    j.set(f"const it = {ITEM}; S.focus = [it('1120', '', '今天到期', '1127'), it('1120', '', '明天', '1128')]")
    bad = dict(j.js("genLines().filter(l => l.sec === 'focus').map(l => [l.t, l.bad])"))
    assert bad["-1120今天到期1127"] == "计划日期要晚于今天"
    assert bad["-1120明天1128"] == ""
    j.done()


def test_space_after_date_only_before_letter_or_digit():
    j = Journal("2026-11-27")
    j.set(f"const it = {ITEM}; S.focus = [it('1120', '', 'CGA样品', '1201'), it('1120', '', '工厂回复', '1201')]")
    t = j.text()
    assert "-1120 CGA样品1201" in t and "-1120工厂回复1201" in t
    j.done()


def test_new_day_starts_empty_with_grey_hints():
    j = Journal("2026-11-25")
    j.set("S.entries = [{cat: 0, text: '回邮件', min: 60, sign: ''}]; S.f.d2 = '无'; S.f.w5 = '还有一笔'")
    j.open("2026-11-26")
    s = j.js("({ entries: S.entries.length, d2: S.f.d2, prev: S.prev.f.d2, w5: S.f.w5 })")
    assert s == {"entries": 0, "d2": "", "prev": "无", "w5": "还有一笔"}, s      # weekly boxes stay until Friday
    assert "@总计" in j.text()[8]
    j.done()


def test_friday_starts_the_weekly_review():
    j = Journal("2026-11-26")
    j.set("S.f.w1n = '2'; S.f.w15n = '3'")
    j.open("2026-11-27")
    s = j.js("({ w1n: S.f.w1n, w15p: S.f.w15p, weekDate: S.weekDate })")
    assert s == {"w1n": "", "w15p": "3", "weekDate": "2026-11-27"}, s     # this week's 超30天 becomes 上周
    assert "●●每周回顾：以下统计值每周5更新：1127更新" in j.text()
    j.done()


def test_new_week_moves_w_reminders():
    j = Journal("2026-11-27")
    j.set(f"const it = {ITEM}; S.remind = [it('W48', '', '周一传未完日常清单表', '1130')]")
    j.open("2026-11-30")
    t = j.text()
    assert "▲提醒：本周第49周" in t
    assert "-W49周一传未完日常清单表1207" in t, [l for l in t if "W4" in l]
    j.done()


def test_c1_count_by_short_name():
    # ABC1/ABCB on one block = 2 clients; the same 简称 on another block counts once
    j = Journal("2026-11-27")
    j.set("S.clients = [{name: 'ABC1/ABCB', role: '前', lines: [{product: '鞋1', items: []}]},"
          " {name: 'ABC1', role: '后', lines: [{product: '鞋2', items: []}]}]")
    assert "●C1有单老客：2客" in j.text()
    j.done()


def test_import_reads_back_what_the_page_wrote():
    # the page's own journal, pasted into 导入现有日志, must give the same journal back
    # (import doesn't know what was changed today, so + items come back as -: start with none)
    j = Journal("2026-11-27")
    j.set("[...S.focus, ...S.remind, ...S.clients.flatMap(c => c.lines.flatMap(l => l.items))].forEach(x => { x.edited = ''; });"
          " Object.keys(S.f).forEach(k => { S.f[k] = S.f[k].replace(NOTE_RE, ''); })")
    r = j.js("""() => { const t = journalText(), p = parseJournal(t); S = p.s; render();
                        return { missed: p.missed, before: t.split('\\r\\n'), after: journalText().split('\\r\\n') }; }""")
    assert r["missed"] == [], r["missed"]
    diff = [(a, b) for a, b in zip(r["before"], r["after"]) if a != b]
    assert not diff and len(r["before"]) == len(r["after"]), diff[:3]
    j.done()


def test_import_keeps_unread_lines_as_own_lines():
    j = Journal("2026-11-27")
    r = j.js("""() => { const t = journalText().split('\\r\\n'); t.splice(12, 0, '这行谁也看不懂'); const p = parseJournal(t.join('\\n'));
                        S = p.s; render(); return { missed: p.missed, after: journalText().split('\\r\\n') }; }""")
    assert r["missed"] == ["这行谁也看不懂"], r["missed"]
    assert r["after"][12] == "这行谁也看不懂", r["after"][10:14]       # kept where it was
    j.done()


def test_own_line_stays_under_its_line():
    j = Journal("2026-11-27")
    j.set(f"const it = {ITEM}; S.focus = [it('1120', '', '第一件', '1201'), it('1120', '', '第二件', '1201'), it('1120', '', '第三件', '1201')];"
          " ensureIds(); S.extra = [{ id: 'e1', after: 'i:' + S.focus[1].id, sec: 'focus', text: '我自己的一行' }]")
    under = lambda: (lambda t: t[t.index("我自己的一行") - 1])(j.text())
    assert under() == "-1120第二件1201"
    # the line it was under is gone: it stays above the line that was below it
    j.set("S.focus.splice(1, 1)")
    assert under() == "-1120第一件1201"
    # both lines around it gone: end of its section, in red
    j.set("S.focus.splice(1, 1)")
    bad = j.js("genLines().find(l => l.t === '我自己的一行').bad")
    assert bad.startswith("它上下的行都没了"), bad
    j.done()


def test_backup_and_restore():
    j = Journal("2026-11-27")
    j.set("S.f.w5 = '备份测试'")
    with j.pg.expect_download() as d:
        j.pg.click("#export")
    path = d.value.path()
    k = Journal("2026-11-27")        # another, empty browser
    k.pg.set_input_files("#import", path)
    k.pg.wait_for_timeout(300)
    assert k.js("S.f.w5") == "备份测试"
    assert k.text() == j.text()
    j.done(), k.done()
