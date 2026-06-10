#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Combine markdown files and convert to PDF."""

import os
import re
from markdown import markdown
from xhtml2pdf import pisa

OUTPUT_DIR = r"D:\b\output"

# Define the 4 source files in order
FILES = [
    "01-AI技术应用场景匹配报告.md",
    "02-软件过程改进方案设计文档.md",
    "03-AI技术应用验证报告.md",
    "04-改进后的软件过程定义文档.md",
]

COVER_TITLE = "软件过程与管理作业"
COVER_SUBTITLE = "AI增强型软件过程改进方案"
COVER_INFO = "四川大学软件学院\n2026年春季学期"


def clean_mermaid(md_text):
    """Replace mermaid code blocks with styled pre blocks for PDF rendering."""
    # Replace ```mermaid ... ``` with a labeled code block
    pattern = r'```mermaid\n(.*?)```'
    replacement = r'```text\n[Mermaid流程图 - 请在Markdown中查看]\n\1\n```'
    return re.sub(pattern, replacement, md_text, flags=re.DOTALL)


def read_and_process_file(filepath):
    """Read a markdown file and process it for conversion."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = clean_mermaid(content)
    return content


def build_html():
    """Combine all markdown files into a single HTML document."""
    css = """
    <style>
        @page {
            size: A4;
            margin: 2cm 2.5cm;
            @frame header {
                -pdf-frame-content: headerContent;
                top: 1cm;
                margin-left: 2.5cm;
                margin-right: 2.5cm;
                height: 1cm;
            }
            @frame footer {
                -pdf-frame-content: footerContent;
                bottom: 1cm;
                margin-left: 2.5cm;
                margin-right: 2.5cm;
                height: 1cm;
            }
        }
        body {
            font-family: "SimSun", "Microsoft YaHei", sans-serif;
            font-size: 11pt;
            line-height: 1.8;
            color: #333;
        }
        h1 {
            font-size: 20pt;
            color: #1a5276;
            border-bottom: 2px solid #2980b9;
            padding-bottom: 8px;
            margin-top: 30px;
            page-break-before: always;
        }
        h2 {
            font-size: 16pt;
            color: #2471a3;
            border-bottom: 1px solid #aed6f1;
            padding-bottom: 5px;
            margin-top: 25px;
        }
        h3 {
            font-size: 13pt;
            color: #2e86c1;
            margin-top: 20px;
        }
        h4 {
            font-size: 12pt;
            color: #3498db;
            margin-top: 15px;
        }
        p {
            text-align: justify;
            margin: 8px 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 9pt;
        }
        th {
            background-color: #2980b9;
            color: white;
            padding: 8px 6px;
            text-align: left;
            font-weight: bold;
        }
        td {
            border: 1px solid #bdc3c7;
            padding: 6px;
        }
        tr:nth-child(even) {
            background-color: #eaf2f8;
        }
        code {
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: "Consolas", "Courier New", monospace;
            font-size: 9pt;
        }
        pre {
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-left: 4px solid #2980b9;
            padding: 10px;
            font-family: "Consolas", "Courier New", monospace;
            font-size: 8pt;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        blockquote {
            border-left: 4px solid #3498db;
            margin: 10px 0;
            padding: 8px 15px;
            background-color: #ebf5fb;
            color: #1a5276;
        }
        ul, ol {
            margin: 8px 0;
            padding-left: 25px;
        }
        li {
            margin: 3px 0;
        }
        strong {
            color: #1a5276;
        }
        hr {
            border: none;
            border-top: 1px solid #bdc3c7;
            margin: 20px 0;
        }
        /* Cover page */
        .cover-page {
            text-align: center;
            padding-top: 200px;
            page-break-after: always;
        }
        .cover-page h1 {
            font-size: 28pt;
            color: #1a5276;
            border: none;
            margin-bottom: 20px;
            page-break-before: avoid;
        }
        .cover-page .subtitle {
            font-size: 18pt;
            color: #2980b9;
            margin-bottom: 60px;
        }
        .cover-page .info {
            font-size: 14pt;
            color: #555;
            line-height: 2.5;
        }
        /* TOC */
        .toc {
            page-break-after: always;
        }
        .toc h2 {
            text-align: center;
        }
        .toc ul {
            list-style: none;
            padding: 0;
        }
        .toc li {
            padding: 5px 0;
            border-bottom: 1px dotted #ccc;
        }
        .toc a {
            color: #2471a3;
            text-decoration: none;
        }
        .footer {
            text-align: center;
            font-size: 8pt;
            color: #999;
        }
    </style>
    """

    header_footer = """
    <div id="headerContent" style="text-align:right;font-size:8pt;color:#999;border-bottom:1px solid #ccc;padding-bottom:3px;">
        软件过程与管理作业 - AI增强型软件过程改进方案
    </div>
    <div id="footerContent" style="text-align:center;font-size:8pt;color:#999;">
        第 <pdf:pagenumber> 页
    </div>
    """

    # Build cover page
    cover_html = f"""
    <div class="cover-page">
        <h1>{COVER_TITLE}</h1>
        <div class="subtitle">{COVER_SUBTITLE}</div>
        <div class="info">{COVER_INFO.replace(chr(10), '<br>')}</div>
    </div>
    """

    # Build TOC
    toc_items = [
        "一、AI技术应用场景匹配报告",
        "二、软件过程改进方案设计文档",
        "三、AI技术应用验证报告",
        "四、改进后的完整软件过程定义文档",
    ]
    toc_html = '<div class="toc"><h2>目  录</h2><ul>'
    for item in toc_items:
        toc_html += f'<li>{item}</li>'
    toc_html += '</ul></div>'

    # Combine all document bodies
    body_parts = []
    for i, filename in enumerate(FILES):
        filepath = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(filepath):
            md_content = read_and_process_file(filepath)
            html_body = markdown(
                md_content,
                extensions=['tables', 'fenced_code', 'codehilite', 'toc', 'nl2br']
            )
            # Don't add page-break before first document's h1 (it's the cover)
            if i == 0:
                html_body = re.sub(
                    r'<h1>',
                    '<h1 style="page-break-before: avoid;">',
                    html_body,
                    count=1
                )
            body_parts.append(html_body)

    full_body = "\n".join(body_parts)

    # Complete HTML
    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    {css}
</head>
<body>
    {header_footer}
    {cover_html}
    {toc_html}
    {full_body}
</body>
</html>
    """
    return full_html


def convert_to_pdf(html_content, output_path):
    """Convert HTML content to PDF using xhtml2pdf."""
    with open(output_path, 'wb') as pdf_file:
        pisa_status = pisa.CreatePDF(
            html_content,
            dest=pdf_file,
            encoding='utf-8',
        )
    return not pisa_status.err


def main():
    print("Building HTML from markdown files...")
    html_content = build_html()

    # Save intermediate HTML for debugging
    html_path = os.path.join(OUTPUT_DIR, "combined.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML saved to: {html_path}")

    # Convert to PDF
    pdf_path = os.path.join(OUTPUT_DIR, "软件过程与管理作业.pdf")
    print(f"Converting to PDF: {pdf_path} ...")
    success = convert_to_pdf(html_content, pdf_path)

    if success:
        print(f"PDF generated successfully: {pdf_path}")
        # Get file size
        size_kb = os.path.getsize(pdf_path) / 1024
        print(f"File size: {size_kb:.1f} KB")
    else:
        print("PDF generation failed!")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
