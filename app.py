from flask import Flask, render_template, request, redirect
from fpdf import FPDF
import os
import urllib.parse

app = Flask(__name__)
PDF_FOLDER = 'pdfs'
os.makedirs(PDF_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('book.html')

@app.route('/book', methods=['POST'])
def book_dj():
    name = request.form['name']
    package = request.form['package']
    hours = request.form['hours']
    date = request.form['date']

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="DJ Booking Confirmation", ln=True)
    pdf.cell(200, 10, txt=f"Client Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Package Selected: {package}", ln=True)
    pdf.cell(200, 10, txt=f"Number of Hours: {hours}", ln=True)
    pdf.cell(200, 10, txt=f"Booking Date: {date}", ln=True)

    filename = f"{name}{package}_invoice.pdf".replace(" ", "")
    pdf_path = os.path.join(PDF_FOLDER, filename)
    pdf.output(pdf_path)

    # WhatsApp setup (use your own number)
    phone_number = '27828490048'  # Example SA number
    link_to_pdf = f"https://yourdomain.com/pdfs/{filename}"
    message = f"Hey! Here’s your DJ booking confirmation: {link_to_pdf}"
    whatsapp_url = f"https://wa.me/{phone_number}?text={urllib.parse.quote(message)}"

    return redirect(whatsapp_url)

if __name__ == '__main__':
    app.run(debug=True)