import os
import pdfkit

def md_to_pdf(md_content: str, output_path: str):
    """Markdown转PDF（极简版）"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    options = {
        "encoding": "UTF-8",
        "quiet": ""
    }
    pdfkit.from_string(md_content, output_path, options=options)