import pandas as pd, os, requests, chardet

RAW  = os.path.join(os.path.dirname(__file__), '..', 'data', 'sales_data.txt')
OUT  = os.path.join(os.path.dirname(__file__), '..', 'output', 'clean_sales.csv')
API  = "https://fakestoreapi.com/products"

def clean_sales_data(in_path=RAW, out_path=OUT):
    # 1. encoding
    with open(in_path, 'rb') as f:
        enc = chardet.detect(f.read(50_000))['encoding'] or 'utf-8'
    # 2. read
    df = pd.read_csv(in_path, sep='|', encoding=enc, dtype=str, on_bad_lines='skip')
    # 3. clean
    df.columns = [c.strip() for c in df.columns]
    df = df.dropna(how='all').apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
    df['Quantity']  = pd.to_numeric(df['Quantity'].str.replace(',', ''), errors='coerce')
    df['UnitPrice'] = pd.to_numeric(df['UnitPrice'].str.replace(',', ''), errors='coerce')
    # 4. filters
    pre = len(df)
    df = df[(df['TransactionID'].str.startswith('T', na=False)) &
            (df['CustomerID'].notna()) & (df['Region'].notna()) &
            (df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    post = len(df)
    print(f'Total records parsed: {pre}')
    print(f'Invalid records removed: {pre - post}')
    print(f'Valid records after cleaning: {post}')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    return df

def enrich_products(df):
    api = pd.json_normalize(requests.get(API, timeout=10).json())[["title", "price", "category"]]
    api.columns = ["api_name", "api_price", "api_category"]
    df["api_key"] = df["ProductName"].str.lower()
    api["api_key"] = api["api_name"].str.lower()
    return df.merge(api, on="api_key", how="left")

if __name__ == "__main__":
    df_clean = clean_sales_data()
    print(enrich_products(df_clean).head())