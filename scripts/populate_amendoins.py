"""Populate index.html from produtos.xlsx using semantic, grouped markup."""

from __future__ import annotations

import unicodedata
import re
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import pandas as pd
from bs4 import BeautifulSoup, Tag


ROOT = Path(__file__).resolve().parent.parent
XLSX_PATH = ROOT / 'scripts' / 'produtos.xlsx'
INDEX_PATH = ROOT / 'index.html'
IMAGE_SEARCH_DIRS = [
    ROOT / 'Pagina' / 'produtos',
    ROOT / 'Pagina',
]
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.avif')
DEFAULT_IMAGE = 'https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=1200&q=80&auto=format&fit=crop'


def normalize_key(value: str | float | int | None) -> str:
    """Normalize text for comparisons (case, accents, spacing)."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ''
    text = str(value).replace('\xa0', ' ').strip()
    text = ' '.join(text.split())
    text = unicodedata.normalize('NFKD', text).encode(
        'ascii', 'ignore').decode('ascii')
    normalized = text.lower()
    # pandas float('nan') -> 'nan'; ignore this sentinel
    return '' if normalized == 'nan' else normalized


def clean_text(value: str | float | int | None) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ''
    text = str(value).replace('\xa0', ' ').strip()
    return ' '.join(text.split())


def clean_code(value: str | float | int | None) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ''
    if isinstance(value, (int, float)):
        if isinstance(value, float) and not value.is_integer():
            return clean_text(value)
        return str(int(value))
    return clean_text(value)


def format_price(value: str | float | int | None) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ''
    try:
        price = float(value)
    except (TypeError, ValueError):
        text = clean_text(value)
        if not text:
            return ''
        return text if text.startswith('R$') else f'R$ {text}'
    formatted = f'R$ {price:,.2f}'.replace(
        ',', 'X').replace('.', ',').replace('X', '.')
    return formatted


@dataclass
class Variant:
    raw_price: object
    weight: str
    unit: str
    code: str

    def formatted_price(self) -> str:
        return format_price(self.raw_price)

    def meta_tokens(self) -> Iterable[str]:
        for token in (self.weight, self.unit):
            if token:
                yield token


@dataclass
class ProductGroup:
    display: str
    variants: list[Variant] = field(default_factory=list)
    image_ref: str = ''

    @property
    def codes(self) -> list[str]:
        ordered: OrderedDict[str, None] = OrderedDict()
        for variant in self.variants:
            if variant.code:
                ordered.setdefault(variant.code, None)
        return list(ordered.keys())


@dataclass
class CategoryData:
    meta: dict
    groups: OrderedDict[str, ProductGroup] = field(default_factory=OrderedDict)


CATEGORY_META = OrderedDict({
    'amendoins/castanhas/amendoas/nozes': {
        'id': 'amendoins',
        'title': 'Amendoins, Castanhas, Amêndoas e Nozes',
        'subtitle': 'Amendoins e itens relacionados',
    },
    'arroz': {
        'id': 'arroz',
        'title': 'Arroz',
        'subtitle': 'Tipos de arroz e embalagens',
    },
    'sucrilhos': {
        'id': 'sucrilhos',
        'title': 'Sucrilhos',
        'subtitle': 'Cereais matinais e produtos afins',
    },
    'chas': {
        'id': 'chas',
        'title': 'Chás',
        'subtitle': 'Ervas, infusões e blends',
    },
    'farinhas': {
        'id': 'farinhas',
        'title': 'Farinhas',
        'subtitle': 'Farinhas diversas e misturas',
    },
    'graos': {
        'id': 'graos',
        'title': 'Grãos',
        'subtitle': 'Feijão, milho, ervilhas e afins',
    },
    'panificacoes': {
        'id': 'panificacoes',
        'title': 'Panificações',
        'subtitle': 'Produtos para panificação e confeitaria',
    },
    'especiarias': {
        'id': 'especiarias',
        'title': 'Especiarias',
        'subtitle': 'Temperos, condimentos e especiarias',
    },
    'especiarias/temperos': {
        'id': 'especiarias',
        'title': 'Especiarias e Temperos',
        'subtitle': 'Temperos, condimentos e especiarias',
    },
    'frutas': {
        'id': 'frutas',
        'title': 'Frutas',
        'subtitle': 'Frutas secas e desidratadas',
    },
    'sementes': {
        'id': 'sementes',
        'title': 'Sementes',
        'subtitle': 'Sementes para consumo e culinária',
    },
    'produtos naturais': {
        'id': 'produtos-naturais',
        'title': 'Produtos Naturais',
        'subtitle': 'Chás, grãos e itens naturais',
    },
    'refrigerante/suco': {
        'id': 'refrigerantes-e-sucos',
        'title': 'Refrigerantes e Sucos',
        'subtitle': 'Bebidas engarrafadas e enlatadas',
    },
    'oleo vegetal': {
        'id': 'oleo-vegetal',
        'title': 'Óleos Vegetais',
        'subtitle': 'Óleos alimentares e especiais',
    },
    'goma pronta': {
        'id': 'gomas-prontas',
        'title': 'Gomas Prontas',
        'subtitle': 'Gomas, balas e confeitos',
    },
    'salgadinhos/snacks': {
        'id': 'salgadinhos-snacks',
        'title': 'Salgadinhos e Snacks',
        'subtitle': 'Snacks salgados e crocantes',
    },
    'doces': {
        'id': 'doces',
        'title': 'Doces',
        'subtitle': 'Confeitos, caramelos e guloseimas',
    },
    'potes': {
        'id': 'potes',
        'title': 'Potes',
        'subtitle': 'Produtos fracionados em potes',
    },
    'diversos': {
        'id': 'diversos',
        'title': 'Diversos',
        'subtitle': 'Outros produtos e novidades',
    },
})


def load_products() -> OrderedDict[str, CategoryData]:
    if not XLSX_PATH.exists():
        raise SystemExit('ERROR: scripts/produtos.xlsx não encontrado')

    df = pd.read_excel(XLSX_PATH, header=None)

    catalog: OrderedDict[str, CategoryData] = OrderedDict()
    current_category_id: str | None = None

    for row in df.itertuples(index=False):
        header_text = clean_text(row[0])
        normalized_header = normalize_key(header_text)

        try:
            trailing_empty = all(pd.isna(value) for value in row[1:])
        except TypeError:
            trailing_empty = False

        if header_text and trailing_empty:
            if normalized_header == 'descricao':
                continue
            meta = CATEGORY_META.get(normalized_header)
            if meta:
                current_category_id = meta['id']
                catalog.setdefault(current_category_id,
                                   CategoryData(meta=meta))
            else:
                current_category_id = None
            continue

        if not current_category_id:
            continue

        if not header_text or normalized_header == 'descricao':
            continue

        price = row[4] if len(row) > 4 else None
        if price is None or (isinstance(price, float) and pd.isna(price)):
            continue

        weight = clean_text(row[1] if len(row) > 1 else '')
        code = clean_code(row[2] if len(row) > 2 else '')
        unit = clean_text(row[3] if len(row) > 3 else '')
        image_ref = clean_text(row[5] if len(row) > 5 else '')

        group_key = normalize_key(header_text)
        if not group_key:
            continue

        category = catalog[current_category_id]
        group = category.groups.get(group_key)
        if not group:
            group = ProductGroup(display=header_text)
            category.groups[group_key] = group

        if image_ref and not group.image_ref:
            group.image_ref = image_ref.replace('\\', '/')

        group.variants.append(
            Variant(raw_price=price, weight=weight, unit=unit, code=code))

    return catalog


def slugify(value: str) -> str:
    base = normalize_key(value)
    slug = re.sub(r'[^a-z0-9]+', '-', base).strip('-')
    return slug or 'produto'


def resolve_image_src(group: ProductGroup) -> str:
    if group.image_ref:
        ref = group.image_ref.strip()
        if ref.lower().startswith(('http://', 'https://', 'data:')):
            return ref
        path = Path(ref)
        if not path.is_absolute():
            path = ROOT / ref
        if path.exists():
            try:
                return path.relative_to(ROOT).as_posix()
            except ValueError:
                return path.as_posix()
        return ref.replace('\\', '/')

    slug = slugify(group.display)
    for directory in IMAGE_SEARCH_DIRS:
        for extension in IMAGE_EXTENSIONS:
            candidate = directory / f'{slug}{extension}'
            if candidate.exists():
                try:
                    return candidate.relative_to(ROOT).as_posix()
                except ValueError:
                    return candidate.as_posix()

    return DEFAULT_IMAGE


def build_card_node(soup: BeautifulSoup, group: ProductGroup) -> Tag:
    card = soup.new_tag('article', attrs={'class': 'card'})

    image_src = resolve_image_src(group)
    media = soup.new_tag('figure', attrs={'class': 'card-media'})
    img = soup.new_tag(
        'img', attrs={'class': 'card-img', 'src': image_src, 'alt': group.display})
    media.append(img)
    card.append(media)

    body = soup.new_tag('div', attrs={'class': 'card-body'})

    title = soup.new_tag('h4', attrs={'class': 'card-title'})
    title.string = group.display
    body.append(title)

    codes = group.codes
    if codes:
        ref = soup.new_tag('p', attrs={'class': 'ref'})
        ref.string = f"Cód.: {', '.join(codes)}"
        body.append(ref)

    variant_list = soup.new_tag('ul', attrs={'class': 'variant-list'})

    for variant in group.variants:
        item = soup.new_tag('li', attrs={'class': 'variant-line'})

        price_span = soup.new_tag('span', attrs={'class': 'variant-price'})
        price_span.string = variant.formatted_price()
        item.append(price_span)

        meta_tokens = list(variant.meta_tokens())
        meta_span = soup.new_tag('span', attrs={'class': 'variant-meta'})
        meta_span.string = ' · '.join(meta_tokens)
        item.append(meta_span)

        variant_list.append(item)

    body.append(variant_list)
    card.append(body)
    return card


def update_index(catalog: OrderedDict[str, CategoryData]) -> None:
    if not INDEX_PATH.exists():
        raise SystemExit('ERROR: index.html não encontrado')

    soup = BeautifulSoup(INDEX_PATH.read_text(encoding='utf-8'), 'html.parser')

    updated_sections: list[tuple[str, int]] = []
    missing_sections: list[str] = []

    for category_id, payload in catalog.items():
        section = soup.find('section', {'id': category_id})
        if not section:
            missing_sections.append(category_id)
            continue
        grid = section.find('div', class_='cards-grid')
        if not grid:
            missing_sections.append(category_id)
            continue

        grid.clear()

        groups = [group for group in payload.groups.values() if group.variants]
        if not groups:
            continue

        for group in groups:
            card = build_card_node(soup, group)
            grid.append(card)
            grid.append('\n')

        updated_sections.append((category_id, len(groups)))

    INDEX_PATH.write_text(soup.prettify(formatter='html'), encoding='utf-8')

    for section_id, count in updated_sections:
        print(f'Section #{section_id} atualizada com {count} cards.')
    if missing_sections:
        print('Atenção: as seguintes sections não foram atualizadas (não encontradas):')
        for section_id in missing_sections:
            print(f'  - {section_id}')


def main() -> None:
    catalog = load_products()
    update_index(catalog)


if __name__ == '__main__':
    main()
