import streamlit as st

from api.client import upload_document


def upload_section():

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
    )

    if uploaded_file:

        if st.button("Upload"):

            with st.spinner(
                "Uploading document..."
            ):

                response = upload_document(
                    uploaded_file
                )
            st.session_state[
                "uploaded_document_id"
            ] = response["id"]   


            st.success(
                "Document uploaded successfully."
            )

            st.info(
                "Your document is being processed. "
            )