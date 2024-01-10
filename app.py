import aspose.pdf as ap, time, json, base64, os
from PyPDF2 import PdfWriter, PdfReader
from flask import Flask, request
from flask_cors import CORS
from env import host, port

app = Flask(__name__)
CORS(app)

image = 'file/ttd.png'
input = 'file/hasil/input.pdf'
output_belum_ttd = 'file/hasil/output_belum_ttd.pdf'
output_sudah_ttd = 'file/hasil/output_sudah_ttd.pdf'
input_tanpa_ttd = 'file/hasil/input_tanpa_ttd.pdf'
file_jadi = 'file/hasil/file_jadi.pdf'

def base64_to_pdf(pdf_base64):
    decoded_data = base64.b64decode(pdf_base64)
    with open(input, 'wb') as output_file:
        output_file.write(decoded_data)
        print("base64 to pdf done")

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

def menggabungkan_halaman_ttd():
    file3 = open(input, 'rb')
    pdf3 = PdfReader(file3)
    page_found = ""

    for page_number, page in enumerate(pdf3.pages, start=1):
        kalimat = "S u h e r l i"
        if kalimat in page.extract_text():
            page_found = page_number

    file1 = open(output_sudah_ttd, 'rb')
    pdf1 = PdfReader(file1)
    file2 = open(input_tanpa_ttd, 'rb')
    pdf2 = PdfReader(file2)
    pdf_writer = PdfWriter()

    for page_num2 in range(len(pdf2.pages)):
        page2 = pdf2.pages[page_num2]
        pdf_writer.add_page(page2)
        if page_num2 == page_found - 2:
            for page_num1 in range(len(pdf1.pages)):
                page1 = pdf1.pages[page_num1]
                pdf_writer.add_page(page1)

    output_file = open(file_jadi, 'wb')
    pdf_writer.write(output_file)
    print("menggabungkan_halaman_ttd")

@app.route("/ttd_genme", methods=["POST"])

def pdf_to_base64():

    authorization_code = '7059416d65dda4b9d5aa1d9b0bfcdf125ef65644e2e10cc7e499ce6ffe0a'
    response_authorization_code = request.headers.get("Authorization")
    start_time = time.time()

    if(response_authorization_code != authorization_code):
        json_content = {
            "code": 401,
            "message_code": 1,
            "message": "Autentikasi Gagal",
            "finish_time": time.time() - start_time,
            "hasil": "",
        }
    else:
        if ('pdf_base64' not in request.form):
            json_content = {
                "code": 401,
                "message_code": 2,
                "message": "Autentikasi Berhasil, Parameter 'base64_pdf' Tidak Ada",
                "finish_time": time.time() - start_time,
                "hasil": "",
            }
        elif(request.form['pdf_base64'] == ""):
            json_content = {
                "code": 401,
                "message_code": 3,
                "message": "Autentikasi Berhasil, Isi Parameter 'base64_pdf' Kosong",
                "finish_time": time.time() - start_time,
                "hasil": "",
            }
        else:
            pdf_base64 = request.form['pdf_base64']
            base64_to_pdf(pdf_base64)
            mengambil_halaman_ttd()
            memisahkan_halaman_ttd()
            insert_ttd()
            menggabungkan_halaman_ttd()

            with open(file_jadi, "rb") as file:
                encoded_pdf = base64.b64encode(file.read())

            json_content = {
                "code": 200,
                "message_code": 4,
                "message": "Autentikasi Berhasil, Proses Selesai",
                "finish_time": time.time() - start_time,
                "hasil": encoded_pdf.decode("utf-8"),
            }
    
    python2json = json.dumps(json_content)

    print("pdf to base64 done")

    # hapus hasil file pdf
    # file_names = os.listdir('file/hasil')
    # for file_name in file_names:
    #     file_path = os.path.join('file/hasil', file_name)
    #     os.remove(file_path)

    return app.response_class(python2json, content_type = 'application/json')

if __name__ == "__main__":
    app.run(host=host,port=port,debug=True)