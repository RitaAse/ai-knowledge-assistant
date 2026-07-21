import streamlit as st

from components.upload import upload_section
from components.documents import document_list
from components.status import document_status_tracker
from components.chat import chat_interface


st.title(
    "AI Knowledge Assistant"
)


with st.sidebar:

    st.header("📚 Document Library")

    st.subheader("📤 Upload Document")

    upload_section()

    st.divider()

    document_status_tracker()

    st.divider()

    document_list()


chat_interface()