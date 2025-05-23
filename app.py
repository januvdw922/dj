from flask import Flask, render_template, request
from fpdf import FPDF
import os
from datetime import datetime

app = Flask(_name_)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Pricing page
@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

# Book page
@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        package = request.form['package']
        hours = request.form['hours']
        event_time = request.form['event_time']

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="DJ Booking Confirmation", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
        pdf.cell(200, 10, txt=f"Package: {package}", ln=True)
        pdf.cell(200, 10, txt=f"Hours: {hours}", ln=True)
        pdf.cell(200, 10, txt=f"When: {event_time}", ln=True)

        # Save PDF
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{name.replace(' ', '')}{now}.pdf"
        filepath = os.path.join("pdfs", filename)
        pdf.output(filepath)

        # Create WhatsApp message
        message = f"Hi, here is your DJ booking confirmation:\nhttps://yourdomain.com/{filepath}"
        whatsapp_url = f"https://wa.me/?text={message.replace(' ', '%20')}"

        return redirect(whatsapp_url)

    return render_template('book.html')

if _name_ == '_main_':
    app.run(debug=True)