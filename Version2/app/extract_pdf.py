import fitz  # PyMuPDF


def extract_text_from_pdf(uploaded_file):
    # Open the PDF file using the file-like object
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    cv_resume = ""

    # Iterate through all the pages and extract text
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)  # Get page by index
        # Extract text in plain text format
        cv_resume += page.get_text("text") + "\n"

    pdf_document.close()  # Close the PDF file
    return cv_resume
