from fpdf import FPDF
import os

def export_to_pdf(data, filename):
    if not os.path.exists("output"):
        os.makedirs("output")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for row in data:
        line = ", ".join([f"{key}: {value}" for key, value in row.items()])
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output(f"output/{filename}.pdf")
