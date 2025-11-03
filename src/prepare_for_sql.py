# src/prepare_for_sql.py
from pathlib import Path
import pandas as pd
import re

R = Path(__file__).resolve().parents[1]
fin = pd.read_csv(R/'out'/'financial_clean.csv', dtype={'id':'string'}, low_memory=False)
prol = pd.read_csv(R/'out'/'prolongations_clean.csv', dtype={'id':'string'}, low_memory=False)

# --- (1) очистим заголовки от BOM и пробелов
def _fix_cols(df: pd.DataFrame) -> pd.DataFrame:
    df.rename(columns=lambda c: c.replace("\ufeff", "").strip(), inplace=True)
    return df

fin = _fix_cols(fin)
prol = _fix_cols(prol)

# --- (2) опционально нормализуем «кривые» символы в текстовых полях
for df, cols in ((fin, ["Account"]), (prol, ["AM"])):
    for c in cols:
        if c in df.columns:
            s = df[c].astype("string")
            s = s.str.replace("\u2019", "'", regex=False)  # ’ -> '
            s = s.str.replace("\u2013", "-", regex=False)  # – -> -
            s = s.str.replace("\u2014", "-", regex=False)  # — -> -
            df[c] = s

# 1) wide→long для финансов: получаем id, month, shipment
months = [c for c in fin.columns if any(y in str(c) for y in ('2022','2023','2024'))]
long = fin.melt(
    id_vars=[c for c in fin.columns if c not in months],
    value_vars=months,
    var_name='month_raw', value_name='shipment'
)

# "Ноябрь 2023" → "2023-11"
m2n = {'янв':1,'фев':2,'мар':3,'апр':4,'май':5,'июн':6,'июл':7,'авг':8,'сен':9,'окт':10,'ноя':11,'дек':12}
def canon(label):
    m = re.search(r'([А-Яа-яЁё]+)\s+(\d{4})', str(label))
    if not m: return None
    mon, y = m.groups()
    mm = m2n.get(mon.lower()[:3])
    return f'{y}-{mm:02d}' if mm else None

long['month']    = long['month_raw'].map(canon)
long['shipment'] = pd.to_numeric(long['shipment'], errors='coerce')
long = long.dropna(subset=['month','shipment'])

# на случай дублей типа "первая/вторая часть оплаты"
ship = long.groupby(['id','month'], as_index=False)['shipment'].sum()

# 2) размерность проектов: id, month_last, AM (+Account при наличии)
dim = prol[['id','month_canon','AM']].rename(columns={'month_canon':'month_last'})
if 'Account' in fin.columns:
    dim = dim.merge(fin[['id','Account']].dropna().drop_duplicates('id'), on='id', how='left')

# 3) сохранить CSV для импорта в SQL — ЧИСТЫЙ UTF-8, без BOM
out = R/'out'
ship.to_csv(out/'shipments.csv',   index=False, encoding='utf-8', lineterminator="\n")
dim.to_csv(out/'projects_dim.csv', index=False, encoding='utf-8', lineterminator="\n")
print('[OK] saved:\n', out/'shipments.csv\n', 'and\n', out/'projects_dim.csv')

