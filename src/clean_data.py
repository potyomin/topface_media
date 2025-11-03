# src/clean_data.py
from pathlib import Path
import pandas as pd
import re

R = Path(__file__).resolve().parents[1]
D, O = R / "data", R / "out"
O.mkdir(exist_ok=True)

def read_csv(p):
    for e in ("utf-8-sig", "utf-8", "cp1251"):
        try: return pd.read_csv(p, encoding=e, dtype={"id":"string"}, low_memory=False)
        except UnicodeDecodeError: pass
    return pd.read_csv(p, dtype={"id":"string"}, low_memory=False)

fin  = read_csv(D / "financial_data.csv")
prol = read_csv(D / "prolongations.csv")

# базовая чистка текста
for df, cols in ((fin, ("id","Account")), (prol, ("id","AM","month"))):
    for c in cols:
        if c in df:
            s = df[c].astype("string").str.replace("\u00A0"," ", regex=False)
            df[c] = s.str.strip().str.replace(r"\s+"," ", regex=True)

# month_canon: "ноябрь 2022" -> "2022-11"
m2n = {"янв":1,"фев":2,"мар":3,"апр":4,"май":5,"июн":6,"июл":7,"авг":8,"сен":9,"окт":10,"ноя":11,"дек":12}
def canon_month(x):
    if pd.isna(x): return None
    m = re.search(r"([а-яё]+)\s+(\d{2,4})", str(x).lower())
    if not m: return None
    mon, y = m.groups(); mm = m2n.get(mon[:3])
    if not mm: return None
    y = int(y);  y = 2000 + y if y < 100 else y
    return f"{y:04d}-{mm:02d}"
if "month" in prol: prol["month_canon"] = prol["month"].map(canon_month)

# все месячные колонки в fin -> числа
months = [c for c in fin.columns if any(y in str(c) for y in ("2022","2023","2024"))]
def to_num(col):
    s = col.astype("string").str.replace("\u00A0","", regex=False).str.replace(" ","", regex=False)
    s = s.str.replace(",",".", regex=False).str.replace("стоп","", case=False, regex=False)
    return pd.to_numeric(s, errors="coerce")
for c in months: fin[c] = to_num(fin[c])

# сохранить
fin.to_csv(O / "financial_clean.csv", index=False, encoding="utf-8", lineterminator="\n")
prol.to_csv(O / "prolongations_clean.csv", index=False, encoding="utf-8", lineterminator="\n")
print("[OK] saved:\n", O/"financial_clean.csv\n", "and\n", O/"prolongations_clean.csv")
