import requests, os, csv

API_ROOT = "https://dummyjson.com/products"

def fetch_all_products(limit=100):
    """3.1a fetch all products with error handling"""
    try:
        resp = requests.get(f"{API_ROOT}?limit={limit}", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        print("[OK] Fetched products from DummyJSON")
        return data['products']
    except Exception as e:
        print("[FAIL] Could not fetch products:", e)
        return []

def create_product_mapping(api_products):
    """3.1b map id -> subset fields"""
    return {p['id']: {
        'title': p['title'],
        'category': p['category'],
        'brand': p.get('brand', 'Unknown'),
        'rating': p.get('rating', 0)
    } for p in api_products}

def enrich_sales_data(transactions, product_mapping):
    """3.2 enrich + save"""
    enriched = []
    for t in transactions:
        pid_num = int(t['ProductID'][1:])  # P123 -> 123
        match = product_mapping.get(pid_num)
        t['API_category'] = match['category'] if match else None
        t['API_Brand']     = match['brand'] if match else None
        t['API_Rating']    = match['rating'] if match else None
        t['API_Match']     = bool(match)
        enriched.append(t)
    save_enriched_data(enriched)
    return enriched

def save_enriched_data(enriched, filename='data/enriched_sales_data.txt'):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    fieldnames = list(enriched[0].keys()) if enriched else []
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='|')
        writer.writeheader()
        writer.writerows(enriched)
    print(f"[OK] Saved enriched data → {filename}")

# ---- quick test ----
if __name__ == "__main__":
    from utils.file_handler import read_sales_data, parse_transactions
    raw  = read_sales_data("data/sales_data.txt")
    trans = parse_transactions(raw)
    products = fetch_all_products()
    mapping = create_product_mapping(products)
    enrich_sales_data(trans, mapping)