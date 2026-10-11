#!/usr/bin/env python3
"""Split the single giant INSERT in inactive_useq.sql into batched INSERTs.

Each output INSERT repeats the full column list, so every statement is
standalone and can be run on its own.

    python3 -I split_bulk.py inactive_useq.sql out.sql                # 20 rows/INSERT
    python3 -I split_bulk.py inactive_useq.sql out.sql 10             # 10 rows/INSERT
    python3 -I split_bulk.py inactive_useq.sql out.sql 100 nothing    # skip dup usr_id
    python3 -I split_bulk.py inactive_useq.sql out.sql 100 update     # upsert dup usr_id

conflict modes, for when usr_id already exists in the target table:
    none      (default) plain INSERT -- the whole statement fails on a duplicate
    nothing   ON CONFLICT (usr_id) DO NOTHING -- keep the row already in the table
    update    ON CONFLICT (usr_id) DO UPDATE  -- overwrite it with these values
"""
import re
import sys

src = sys.argv[1]
dst = sys.argv[2]
size = int(sys.argv[3]) if len(sys.argv) > 3 else 20
conflict = sys.argv[4] if len(sys.argv) > 4 else "none"
if conflict not in ("none", "nothing", "update"):
    sys.exit(f"unknown conflict mode {conflict!r} (use none|nothing|update)")

with open(src, encoding="utf-8") as fh:
    lines = fh.read().splitlines()

# line 0: comment, line 1: INSERT INTO ... (cols), line 2: VALUES, rest: rows
comment, insert_head, values_kw = lines[0], lines[1], lines[2]
if values_kw.strip().upper() != "VALUES":
    sys.exit(f"unexpected line 3 (expected VALUES): {values_kw[:60]!r}")

cols = [c.strip() for c in re.search(r"\((.*)\)", insert_head).group(1).split(",")]

if conflict == "nothing":
    tail = "ON CONFLICT (usr_id) DO NOTHING;"
elif conflict == "update":
    sets = ",\n    ".join(f"{c} = EXCLUDED.{c}" for c in cols if c != "usr_id")
    tail = f"ON CONFLICT (usr_id) DO UPDATE SET\n    {sets};"
else:
    tail = None

rows = []
for line in lines[3:]:
    line = line.strip()
    if line:
        rows.append(line.rstrip(",").rstrip(";").rstrip())

with open(dst, "w", encoding="utf-8") as fh:
    fh.write(comment + "\n")
    for i in range(0, len(rows), size):
        chunk = rows[i:i + size]
        fh.write(f"-- batch {i // size + 1} (rows {i + 1}-{i + len(chunk)})\n")
        fh.write(insert_head + "\nVALUES\n")
        for j, row in enumerate(chunk):
            if j == len(chunk) - 1 and tail:
                fh.write(f"{row}\n{tail}\n")
            else:
                fh.write(row + (";" if j == len(chunk) - 1 else ",") + "\n")

print(f"{len(rows)} rows -> {(len(rows) + size - 1) // size} INSERTs of up to {size}")
