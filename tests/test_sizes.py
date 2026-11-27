"""The 尺码 tab (sizes.html): type a size in one box, read the other boxes.

The table below is what the page showed on 2026-11-27 with the brand charts
copied that day. If a chart is changed on purpose, change the table here too.
Boxes: 0 = mm, 1 = EU, 2 = UK, 3 = US. Default chart 自动.
"""
from browser import Journal

# (box typed in, text typed) -> (mm, EU, UK, US shown, chart used)
AUTO = [
    ((1, "38"), ("253", "38", "5", "5-5.5", "Birkenstock")),       # EU: Birkenstock first (adults)
    ((1, "42"), ("280", "42", "8", "9-9.5", "Birkenstock")),
    ((1, "25"), ("167", "25", "7.5", "8", "Clarks")),               # kids' EU: Clarks
    ((2, "7"), ("273", "41", "7", "8", "Clarks")),                  # UK: Clarks
    ((3, "9"), ("283", "42.5", "8", "9", "Nike")),                  # US: Nike
    ((0, "25"), ("25", "37.5", "4.5", "7", "Clarks")),              # under 60 in the mm box = cm
]


def boxes(j, box, text):
    j.pg.fill(f"#b{box}", text)
    return tuple(j.pg.input_value(f"#b{k}") for k in range(4))


def test_auto_chart_table():
    for (box, text), (*want, chart) in AUTO:
        j = Journal("2026-11-27", page="sizes.html")     # a fresh page each time: the UK/US switches remember the last part used
        got = boxes(j, box, text)
        assert got == tuple(want), f"typed {text} in box {box}: {got}, expected {tuple(want)}"
        assert chart in j.pg.text_content("#src"), j.pg.text_content("#src")
        j.done()


def test_mm_is_eu_divided_by_015():
    # the owner's one formula: mm = EU / 0.15 (shoe/last length)
    j = Journal("2026-11-27", page="sizes.html")
    for eu in ["36", "38", "40", "42", "44"]:
        assert boxes(j, 1, eu)[0] == str(round(int(eu) / 0.15)), eu
    j.done()


def test_between_two_sizes_follows_the_half_size_rule():
    j = Journal("2026-11-27", page="sizes.html")
    boxes(j, 1, "18")                                   # kids: one size up
    assert "童鞋取大一码：18.5" in j.pg.text_content("#near"), j.pg.text_content("#near")
    j.done()


def test_every_chart_opens():
    j = Journal("2026-11-27", page="sizes.html")
    for i in range(j.js("CHARTS.length")):
        j.pg.select_option("#chart", str(i))
        assert boxes(j, 1, "40")[1] == "40"
    j.done()
