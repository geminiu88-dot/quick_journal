# 日志 (quick_journal)

PC page for the BC team's daily journal (日志格式-BC组员). A plain form on the
left (yellow boxes are typed, red means "check this"), the journal text in the
exact format on the right, made from the form. 「复制日志」 copies that text.
(Since 2026-11-17 this is the main page; `preview/` only forwards to it.)

- **Holds no data.** Everything is kept in the browser on that PC
  (localStorage, key `journal-bc-v1`). Nothing is uploaded anywhere. Clearing
  the browser's data wipes it, so use 「备份到文件」 now and then
  (「从备份恢复」 puts it back). Keep the file in one fixed place.
- **One file, no libraries,** works offline: double-click `index.html`
  (Chrome or Edge).
- **Hours** are a list of time entries (今日工时, like a timesheet app):
  category, what you did, hours + minutes from menus, optional +/-. The @
  lines are written from them in the group leader's format (`4h15` = 4 h 15
  min): one entry -> its text in brackets, several -> each with its time.
  Old typed hours (imported journals) become entries once (`migrateHours`).
  「格式范本」 shows the group's example journal and rules.
- **Automatic:** date codes (MMDD), hours total, ISO week no., `+`/`-`
  (`+` = item changed today), plan dates checked (must be after today), items
  ended with `X` disappear the next day, 登记 counts per category, client counts.
