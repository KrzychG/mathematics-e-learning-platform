import functools
import re
import markdown
from app.services.sanitizer_service import sanitize_theory_html, clean_latex

DISPLAY_MATH_RE = re.compile(r'(\$\$.*?\$\$)|(\\\[.*?\\\])', re.DOTALL)
INLINE_MATH_RE = re.compile(r'(?<!\\)\$([^\$\n]+?)(?<!\\)\$|(?<!\\)\\\((.*?)(?<!\\)\\\)', re.DOTALL)

FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)

def strip_frontmatter(text: str) -> str:
    if not text:
        return ""
    match = FRONTMATTER_RE.match(text)
    if match:
        return text[match.end():]
    return text


class TheoryRendererService:
    def __init__(self):
        self.md = markdown.Markdown(
            extensions=[
                'extra',
                'nl2br',
                'sane_lists',
            ]
        )

    def _protect_math(self, text: str) -> tuple[str, dict[str, str]]:
        math_map: dict[str, str] = {}
        counter = 0
        def _disp_repl(match):
            nonlocal counter
            key = f"@@MATH_DISPLAY_{counter}@@"
            counter += 1
            math_map[key] = clean_latex(match.group(0))
            return key
        def _inl_repl(match):
            nonlocal counter
            key = f"@@MATH_INLINE_{counter}@@"
            counter += 1
            math_map[key] = clean_latex(match.group(0))
            return key
        text = DISPLAY_MATH_RE.sub(_disp_repl, text)
        text = INLINE_MATH_RE.sub(_inl_repl, text)
        return text, math_map

    def _restore_math(self, html: str, math_map: dict[str, str]) -> str:
        for key, formula in math_map.items():
            html = html.replace(key, formula)
        return html

    def _render_raw_markdown(self, text: str) -> str:
        self.md.reset()
        return self.md.convert(text)

    def render(self, raw_content: str | None) -> str:
        # Pełny potok renderowania teorii z Markdowna do  HTML
        # Obcinamy nagłówek YAML frontmatter
        #_protect_math zastępuje formuły LaTeX unikalnymi tokenami
        # Konwersja Markdown -> HTML, przywrócenie wzorów i ostylowanie tabel pod Bootstrapa.
        # Na koniec Bleach sanityzuje cały wynik z niebezpiecznych tagów i atrybutów.
        if not raw_content:
            return ""
        text = str(raw_content).strip()
        if not text:
            return ""
        body = strip_frontmatter(text)
        protected_text, math_map = self._protect_math(body)
        html = self._render_raw_markdown(protected_text)
        html_with_math = self._restore_math(html, math_map)
        html_with_tables = self._format_tables(html_with_math)
        return sanitize_theory_html(html_with_tables)

    def _format_tables(self, html: str) -> str:
        if '<table' in html:
            def _replace_table(match):
                tag = match.group(0)
                if 'class=' not in tag:
                    return '<div class="table-responsive my-2"><table class="table table-bordered text-center align-middle mb-0">'
                return f'<div class="table-responsive my-2">{tag}'
            formatted = re.sub(r'<table[^>]*>', _replace_table, html)
            formatted = re.sub(r'</table>', r'</table></div>', formatted)
            return formatted
        return html


_default_renderer = TheoryRendererService()


@functools.lru_cache(maxsize=512)
def render_theory_markdown(raw_content: str | None) -> str:
    return _default_renderer.render(raw_content)

