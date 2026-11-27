"""Every tab of the main page opens without a script error, and the 评估单 text reads back."""
from browser import Journal


def test_all_tabs_open():
    j = Journal("2026-11-27")
    tabs = j.js("[...document.querySelectorAll('[id^=tab]')].map(b => b.id)")
    assert len(tabs) >= 4, tabs
    for t in tabs:
        j.pg.click("#" + t)
        j.pg.wait_for_timeout(200)
    j.done()      # fails if any tab raised a script error


def test_erp_and_sizes_pages_load():
    for page in ["erp.html", "sizes.html"]:
        Journal("2026-11-27", page=page).done()


def test_eval_text_reads_back():
    # 评估单: the text the page writes, read again by 导入txt, gives the same text
    j = Journal("2026-11-27")
    r = j.js("""() => { const e = evNew(); Object.assign(e, { style: 'ZZZ1', title: '测试凉鞋', qty: '2双', got: '1126', len: '242', fw: '90', bw: '70',
                          thick: '25', hard: '45', weight: '38#/150g', fit: '合脚', last: '无' });
                        e.points = [{ sign: '+', text: '颜色好看', names: ['测试员'] }, { sign: '-', text: '底太硬', names: [] }];
                        const t = evText(e), p = evParse(t, evFile(e));
                        return { ok: p.ok, same: evText(p.e) === t, t, back: evText(p.e), file: evFile(e) }; }""")
    assert r["ok"] and r["same"], (r["t"], r["back"])
    assert r["file"] == "鞋1评估单-ZZZ1-测试凉鞋.txt", r["file"]
    j.done()
