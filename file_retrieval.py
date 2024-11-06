import os
from PyPDF2 import PdfReader

class FileRetrieval:
    path = r"C:\Users\syshe\PycharmProjects\FYP\articles"

    @staticmethod
    def retrieve_pdf_files():
        pdf_files = [file for file in os.listdir(FileRetrieval.path) if file.endswith(".pdf")]
        return pdf_files

    @staticmethod
    def read_pdf_content(filename, paragraph_limit=6):
        if not filename:
            return []
        filepath = os.path.join(FileRetrieval.path, filename)
        with open(filepath, "rb") as f:
            pdf_reader = PdfReader(f)
            paragraphs = []
            for page_num in range(len(pdf_reader.pages)):
                page_text = pdf_reader.pages[page_num].extract_text()
                if page_text:
                    page_paragraphs = page_text.strip().split('\n\n')  # Split text into paragraphs
                    for paragraph in page_paragraphs:
                        if len(paragraphs) < paragraph_limit:
                            paragraphs.append(paragraph.strip())
                        else:
                            break
                if len(paragraphs) >= paragraph_limit:
                    break
        return paragraphs


# content = FileRetrieval.read_pdf_content("AI and Human Future.pdf", paragraph_limit=6)
# print(content)