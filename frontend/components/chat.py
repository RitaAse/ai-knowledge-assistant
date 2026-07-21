import streamlit as st

from api.client import search_documents

def chat_interface():

    st.header("💬 Ask Questions")

    question = st.text_input(
        "Ask a question about your uploaded documents"
    )

    if st.button("Ask"):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

            return

        with st.spinner(
            "Thinking..."
        ):

            result = search_documents(
                question
            )

        st.subheader("Answer")

        st.write(
            result["answer"]
        )