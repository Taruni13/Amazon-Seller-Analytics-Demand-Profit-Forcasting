"""
Script to generate a Word document and PowerPoint slides from REPORT.md.
Requires: python-docx, python-pptx, markdown (for optional parsing)

Usage:
    pip install -r requirements.txt
    python scripts/create_report.py

This will create `MSBA_286_Report_Group7.docx` and `MSBA_286_Slides_Group7.pptx` in the repository root.
"""
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from pptx import Presentation
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
REPORT_MD = ROOT / 'REPORT.md'
OUT_DOCX = ROOT / 'MSBA_286_Report_Group7.docx'
OUT_PPTX = ROOT / 'MSBA_286_Slides_Group7.pptx'


def load_markdown(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def make_docx(md_text: str, out_path: Path):
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)

    # Title page: first lines until a blankline
    lines = md_text.splitlines()
    # Cover data from top of file
    title = lines[0] if lines else 'MSBA 286 Project'
    doc.add_paragraph(title).alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    doc.add_paragraph('')

    # Add content: simple parsing by headers
    i = 0
    for line in lines[1:]:
        if line.strip() == '':
            doc.add_paragraph('')
            continue
        if line.startswith('='):
            continue
        if line.endswith(':') and len(line) < 100:
            p = doc.add_heading(line.strip(), level=2)
            continue
        # Headings
        if line.startswith('1.') or line.startswith('2.') or line.startswith('3.') or line.startswith('4.'):
            doc.add_heading(line.strip(), level=2)
            continue
        # For any other line, add a paragraph
        doc.add_paragraph(line)

    # Add footer note about line numbers
    section = doc.sections[0]
    footer = section.footer.paragraphs[0]
    footer.text = 'Note: To enable line numbers, open this document in MS Word and select Layout → Line Numbers.'

    doc.save(out_path)
    print('Saved DOCX to', out_path)


def make_pptx(md_text: str, out_path: Path):
    prs = Presentation()
    prs.slide_height = Inches(7.0)
    prs.slide_width = Inches(12.8)

    # Title slide
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = 'MSBA 286 — Capstone Final Project'
    subtitle.text = 'Group 7 — Amazon Seller Analytics Dashboard'

    # Create slides for main sections: Abstract, Methods, Data, Results, Conclusions
    sections = ['Abstract', 'Data', 'Methods', 'Results', 'Discussion', 'Conclusion']
    for s in sections:
        slide_layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(slide_layout)
        slide.shapes.title.text = s
        body = slide.shapes.placeholders[1].text_frame
        # Add placeholder bullet points — user can refine
        if s == 'Abstract':
            body.text = 'Project objective and short summary of approach and key findings.'
        elif s == 'Data':
            body.text = 'Datasets used: clean_global_sales.csv; clean_e-commerce_orders.csv. Source, size, key columns.'
        elif s == 'Methods':
            body.text = 'EDA, Random Forest, Gradient Boosting, ARIMA. Model evaluation: MAE, RMSE.'
        elif s == 'Results':
            body.text = 'Top SKUs, revenue by region, model performance (MAE/RMSE), forecasts for next months.'
        elif s == 'Discussion':
            body.text = 'Interpretation, managerial implications, limitations.'
        elif s == 'Conclusion':
            body.text = 'Summary of key recommendations and next steps.'

    prs.save(out_path)
    print('Saved PPTX to', out_path)


if __name__ == '__main__':
    md = load_markdown(REPORT_MD)
    make_docx(md, OUT_DOCX)
    make_pptx(md, OUT_PPTX)
