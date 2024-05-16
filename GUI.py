import streamlit as st
from file_retrieval import FileRetrieval


def main():
    st.title("Reading Module")

    # Display initial message
    username = "Fiona"
    st.write(f"Hi {username}! Let's do some reading, shall we? Choose one of the topics below:")

    # Retrieve PDF files
    file_retrieval = FileRetrieval()
    pdf_files = file_retrieval.retrieve_pdf_files()

    # Extract article names (remove '.pdf' extension)
    article_names = [file.replace('.pdf', '') for file in pdf_files]

    # Selectbox for choosing an article
    selected_article = st.selectbox("Select an article:", article_names)

    content_displayed = False  # Flag to track if content has been displayed

    # Submit button
    if st.button("Submit"):
        # Read content of selected PDF file
        paragraphs = file_retrieval.read_pdf_content(f"{selected_article}.pdf")

        # Check if content exists
        if paragraphs:
            # Combine paragraphs into one Markdown block
            markdown_content = "\n\n".join(paragraphs)

            # Display content in a styled container
            st.markdown(
                f"""
                <div style="background-color: #2c2e30; padding: 10px; border-radius: 5px;">
                    {markdown_content}
                </div>
                """
                ,
                unsafe_allow_html=True
            )

            # Set content_displayed to True
            content_displayed = True

    # Display questions only if content has been displayed
    if content_displayed:
        st.write(f"Let's do some questions to check your understanding, shall we?")
        if st.button("I'm ready!"):
            pass


if __name__ == "__main__":
    main()
