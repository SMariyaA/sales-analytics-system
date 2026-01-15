"""BMA – Sales Data Analytics System – data cleaning & validation"""
import re, pandas as pd, sys, os

RAW_FILE = "sales_data.txt"

def parse_line(line: str):
    line = line.strip()
    if not line: return None
    parts = re.split(r'\|(?![^"]*"(?:(?:[^"]*"){2})*[^"]*$)', line)
    return [p.strip() for p in parts] if len(parts) == 8 else None

def clean_sales_data(path: str):
    total = removed = 0; kept = []
    with open(path, encoding="utf-8") as f:
        _ = f.readline()
        for raw in f:
            total += 1
            p = parse_line(raw)
            if p is None: removed += 1; continue
            tid, date, pid, pname, qty, up, cid, region = p
            if not cid or not region: removed += 1; continue
            try:
                qty_int  = int(qty)
                up_float = float(up.replace(",", ""))
            except ValueError: removed += 1; continue
            if qty_int <= 0 or up_float <= 0 or not tid.startswith("T"): removed += 1; continue
            kept.append([tid, date, pid, pname, qty_int, up_float, cid, region])
    df = pd.DataFrame(kept, columns=["TransactionID","Date","ProductID","ProductName","Quantity","UnitPrice","CustomerID","Region"])
    print(f"Total records parsed: {total}"); print(f"Invalid records removed: {removed}"); print(f"Valid records after cleaning: {len(df)}")
    return df

if __name__ == "__main__":
    clean_df = clean_sales_data(RAW_FILE)
    print("\nClean sample:"); print(clean_df.head())
