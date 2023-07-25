import jinja2
import pdfkit
import os
import sys

def get_wkhtmltopdf_path() -> str:
    if sys.platform.startswith('linux'):
        # Linux
        return '/usr/local/bin/wkhtmltopdf'
    elif sys.platform.startswith('darwin'):
        # macOS
        return '/usr/local/bin/wkhtmltopdf'
    elif sys.platform.startswith('win'):
        # Windows
        return r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    else:
        raise OSError("Unsupported operating system. Please install wkhtmltopdf and set the path manually.")


template = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'template')))
template = template.get_template('index.html')

wkhtmltopdf_path = get_wkhtmltopdf_path()
conf = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

def generate_pdf(questions, pdf_name):
    html = template.render(questions=questions)
    pdfkit.from_string(html, f'{pdf_name}.pdf')
    return True