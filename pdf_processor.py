import PyPDF2 as pdf

def extract_text_from_pdf(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += str(page.extract_text())
    return extracted_text