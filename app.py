# app.py
from flask import Flask, render_template, request
from fpdf import FPDF
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        package = request.form['package']
        hours = request.form['hours']
        event_time = request.form['date']


        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="DJ Booking Confirmation", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
        pdf.cell(200, 10, txt=f"Package: {package}", ln=True)
        pdf.cell(200, 10, txt=f"Hours: {hours}", ln=True)
        pdf.cell(200, 10, txt=f"When: {event_time}", ln=True)

        now = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{name.replace(' ', '')}{now}.pdf"
        pdf_folder = os.path.join("static", "pdfs")
        os.makedirs(pdf_folder, exist_ok=True)
        filepath = os.path.join(pdf_folder, filename)
        pdf.output(filepath)

        public_url = f"https://dj-imln.onrender.com/static/pdfs/{filename}"
        message = f"Hey, here's your DJ booking confirmation: {public_url}"
        whatsapp_number = "27677801555"
        whatsapp_url = f"https://wa.me/{whatsapp_number}?text={message.replace(' ', '%20')}"

        return render_template("confirmation.html", pdf_url=public_url, whatsapp_url=whatsapp_url)

    return render_template("book.html")

if __name__ == '__main__':
    app.run(debug=True)