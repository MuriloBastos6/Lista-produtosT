import pandas as pd
from pathlib import Path

xlsx = Path('produtos_Peso_C.xlsx')
if not xlsx.exists():
    print('ERROR: produtos_Peso_C.xlsx not found in workspace root (d:/ListProducts)')
    raise SystemExit(1)

# read first sheet
df = pd.read_excel(xlsx, sheet_name=0)
print('=== Columns ===')
print(list(df.columns))
print('\n=== Head (first 20 rows) ===')
print(df.head(20).to_string(index=False))

# show unique values per column (small sample)
print('\n=== Unique values sample per column ===')
for c in df.columns:
    try:
        uniques = df[c].dropna().unique()[:10]
        print(f"{c}: {list(uniques)}")
    except Exception as e:
        print(f"{c}: (error reading uniques) {e}")

print('\n=== Done ===')
