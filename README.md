# 日志 (quick_journal)

PC page for the BC team's daily journal (日志格式-BC组员). The page *is* the
journal, in the exact text format: yellow boxes are typed, blue parts are
worked out, red means "check this". 「复制日志」 copies the text exactly as shown.

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
- The fixed lines (labels, boxes, counts) are the `DAILY` / `WEEKLY` lists at
  the top of the script; the importer reads lines with the same lists.
- **日常清单 tab** (the coded to-do list from the bosses). Paste messages: a
  code like `1019G-02` is found anywhere in a line (MMDD + letter + `-` + the
  day's number); each line with a code starts a new item. The letter says who
  sent it: `SOURCES` at the top of the to-do script (group B01's letters,
  other groups may differ). Status follows 须知 5: `OK` when the last note line
  ends in X (打X登记日期 = that day), `G` when a note line starts with today's
  date. 先前已传 = 1 once an OK item has been sent before (须知 6). The journal's
  `*组内日常清单表` line is filled from this list.
  The big boss is everyone's direct boss too: `G` (to the whole group) goes on
  01直接上级, no letter (to one person) on his own sheet, 01间接上级.
- **Kanban (preview):** one column per list side by side: 直接上级, 间接上级 ·
  大老板, and each F tracking sheet in use. In each column: 要处理 (overdue, no
  plan date, no record; for an F sheet: not updated on its review day, read
  from its name, e.g. `周1周4`) on top, then 进行中, then closed but not sent;
  closed and sent items fold away at the bottom (30 at a time). The search box
  also searches the folded history.
- 「下载Excel」 saves as `<file name>-YYYYMMDD.xlsx`, e.g.
  `日常清单-B01组-15.Arthur-20261019.xlsx`: the name is editable on the tab
  (taken from the imported file), the date is always today. Built from a
  template file. **An imported file is changed in place:** its rows never move
  (so Excel comments, pictures and hidden rows stay right), only rows edited
  here are rewritten, new items go at the bottom, and items that came from the
  file can't be deleted. 状态 OK in the file counts as closed even without the X
  (older items). 02新增统计 keeps each person's own rows (deleted rows stay
  deleted); only counts of items added here are written, `未完成` rows are
  filled from the open items of each day the page was opened, and a new month
  copies the rows of the month before. Untouched sheets go out byte for byte.
  「导入Excel」 reads your current file once and makes it the template, kept in
  this browser's IndexedDB (room for big files; localStorage holds ~5 MB). A
  list never imported uses the built-in file the old way (rows rebuilt, 02: 8
  rows per month). The built-in template
  (`DEFAULT_XLSX`) is the group's file with the example rows, the 须知 pictures
  and author names removed. No library: the browser unzips/zips the file.
- Not done yet: business-year rollover on 31 Oct (rule 10), other teams' formats.
