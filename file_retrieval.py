import os
from PyPDF2 import PdfReader

class FileRetrieval:
    path = r"C:\Users\syshe\PycharmProjects\FYP\articles"

    @staticmethod
    def retrieve_pdf_files():
        """
        Retrieve the list of PDF files in the specified directory.

        Args:
            directory (str): Path to the directory containing PDF files.

        Returns:
            List[str]: List of PDF file names.
        """
        pdf_files = []
        for file in os.listdir(FileRetrieval.path):
            if file.endswith(".pdf"):
                pdf_files.append(file)
        return pdf_files

    @staticmethod
    def read_pdf_content(filename):
        """
        Read and return the text content of the specified PDF file.

        Args:
            directory (str): Path to the directory containing the PDF file.
            filename (str): Name of the PDF file to read.

        Returns:
            str: Text content of the PDF file.
        """
        if not filename:
            return []  # Return empty list if filename is empty
        filepath = os.path.join(FileRetrieval.path, filename)
        with open(filepath, "rb") as f:
            pdf_reader = PdfReader(f)
            paragraphs = []
            for page_num in range(len(pdf_reader.pages)):
                page_text = pdf_reader.pages[page_num].extract_text()
                paragraphs.extend(page_text.strip().split('\n\n'))  # Split text into paragraphs
        return paragraphs

# if __name__ == "__main__":
#     # Example usage:
#     file_retrieval = FileRetrieval()
#     pdf_files = file_retrieval.retrieve_pdf_files()
#     print("PDF files in directory:")
#     for file in pdf_files:
#         print(file)
#     if pdf_files:
#         selected_file = input("Enter the name of the PDF file to read: ")
#         content = file_retrieval.read_pdf_content(selected_file)
#         print(content.len())
#         # print("Content of the selected PDF file:")
#         # print(content)
