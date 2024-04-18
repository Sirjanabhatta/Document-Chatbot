import streamlit as st
from app.enum.llm import Llm
from app.core.config import load_config
from app.llm import get_pdf_text, get_chunks, get_vector_store, user_input


def main():
    load_config()
    st.set_page_config("smart-doc-bot")
    st.header("Chat with PDF")

    user_question = st.text_input("Ask a Question from the PDF Files")
    llm_option = st.radio("Choose Model", [Llm.GEMINI.value, Llm.OPENAI.value])
    if user_question:
        user_input(
            user_question,
            llm=Llm.GEMINI.value if llm_option == Llm.GEMINI.value else Llm.OPENAI.value
        )

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader(
            "Upload your PDF Files and Click on the Submit & Process Button",
            accept_multiple_files=True,
        )
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_chunks(raw_text)
                get_vector_store(
                    text_chunks,
                    llm=Llm.GEMINI.value if llm_option == Llm.GEMINI.value else Llm.OPENAI.value
                )
                st.success("Done")


if __name__ == "__main__":
    main()
