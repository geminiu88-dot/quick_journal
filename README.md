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
- **Hours** are written the group leader's way: `4h15` = 4 h 15 min (no unit
  on the minutes), `+`/`-` at the end. Typing `1.5`, `1:30`, `90m` or `1h30` all
  work; the box is tidied to `1h30` when you leave it (`parseHours` /
  `fmtHours`). 「格式范本」 shows the group's example journal and rules.
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
- 「下载Excel」 writes `日常清单-组-姓名-2YYMMDD-n.xlsx` (n = sends today) from a
  template file: only the two 01 sheets and 02新增统计 are rewritten (02: 8 rows
  per month, days Mon-Sat filled, sums as formulas); every other sheet stays as
  it is in the template. 「导入Excel」 reads your current file once and makes it
  the template (kept in this browser only). The built-in template
  (`DEFAULT_XLSX`) is the group's file with the example rows, the 须知 pictures
  and author names removed. No library: the browser unzips/zips the file.
- Not done yet: business-year rollover on 31 Oct (rule 10), other teams' formats.
