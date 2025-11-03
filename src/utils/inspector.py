# src/utils/inspector.py
from pathlib import Path
import pandas as pd

DEFAULT_ENCODINGS = ["utf-8-sig", "utf-8", "cp1251"]

# функция чтения файлов для первичного анализа
def read_table(path, encodings=None, id_col=None):
    p = Path(path)
    if not p.exists():
        return None, None, {"error": "not_found", "path": str(p)}

    suf = p.suffix.lower()
    encodings = encodings or DEFAULT_ENCODINGS

    if suf in (".xlsx", ".xls"):
        df = pd.read_excel(p)
        if id_col and id_col in df.columns:
            df[id_col] = df[id_col].astype("string")
        return df, "n/a (excel)", {}

    # CSV (или .txt)
    for enc in encodings:
        try:
            df = pd.read_csv(
                p,
                encoding=enc,
                dtype={id_col: "string"} if id_col else None,
                low_memory=False
            )
            return df, enc, {}
        except UnicodeDecodeError:
            continue
    # fallback без encoding
    df = pd.read_csv(
        p,
        dtype={id_col: "string"} if id_col else None,
        low_memory=False
    )
    return df, "default/unknown", {}

# функция возврата основных сведений о файлах с данными
def summarize_df(df, head_rows=5):
    return {
        "shape": tuple(df.shape),
        "head": df.head(head_rows).to_string(index=False),
        "columns_count": df.shape[1],
        "columns_sample": list(df.columns[:min(10, df.shape[1])])
    }
