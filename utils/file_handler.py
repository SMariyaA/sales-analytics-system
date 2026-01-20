import os, csv, chardet

ENCODINGS = ['utf-8', 'latin-1', 'cp1252']

def read_sales_data(filename: str) -> list[str]:
    """Task 1.1 – read raw lines with encoding fall-back"""
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"[ERROR] File not found: {filename}")
    for enc in ENCODINGS:
        try:
            with open(filename, encoding=enc) as f:
                lines = [ln.rstrip() for ln in f if ln.strip()]
            return lines[1:]          # skip header
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("Unable to decode file with any tried encoding.")

def parse_transactions(raw_lines: list[str]) -> list[dict]:
    """Task 1.2 – parse & clean"""
    out = []
    for raw in raw_lines:
        parts = raw.split('|')
        if len(parts) != 8:
            continue
        tid, date, pid, pname, qty, up, cid, region = parts
        pname = pname.replace(',', '')          # remove commas in name
        try:
            qty = int(qty.replace(',', ''))
            up  = float(up.replace(',', ''))
        except ValueError:
            continue
        out.append({
            'TransactionID': tid.strip(),
            'Date': date.strip(),
            'ProductID': pid.strip(),
            'ProductName': pname.strip(),
            'Quantity': qty,
            'UnitPrice': up,
            'CustomerID': cid.strip(),
            'Region': region.strip()
        })
    return out

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """Task 1.3 – validate + optional filters"""
    invalid = 0
    base = []
    for t in transactions:
        if (t['Quantity'] <= 0 or t['UnitPrice'] <= 0 or
            not all(t.get(k) for k in t) or
            not t['TransactionID'].startswith('T') or
            not t['ProductID'].startswith('P') or
            not t['CustomerID'].startswith('C')):
            invalid += 1
            continue
        base.append(t)

    summary = {'total_input': len(transactions), 'invalid': invalid}

    # ---- region filter ----
    avail_regs = sorted({t['Region'] for t in base})
    if region:
        base = [t for t in base if t['Region'] == region]
    summary['filtered_by_region'] = summary['total_input'] - invalid - len(base)

    # ---- amount filter ----
    amounts = [t['Quantity'] * t['UnitPrice'] for t in base]
    if min_amount is not None:
        base = [t for t, a in zip(base, amounts) if a >= min_amount]
    if max_amount is not None:
        base = [t for t, a in zip(base, amounts) if a <= max_amount]
    summary['filtered_by_amount'] = len(amounts) - len(base)
    summary['final_count'] = len(base)

    # ---- user info ----
    print("Available regions:", ', '.join(avail_regs))
    if amounts:
        print(f"Amount range: {min(amounts):.2f} – {max(amounts):.2f}")
    return base, invalid, summary

# quick self-test
if __name__ == "__main__":
    raw  = read_sales_data("data/sales_data.txt")
    trans = parse_transactions(raw)
    valid, inv, summ = validate_and_filter(trans)
    print("Invalid count:", inv)
    print("Summary:", summ)