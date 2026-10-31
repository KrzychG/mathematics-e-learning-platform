"""
Serwis Sanityzacji Treści HTML i Bezpieczeństwa
Ochrona przed atakami XSS przy użyciu biblioteki Bleach
Zapewnia białą listę tagów i atrybutów HTML dla artykułów teorii i edytora CMS
Filtruje szkodliwe skrypty <script>, <style>
Weryfikuje sensowność wprowadzonej treści 
Normalizuje zapis formuł matematycznych pod silnik MathJax 3 / KaTeX 
"""

import html
import re
import bleach

ALLOWED_TAGS = [
    'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'strong', 'em', 'b', 'i', 'u', 's', 'small', 'mark',
    'ul', 'ol', 'li',
    'div', 'span',
    'code', 'pre',
    'table', 'thead', 'tbody', 'tfoot', 'tr', 'td', 'th',
    'blockquote', 'br', 'hr',
    'a', 'sub', 'sup'
]

ALLOWED_ATTRIBUTES = {
    '*': ['class', 'id', 'title'],
    'a': ['href', 'title', 'target', 'rel'],
    'th': ['colspan', 'rowspan', 'scope', 'align'],
    'td': ['colspan', 'rowspan', 'align'],
    'code': ['class'],
    'div': ['class', 'id'],
    'span': ['class', 'id'],
}

ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']

SCRIPT_REGEX = re.compile(r'<\s*(script|style)[^>]*>.*?<\s*/\s*\1\s*>', re.DOTALL | re.IGNORECASE)
DANGLING_SCRIPT_REGEX = re.compile(r'<\s*(script|style)[^>]*>', re.IGNORECASE)
EMPTY_HTML_STRUCTURE_REGEX = re.compile(r'<(?:table|hr|img)\b', re.IGNORECASE)
HTML_TAG_REGEX = re.compile(r'<[^>]+>')
DOLLAR_PATTERN = re.compile(r'(\$\$.*?\$\$)|(?:\$([^$\n]+)\$)', re.DOTALL)

def clean_latex(val: str | None) -> str | None:
    if not val or not isinstance(val, str):
        return val
    return val.strip()


def sanitize_theory_html(raw_html: str | None) -> str:
    if not raw_html:
        return ""
    cleaned = SCRIPT_REGEX.sub('', str(raw_html))
    cleaned = DANGLING_SCRIPT_REGEX.sub('', cleaned)
    sanitized = bleach.clean(
        cleaned,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True
    )
    return sanitized


def has_meaningful_theory(raw_html: str | None) -> bool:
    # Weryfikacja, czy edytor WYSIWYG nie zapisał pustego szablonu
    # czy spacji zerowej szerokości. Przepuszcza treść, jeśli jest tam czytelny tekst
    # lub elementy semantyczne
    if not raw_html:
        return False
    html_str = str(raw_html)
    if EMPTY_HTML_STRUCTURE_REGEX.search(html_str):
        return True
    text_only = html.unescape(HTML_TAG_REGEX.sub('', html_str))
    text_only = text_only.replace('\u200b', '').replace('\u00a0', '').strip()
    return bool(text_only)


def empty_if_meaningless(raw_html: str | None) -> str:
    return raw_html if (raw_html and has_meaningful_theory(raw_html)) else ''


def normalize_theory_input(raw_html: str | None) -> str:
    if not raw_html:
        return ''
    return empty_if_meaningless(sanitize_theory_html(raw_html))


def format_math(val: str | None) -> str:
    # Normalizacja zapisu matematycznego pod KaTeX na frontendzie:
    #  Konwertuje pojedyncze dolary $...$ na notację inline \\( ... \\)
    #Pozostawia podwójne dolary $$...$$ jako wzory blokowe
    # Jeśli tekst zawiera surowy kod LaTeX bez ograniczników
    if not val:
        return ""
    s = clean_latex(str(val).strip())
    def _repl(m):
        if m.group(1):
            return m.group(1)
        return f"\\({m.group(2).strip()}\\)"
    s = DOLLAR_PATTERN.sub(_repl, s)
    if re.search(r'(\${1,2}|\\\(|\\\[)', s):
        return s
    if re.search(r'(\\[a-zA-Z]+|\^|_|\{|\})', s):
        return f"\\({s}\\)"
    return s