- **A new day** (first time the page is opened after the last entry; days not
  opened don't count): hours and ▲每日回顾 start empty, last values shown in
  grey. **Friday:** ●●每周回顾 starts empty and is dated today; its counts
  follow the items that day, then stay. **First entry of a new week:** `W..`
  reminders get the new week no. and next Monday as plan date.
- 「导入现有日志」 reads a pasted journal; tolerant of spaces and half/full-width
  punctuation, lists every line it can't place (no guessing).
- 「以前的日志」: the text of each day, last 60 days.
- **Own lines:** every line of the journal text has a grey dot on its left
  (＋ under the mouse): it adds a line of your own right under it, exactly
  as typed, kept every day until deleted (click to edit, × to delete). It
  stays under the line it was added to (lines have stable keys); if that
  line is gone, above the line that was below it; if both are gone, at the
  end of its section in red. 移 puts it under another line. Stored in
  `S.extra`.
- **Import** (导入现有日志): marked lines (@ ▲ ● * + -) are read by their marker. In the
  C1 block (no markers): a line with 双 = quantity line (read only in the page's own
  wording, else kept as typed), 3 capitals in a row = client line (name = all before
  前/后), else a product line. 检查 lists the client block's lines with a tick each
  (ticked = client) to fix misreads. Unread lines are kept as own lines.
- **Boss list**: items on 01间接上级 are counted on their own daily line under
  组内日常清单表 (*老板日常清单表：…，传递：无传 when nothing came in or closed today), only when that list has items; the group
  line counts 01直接上级 only.
- **Import, more:** fixed lines worded a bit differently get a looser second read
  (separators/units may differ, number boxes take only numbers) and are written back in
  the template's words; if even that fails, the line is kept as typed (`S.raw`) until a
  box is filled. 检查 shows the pasted text beside the 格式范本: red = not read, yellow =
  kept as typed. ●/●● titles both work. A space after an item's date only before a
  letter/digit.
- **Plan date:** typed as 4 digits (MMDD); the date it means is spelled out next to it.
- **传递:** time if sent today, else 无传 when nothing came in or closed today (Mondays:
  and nothing open), else 未传. C1 count = distinct 简称 (ABC1/ABCB = 2).
- **Click a journal line** to scroll the form to what makes it (thin blue box).
- **最近更新** (top right): the last 20 commits of this repo, read from the
  GitHub API on click (needs internet), with a link to the commits page.
- The fixed lines (labels, boxes, counts) are the `DAILY` / `WEEKLY` lists at
  the top of the script; the importer reads lines with the same lists.
  Only the values are boxes (numbers side by side, text below); the words
  around them come from these lists. 上周 in 超30天样单数 is filled each Friday
  from the week before. The template's notes （仅前道业务） / （仅有立项业务） are
  left out of the generated lines.
- **日常清单 tab** (the coded to-do list from the bosses). Paste messages: a
  code like `1019G-02` is found anywhere in a line (MMDD + letter + `-` + the
  day's number); each line with a code starts a new item. The letter says who
  sent it: `SOURCES` at the top of the to-do script (group B01's letters,
  other groups may differ). Status follows 须知 5: `OK` when the last note line
  ends in X (打X登记日期 = that day), `G` when a note line starts with today's
  date. 先前已传 = 1 (row hidden by the filter) at the first download after the day it was closed (打X登记日期 before today; 须知 6). The journal's
  `*组内日常清单表` line is filled from this list.
  The big boss is everyone's direct boss too: `G` (to the whole group) goes on
  01直接上级, no letter (to one person) on his own sheet, 01间接上级. A file
  without a 01间接上级 sheet has no boss list: no boss line, no column, no B rows
  in 02新增统计, and codes with no letter count as A 单独通知.
  The sheet a task is on follows its code, not the sheet it was on in the
  imported file (owner, 2026-11-27).
- **New tasks** start with the action line `MMDD已查收`; an open task with an
  empty 进展备注 gets it at import (its received date).
- **Plan date on a to-do card:** the bar under the notes shows the last line's
  date → a 4-digit plan box (date spelled out, like the journal). The box
  writes/replaces the plan date at the end of the last line; an open task whose
  last line has none is flagged. 9999 = kept open with no deadline (长期，没有期限; to-do list only).
- **Kanban:** one column per list side by side: 直接上级, 间接上级 ·
  大老板, and each F tracking sheet in use. In each column: 要处理 (overdue, no
  plan date, no record; for an F sheet: not updated on its review day, read
  from its name, e.g. `周1周4`) on top, then 进行中, then closed but not sent;
  closed and sent items fold away at the bottom (30 at a time). The search box
  also searches the folded history.
- 「下载Excel」 saves as `<file name>-YYYYMMDD.xlsx`, e.g.
  `日常清单-B01组-15.Arthur-20261019.xlsx`: the name is editable on the tab
  (taken from the imported file), the date is always today. Built from a
  template file (the imported one, else the built-in one). What goes where and
  how it looks: section **日常清单 Excel** below. Items that came from the file
  can't be deleted. 状态 OK in the file counts as closed even without the X
  (older items).
  「导入Excel」 reads your current file once and makes it the template, kept in
  this browser's IndexedDB (room for big files; localStorage holds ~5 MB). A
  list never imported uses the built-in file. The built-in template
  (`DEFAULT_XLSX`) is the group's file with the example rows, the 须知 pictures
  and author names removed. No library: the browser unzips/zips the file.
- **Client numbers from the old system:** 「粘贴系统数量」 in the C1有单老客
  section. On the old system's 客户总表 page, click the ERP bookmark 复制本页
  (smol_system `tools/erp_bookmarks/`: copies the page's boxes and tables to
  the clipboard), then press the button here. It finds the client table by
  its column titles and fills, per client 简称 and product line (沙滩鞋,
  室内鞋): last year's orders (去年定单数量), this year's (已接定单数量), 未出 =
  ordered but not shipped (已投产未出数 + 已接未投产数) and 估 (预估未下单数).
  Only clients already in the journal are filled; a product line with no
  order in either year is left out; changed boxes get a blue frame with the
  old value as a tooltip. Nothing about the old system is stored in this page.
- **尺码 tab** (`sizes.html`, loaded in a frame): four boxes, mm, EU, UK and US;
  type a size in any box and the others show the same size. UK and US have a
  small switch for the part of their scale (kids' sizes start again from 1);
  the part picked is used while it has the size, else the box moves to one
  that has it; the same size in the box's other parts is shown under it. A
  menu picks the chart. Default **自动**: the box you type in picks the chart
  of that market's big brand (EU and mm: Birkenstock, adults only, then
  Clarks for kids; UK: Clarks; US: Nike); the first chart that has the exact
  size wins, else the closest; the page says which chart it used. So every
  whole size is found except EU 18 and UK baby 0-3. Also in the menu: **Nike
  凉鞋**, **Clarks** (clarks.com.au), **Birkenstock** (US by its own rule
  US+31/+33 = EU, UK from UK shops as its GB site can't be read), **Crocs**
  (crocs.com.my, whole sizes, EU as ranges, kids in US only; not in 自动). All
  copied on 2026-11-27, links in the page's 怎么换算的？ note. EU/UK/US come only
  from those charts; **mm = EU ÷ 0.15** (owner's rule: shoe/last length, not
  foot length) is the one formula; a number under 60 in the mm box is read
  as cm. A size between two chart sizes names both and picks by the half-
  size rule (kids the bigger, adults the smaller); when a half size is
  shown, a line says what to do without half sizes. Nike gives the same pair
  different EU/UK in its men's and women's tables, so both are kept and the
  US 男/女 switch picks which wins. Client charts later: imported from Excel
  and kept in the browser; never type a client's chart into the file (this
  repo is public).
- **评估单 tab** (sample evaluation, 鞋N评估单-客户-描述.txt): boxes for the
  values, the numbered text 1）…12） written by the page; 产品线 鞋1 夏季凉鞋 /
  鞋2 室内软拖鞋; names under 10） kept as chips. Saved on this PC with the
  journal (`S.evals`, in the backup). 「导入txt」 reads old ones (GBK or
  UTF-8, lines found by number); 「下一轮」 starts the next round with 9） =
  this round's 11） and 12） 初定 copied. 「下载txt」 = UTF-8 with BOM, CRLF.
- **旧ERP书签 tab**: shows `erp.html`, the install page of the old-ERP
  bookmarks 复制本页 / 粘贴表单 / 填今天 (drag onto the bookmarks bar), with
  each one's version date. `erp.html` is made by smol_system's
  `tools/erp_bookmarks/build_install.py ../quick_journal`: never edit it
  here. This repo is public: no ERP address, client data or names in it.
- Not done yet: business-year rollover on 31 Oct (rule 10), other teams' formats.

## 日常清单 Excel

Decided by the owner on 2026-11-27 (a colleague's export had wrong 02新增统计
numbers; checked against a long-used real file, which stays out of this repo).
**On preview since 2026-11-27; the main page still keeps the imported layout
until the release.**

**Which sheet a task goes on** — by its code, at every download:
- no letter (`1120-01`) → **01日常清单-间接上级** (the big boss's own list); a
  file without that sheet → 01直接上级.
- G, A, Z, X (`1124G-01`) → **01日常清单-直接上级**.
- a code the page can't read (old styles like `1117T01`, `1120-A02`, or no date
  like `G20-014`) → its own sheet **旧编码-无法识别**, added at the end of the
  file when needed, same columns as 01直接上级. These tasks are not counted
  anywhere (not 今天收到, not 02新增统计) and are not on the kanban; a small
  grey fold under the kanban lists them. Importing the file again reads that
  sheet back.
- F tracking sheets: untouched, tasks stay where they are.
- On each sheet: **oldest code first** (same day: by its number); 旧编码 sheet
  in the order of the file.

**02新增统计** — recounted from the tasks at every download:
- Each month gets **the same rows as the last month of the imported sheet**,
  in that order (a file used for years may have e.g. A单独 / A大群 / A小群 /
  A汇总 / 直接上级未完成 / B单独 / B汇总 / 间接上级未完成). A file without months
  uses the 8 standard rows (A and B × 单独/大群/小群 + 汇总). The row kind comes
  from its label: count row = tasks whose code is from that day (by letter:
  none → B单独, G/Z → A大群, A → A单独, X → A小群); 汇总 = sum of that letter's
  count rows above it; **未完成** = tasks of that list still open at the end of
  that day (closed = 打X登记日期, else the date of its last note line);
  未完成's 月汇总 stays empty.
- Months: from the **first month of the imported sheet** (else the first
  task's month) to this month. Mon-Fri up to today get a number (0 when
  none), Sat/Sun stay empty (no holidays). The 月份 filter shows this month.

**Never lose a task** (owner, 2026-11-27): the page keeps a running count
(tasks at import, +1 per task added, −1 per task deleted with ×). Every
download reads its own new Excel back before saving it and checks: count =
tasks in the list = tasks in the file, and every task of the list is in the
file (same code, description, notes). If not, a red warning names what is
missing, with 「仍然下载」/「取消」.

**Formatting must stay right** (owner: noticeable mistakes make the tool look
untrustworthy). What a download keeps, checked by `tests/test_export.py`:
- **Each task keeps the look of its own row** in the imported file, also when
  it moves to another sheet: fonts (微软雅黑 / 等线 as it was), fill colours
  (yellow/red highlights), borders, wrap, date format of 打X登记日期, row height,
  extra columns. A task not changed here goes out with its cells exactly as
  they were (coloured words inside a cell too). A changed task gets new values
  in its row's styles and a height fitted to its text. A new task takes the
  look most rows of that sheet have.
- **Excel comments move with their task** (text, author, box size).
- Kept per sheet: header row, column widths, frozen header, the 先前已传 filter
  (rows with 1 hidden), tab colour, zoom.
- 02新增统计: every row has the look (fill colour, borders, font, height) of
  the row with the same label in the file's last month, e.g. yellow 未完成 rows;
  the day cells of a row all get one bordered style.
- Sheets the page doesn't fill (03, 须知, F sheets' pictures) go out byte for
  byte. Excel recalculates formulas on opening.

## Tests

**Run them before every release to live** (every push to `main`, which is
what colleagues use); release only when they all pass:

    python tests/run.py                 # all, about 15 seconds
    python tests/run.py test_todo       # one file
    python tests/run.py --preview       # the pages in preview/: before a preview goes live

While something is on preview, the tests describe the preview: run them with
`--preview`; the main page may fail the new ones until the release.

They need Python with `playwright` (and its Chromium) and `openpyxl`: the
smol_system development setup has both, so on the office PC:
`~/smol_system/.venv/bin/python tests/run.py`.

How they work: a hidden Chrome opens `index.html` / `sizes.html` straight from
the folder (offline, like double-clicking it), with an empty browser memory
and a **pretend date** (so Friday, Monday, a new day can be checked any day).
Each test changes only what it checks and reads the result: the journal
text, the counts, the downloaded Excel, the size boxes. A script error on the
page fails the test. Only made-up data: never a colleague's real file here
(this repo is public).

| File | Checks |
|---|---|
| `tests/test_journal.py` | journal text (hours, +/-, X, plan dates, spaces, C1 count), new day / Friday / new week, import round trip, own lines, backup |
| `tests/test_todo.py` | 日常清单: codes in messages, OK/G, the 组内/老板 count lines, 传递, Excel download from the built-in file |
| `tests/test_export.py` | 日常清单 Excel with an imported file (`tests/todo_file.py`, made up): sheets by code, 旧编码 sheet, order, look + comments kept, 02 layout/colours/counts/未完成, read back, missing-task warning |
| `tests/test_sizes.py` | 尺码: a table of known sizes per chart (change it when a chart changes on purpose), mm = EU ÷ 0.15, half-size rule |
| `tests/test_tabs.py` | every tab opens, erp.html and sizes.html load, 评估单 text reads back |

(The usual way for a JavaScript page is Node + npm with tests in JavaScript;
these are in Python because the smol_system setup already has everything,
and the page stays one file. `tests/browser.py` holds the shared helpers.)
