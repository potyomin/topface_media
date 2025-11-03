# src/run_inspection.py
from pathlib import Path
from src.files_to_check import FILES, ID_COL, ENCODINGS, HEAD_ROWS
from src.utils.inspector import read_table, summarize_df

ROOT = Path(__file__).resolve().parents[1]

def kb(size_bytes):
    return f"{size_bytes/1024:.1f} KB"

def abspath(p):
    p = Path(p)
    return p if p.is_absolute() else (ROOT / p)

def main():
    for path in FILES:
        p = abspath(path)
        exists = p.exists()
        size = kb(p.stat().st_size) if exists else "—"
        print(f"\n=== {p.name} ===")
        print(f"path: {p.resolve()}")
        print(f"exists: {exists}  size: {size}")

        df, enc, err = read_table(p, encodings=ENCODINGS, id_col=ID_COL)
        if err:
            print(f"error: {err.get('error')}")
            continue

        print(f"encoding: {enc}")
        info = summarize_df(df, head_rows=HEAD_ROWS)
        print(f"shape: {info['shape']}  columns: {info['columns_count']}")
        print("columns sample:", info["columns_sample"])
        print("\nhead:")
        print(info["head"])

if __name__ == "__main__":
    main()
