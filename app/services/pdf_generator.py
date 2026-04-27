from pathlib import Path
from typing import List

import markdown as md
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import CSS, HTML

from app.models.models import Lesson, Section

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html"]),
)

_MD_EXTENSIONS = ["extra", "sane_lists", "nl2br"]


def _render_markdown(content: str) -> str:
    if not content:
        return ""
    return md.markdown(content, extensions=_MD_EXTENSIONS, output_format="html5")


def build_lesson_pdf(lesson: Lesson, sections: List[Section]) -> bytes:
    sections_html = [
        {
            "title": s.title or "",
            "html_body": _render_markdown(s.content or ""),
        }
        for s in sections
    ]

    template = _env.get_template("lesson.html")
    html_str = template.render(
        lesson=lesson,
        lesson_number=lesson.order if lesson.order is not None else 1,
        sections_html=sections_html,
    )

    base_url = str(TEMPLATES_DIR)
    html_doc = HTML(string=html_str, base_url=base_url)
    css = CSS(filename=str(TEMPLATES_DIR / "lesson.css"))
    return html_doc.write_pdf(stylesheets=[css])
