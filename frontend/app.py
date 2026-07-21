import streamlit as st

from components.upload import upload_section
from components.documents import document_list
from components.status import document_status_tracker
from components.chat import chat_interface


st.title(
    "AI Knowledge Assistant"
)


st.header("📤 Upload New Document")

upload_section()

document_status_tracker()

st.divider()

chat_interface()

st.divider()

st.header("📚 Document Library")

document_list()