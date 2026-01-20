import pandas as pd
from collections import defaultdict, Counter
from datetime import datetime

# ---------- Task 2.1 ----------
def calculate_total_revenue(transactions):
    return sum(t['Quantity'] * t['UnitPrice'] for t in transactions)

def region_wise_sales(transactions):
    rev = defaultdict(float)
    cnt = defaultdict(int)
    for t in transactions:
        rev[t['Region']] += t['Quantity'] * t['UnitPrice']
        cnt[t['Region']] += 1
    total = sum(rev.values())
    out = {}
    for r in sorted(rev, key=rev.get, reverse=True):
        out[r] = {
            'total_sales': round(rev[r], 2),
            'transaction_count': cnt[r],
            'percentage': round((rev[r] / total) * 100, 2)
        }
    return out

def top_selling_products(transactions, n=5):
    qty = defaultdict(int)
    rev = defaultdict(float)
    for t in transactions:
        qty[t['ProductName']] += t['Quantity']
        rev[t['ProductName']] += t['Quantity'] * t['UnitPrice']
    items = [(p, qty[p], round(rev[p], 2)) for p in qty]
    items.sort(key=lambda x: x[1], reverse=True)
    return items[:n]

def customer_analysis(transactions):
    spent = defaultdict(float)
    count = defaultdict(int)
    prods = defaultdict(set)
    for t in transactions:
        cid = t['CustomerID']
        spent[cid] += t['Quantity'] * t['UnitPrice']
        count[cid] += 1
        prods[cid].add(t['ProductName'])
    out = {}
    for cid in sorted(spent, key=spent.get, reverse=True):
        out[cid] = {
            'total_spent': round(spent[cid], 2),
            'purchase_count': count[cid],
            'avg_order_value': round(spent[cid] / count[cid], 2),
            'products_bought': list(prods[cid])
        }
    return out

# ---------- Task 2.2 ----------
def daily_sales_trend(transactions):
    trend = defaultdict(lambda: {'revenue': 0.0, 'transaction_count': 0, 'unique_customers': set()})
    for t in transactions:
        d = t['Date']
        amt = t['Quantity'] * t['UnitPrice']
        trend[d]['revenue'] += amt
        trend[d]['transaction_count'] += 1
        trend[d]['unique_customers'].add(t['CustomerID'])
    # convert set -> count & round
    for v in trend.values():
        v['unique_customers'] = len(v['unique_customers'])
        v['revenue'] = round(v['revenue'], 2)
    return dict(sorted(trend.items()))

def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)

    if __name__ == "__main__":
    from utils.file_handler import read_sales_data, parse_transactions
    raw  = read_sales_data("data/sales_data.txt")
    trans = parse_transactions(raw)
    print("Total revenue:", calculate_total_revenue(trans))
    print("Region stats:", region_wise_sales(trans))
    print("Top 3 products:", top_selling_products(trans, 3))
    print("Peak day:", find_peak_sales_day(trans))