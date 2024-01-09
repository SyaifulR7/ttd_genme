import aspose.pdf as ap, time, json, base64
from PyPDF2 import PdfWriter, PdfReader
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

image = "ttd.png"
input = 'input.pdf'
output_belum_ttd = 'output_belum_ttd.pdf'
output_sudah_ttd = 'output_sudah_ttd.pdf'
input_tanpa_ttd = 'input_tanpa_ttd.pdf'
file_jadi = 'file_jadi.pdf'

def base64_to_pdf(data):
    decoded_data = base64.b64decode(data)
    with open(input, 'wb') as output_file:
        output_file.write(decoded_data)
        print("base64 to pdf done")

def pdf_to_base64(output_sudah_ttd):
    with open(output_sudah_ttd, "rb") as file:
        encoded_pdf = base64.b64encode(file.read())
        return encoded_pdf.decode("utf-8")
        print("pdf to base64 done")

def mengambil_halaman_ttd():
    with open(input, 'rb') as file:
        pdf_reader = PdfReader(file)
        pdf_writer = PdfWriter()
        total_pages = len(pdf_reader.pages)

        page_found = ""

        for page_number, page in enumerate(pdf_reader.pages, start=1):
            kalimat = "S u h e r l i"
            if kalimat in page.extract_text():
                page_found = page_number

        for page in range(total_pages):
            if page == page_found - 1:
                pdf_writer.add_page(pdf_reader.pages[page])

        with open(output_belum_ttd, 'wb') as output_file:
            pdf_writer.write(output_file)

            print("mengambil halaman ttd done")

def memisahkan_halaman_ttd():
    with open(input, 'rb') as file:
        pdf_reader = PdfReader(file)
        pdf_writer = PdfWriter()
        total_pages = len(pdf_reader.pages)

        page_found = ""

        for page_number, page in enumerate(pdf_reader.pages, start=1):
            kalimat = "S u h e r l i"
            if kalimat in page.extract_text():
                page_found = page_number

        for page in range(total_pages):
            if page != page_found - 1:
                pdf_writer.add_page(pdf_reader.pages[page])

        with open(input_tanpa_ttd, 'wb') as output_file:
            pdf_writer.write(output_file)

            print("memisahkan halaman ttd done")

def insert_ttd():
    document = ap.Document(output_belum_ttd)
    document.pages[1].add_image(image, ap.Rectangle( 300, 250, 600, 850, True ))
    document.save(output_sudah_ttd)
    print("insert ttd done")

@app.route("/ttd_genme", methods=["POST"])

def menggambungkan_halaman_ttd():

    data = request.form['pdf_base64']
    
    base64_to_pdf(data)
    mengambil_halaman_ttd()
    memisahkan_halaman_ttd()
    insert_ttd()
    print("menggambungkan halaman ttd done")
    pdf_to_base64(data)
    return {
        "status": "200",
        "message": "success",
    }

if __name__ == "__main__":
    app.run(host='192.168.0.110',port='5000',debug=True)