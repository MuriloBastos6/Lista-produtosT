import pandas as pd
from pathlib import Path
import html

xlsx = Path('produtos_Peso_C.xlsx')
index_html = Path('Pagina/index.html')

if not xlsx.exists():
    print('ERROR: produtos_Peso_C.xlsx not found')
    raise SystemExit(1)
if not index_html.exists():
    print('ERROR: index.html not found')
    raise SystemExit(1)

# read sheet
df = pd.read_excel(xlsx, sheet_name=0)
# normalize column names
cols = {c: c.strip() for c in df.columns}
df.rename(columns=cols, inplace=True)

# The user specified the first category is the first block (lines 1..94).
# Use the first 94 rows of the sheet for the Amendoins category (if sheet is that long).
max_rows = 94
rows = df.iloc[0:max_rows]

if rows.empty:
    print(
        f'No rows found in the first {max_rows} rows. Showing first 10 rows instead.')
    rows = df.head(10)

cards_html = []
for _, r in rows.iterrows():
    descricao = html.escape(str(r.get('Descrição', '')).strip())
    cod = html.escape(str(r.get('Cod.', '')).strip())
    debit = r.get('Débito/Crédito', '')
    avista = r.get('Á vista', '')
    peso = r.get('Peso', '')
    un = html.escape(str(r.get('Un', '')).strip())

    # format prices
    def fmt(v):
        try:
            return f"R$ {float(v):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except:
            return str(v)

    debit_s = fmt(debit)
    avista_s = fmt(avista)

    img_src = 'https://images.unsplash.com/photo-1544025162-d76694265947?w=800&q=60&auto=format&fit=crop'

    card = f'''                <div class="card">
                    <img class="card-img" src="{img_src}" alt="{descricao}">
                    <div class="card-body">
                        <p class="ref">REF.: {cod}</p>
                        <h4 class="card-title">{descricao}</h4>
                        <div class="prices">
                            <div class="price"><span class="price-value">{debit_s}</span><small>Débito / Crédito</small></div>
                            <div class="price"><span class="price-value">{avista_s}</span><small>À vista</small></div>
                        </div>
                        <div class="payment">Un: {un} • Peso: {peso}</div>
                    </div>
                </div>'''
    cards_html.append(card)

new_cards = '\n'.join(cards_html)

# read index.html
text = index_html.read_text(encoding='utf-8')
start_section = text.find('<section id="amendoins"')
if start_section == -1:
    print('ERROR: amendoins section not found in index.html')
    raise SystemExit(1)

grid_start = text.find('<div class="cards-grid">', start_section)
if grid_start == -1:
    print('ERROR: cards-grid not found in amendoins section')
    raise SystemExit(1)

pager_idx = text.find('<div class="pager-actions">', grid_start)
if pager_idx == -1:
    print('ERROR: pager-actions not found after cards-grid')
    raise SystemExit(1)

# build replacement
replacement = '<div class="cards-grid">\n' + \
    new_cards + '\n            </div>\n\n            '

new_text = text[:grid_start] + replacement + text[pager_idx:]
index_html.write_text(new_text, encoding='utf-8')
print(f'Updated index.html with {len(cards_html)} cards for Amendoins')
